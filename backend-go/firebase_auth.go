package main

import (
	"crypto/rsa"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

type keyCache struct {
	mu     sync.RWMutex
	keys   map[string]*rsa.PublicKey
	expiry time.Time
}

var cache = &keyCache{}

func getPublicKeys() (map[string]*rsa.PublicKey, error) {
	cache.mu.RLock()
	if time.Now().Before(cache.expiry) && cache.keys != nil {
		defer cache.mu.RUnlock()
		return cache.keys, nil
	}
	cache.mu.RUnlock()

	resp, err := http.Get(
		"https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com",
	)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch public keys: %w", err)
	}
	defer resp.Body.Close()

	maxAge := 3600 * time.Second
	cc := resp.Header.Get("Cache-Control")
	for _, part := range strings.Split(cc, ",") {
		part = strings.TrimSpace(part)
		if strings.HasPrefix(part, "max-age=") {
			fmt.Sscanf(part, "max-age=%d", &maxAge)
		}
	}

	var certs map[string]string
	if err := json.NewDecoder(resp.Body).Decode(&certs); err != nil {
		return nil, fmt.Errorf("failed to decode certs: %w", err)
	}

	keys := make(map[string]*rsa.PublicKey)
	for kid, certPEM := range certs {
		block, _ := pem.Decode([]byte(certPEM))
		if block == nil {
			continue
		}
		cert, err := x509.ParseCertificate(block.Bytes)
		if err != nil {
			continue
		}
		rsaKey, ok := cert.PublicKey.(*rsa.PublicKey)
		if !ok {
			continue
		}
		keys[kid] = rsaKey
	}

	cache.mu.Lock()
	cache.keys = keys
	cache.expiry = time.Now().Add(time.Duration(maxAge) * time.Second)
	cache.mu.Unlock()

	return keys, nil
}

func VerifyFirebaseToken(tokenString, projectID string) (*jwt.MapClaims, error) {
	keys, err := getPublicKeys()
	if err != nil {
		return nil, err
	}

	iss := fmt.Sprintf("https://securetoken.google.com/%s", projectID)

	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {

		if _, ok := token.Method.(*jwt.SigningMethodRSA); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}

		kid, ok := token.Header["kid"].(string)
		if !ok {
			return nil, fmt.Errorf("missing kid in token header")
		}

		key, exists := keys[kid]
		if !exists {
			return nil, fmt.Errorf("unknown kid: %s", kid)
		}

		return key, nil
	}, jwt.WithIssuer(iss), jwt.WithAudience(projectID))

	if err != nil {
		return nil, fmt.Errorf("token parse failed: %w", err)
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || !token.Valid {
		return nil, fmt.Errorf("invalid token claims")
	}

	return &claims, nil
}

func FirebaseAuth(projectID string, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {

		authHeader := r.Header.Get("Authorization")
		if authHeader == "" {
			http.Error(w, "missing Authorization header", http.StatusUnauthorized)
			return
		}

		parts := strings.SplitN(authHeader, " ", 2)
		if len(parts) != 2 || parts[0] != "Bearer" {
			http.Error(w, "invalid Authorization format", http.StatusUnauthorized)
			return
		}

		tokenString := parts[1]

		claims, err := VerifyFirebaseToken(tokenString, projectID)
		if err != nil {
			http.Error(w, "unauthorized: "+err.Error(), http.StatusUnauthorized)
			return
		}
		uid := fmt.Sprintf("%v", (*claims)["sub"])
		r.Header.Set("X-User-UID", uid)

		next.ServeHTTP(w, r)
	})
}
