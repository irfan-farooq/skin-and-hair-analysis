package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/joho/godotenv"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file, using environment variables")
	}
	projectID := os.Getenv("FIREBASE_PROJECT_ID")
	flaskURL := os.Getenv("FLASK_BACKEND_URL")
	port := os.Getenv("PORT")
	if projectID == "" {
		log.Fatal("FIREBASE_PROJECT_ID not set")
	}
	if port == "" {
		port = "8080"
	}

	proxyHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		targetURL := flaskURL + r.URL.Path
		req, err := http.NewRequest(r.Method, targetURL, r.Body)
		if err != nil {
			http.Error(w, "proxy error", http.StatusInternalServerError)
			return
		}
		for key, values := range r.Header {
			for _, v := range values {
				req.Header.Add(key, v)
			}
		}
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			http.Error(w, "failed to reach Flask: "+err.Error(), http.StatusBadGateway)
			return
		}
		defer resp.Body.Close()
		w.WriteHeader(resp.StatusCode)
		io.Copy(w, resp.Body)
	})
	protected := FirebaseAuth(projectID, proxyHandler)

	r := chi.NewRouter()
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(60 * time.Second))
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedMethods:   []string{"GET", "POST", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Content-Type", "Authorization"},
		AllowCredentials: false,
	}))

	r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`{"status":"ok"}`))
	})
	r.With(func(next http.Handler) http.Handler {
		return FirebaseAuth(projectID, next)
	}).Post("/chat", handleChat)

	r.With(func(next http.Handler) http.Handler {
		return FirebaseAuth(projectID, next)
	}).Post("/chat/reset", handleReset)

	r.Post("/register", http.HandlerFunc(registerHandler).ServeHTTP)

	r.Handle("/*", protected)

	log.Printf("SkinMax gateway + chatbot running on :%s -> Flask at %s", port, flaskURL)
	log.Fatal(http.ListenAndServe(":"+port, r))
}

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type ChatRequest struct {
	SessionID   string       `json:"session_id"`
	Message     string       `json:"message"`
	SkinProfile *SkinProfile `json:"skin_profile,omitempty"`
}

type SkinProfile struct {
	SkinType string   `json:"skin_type"`
	Concerns []string `json:"concerns"`
	SkinTone string   `json:"skin_tone"`
	HairType string   `json:"hair_type"`
}

type ChatResponse struct {
	Reply     string `json:"reply"`
	SessionID string `json:"session_id"`
}

var sessionStore = NewSessionStore()

func handleChat(w http.ResponseWriter, r *http.Request) {
	var req ChatRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request", http.StatusBadRequest)
		return
	}

	if req.Message == "" {
		http.Error(w, "message is required", http.StatusBadRequest)
		return
	}

	if req.SessionID == "" {
		req.SessionID = generateSessionID()
	}

	history := sessionStore.Get(req.SessionID)
	history = append(history, Message{Role: "user", Content: req.Message})
	systemPrompt := buildSystemPrompt(req.SkinProfile)

	reply, err := callLLM(r.Context(), systemPrompt, history)
	if err != nil {
		log.Printf("LLM error: %v", err)
		http.Error(w, "AI service error", http.StatusInternalServerError)
		return
	}

	history = append(history, Message{Role: "assistant", Content: reply})
	sessionStore.Set(req.SessionID, history)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(ChatResponse{
		Reply:     reply,
		SessionID: req.SessionID,
	})
}

func handleReset(w http.ResponseWriter, r *http.Request) {
	var body struct {
		SessionID string `json:"session_id"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil || body.SessionID == "" {
		http.Error(w, "session_id required", http.StatusBadRequest)
		return
	}
	sessionStore.Delete(body.SessionID)
	w.Write([]byte(`{"status":"reset"}`))
}

func buildSystemPrompt(profile *SkinProfile) string {
	base := `You are Glow, a friendly and knowledgeable AI skincare assistant for SkinMax.
You help users understand their skin, recommend routines, explain ingredients, and answer skincare and haircare questions.
Keep responses concise, warm, and practical. Use simple language and avoid overwhelming jargon.
If a question is unrelated to skincare, haircare, or wellness, politely redirect the user.`

	if profile == nil {
		return base
	}

	profileContext := "\n\nUser's skin profile from analysis:\n"
	if profile.SkinType != "" {
		profileContext += "- Skin type: " + profile.SkinType + "\n"
	}
	if len(profile.Concerns) > 0 {
		profileContext += "- Concerns: "
		for i, c := range profile.Concerns {
			if i > 0 {
				profileContext += ", "
			}
			profileContext += c
		}
		profileContext += "\n"
	}
	if profile.SkinTone != "" {
		profileContext += "- Skin tone: " + profile.SkinTone + "\n"
	}
	if profile.HairType != "" {
		profileContext += "- Hair type: " + profile.HairType + "\n"
	}
	profileContext += "\nTailor your advice to this user's specific profile when relevant."

	return base + profileContext
}
