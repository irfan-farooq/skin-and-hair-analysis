package main

import (
	"crypto/rand"
	"database/sql"
	"encoding/hex"
	"encoding/json"
	"log"
	"time"

	_ "modernc.org/sqlite"
)

type SessionStore struct {
	db *sql.DB
}

func NewSessionStore() *SessionStore {
	db, err := sql.Open("sqlite", "sessions.db")
	if err != nil {
		log.Fatalf("failed to open sessions db: %v", err)
	}

	_, err = db.Exec(`
		CREATE TABLE IF NOT EXISTS sessions (
			id         TEXT PRIMARY KEY,
			history    TEXT NOT NULL,
			updated_at INTEGER NOT NULL
		)
	`)
	if err != nil {
		log.Fatalf("failed to create sessions table: %v", err)
	}

	s := &SessionStore{db: db}
	go s.cleanup()
	return s
}

func (s *SessionStore) Get(id string) []Message {
	var historyJSON string
	err := s.db.QueryRow("SELECT history FROM sessions WHERE id = ?", id).Scan(&historyJSON)
	if err != nil {
		return []Message{}
	}

	var history []Message
	if err := json.Unmarshal([]byte(historyJSON), &history); err != nil {
		log.Printf("failed to unmarshal history for %s: %v", id, err)
		return []Message{}
	}
	return history
}

func (s *SessionStore) Set(id string, history []Message) {
	historyJSON, err := json.Marshal(history)
	if err != nil {
		log.Printf("failed to marshal history for %s: %v", id, err)
		return
	}

	_, err = s.db.Exec(`
		INSERT INTO sessions (id, history, updated_at)
		VALUES (?, ?, ?)
		ON CONFLICT(id) DO UPDATE SET
			history = excluded.history,
			updated_at = excluded.updated_at
	`, id, string(historyJSON), time.Now().Unix())
	if err != nil {
		log.Printf("failed to save session %s: %v", id, err)
	}
}

func (s *SessionStore) Delete(id string) {
	_, err := s.db.Exec("DELETE FROM sessions WHERE id = ?", id)
	if err != nil {
		log.Printf("failed to delete session %s: %v", id, err)
	}
}
func (s *SessionStore) cleanup() {
	ticker := time.NewTicker(15 * time.Minute)
	for range ticker.C {
		cutoff := time.Now().Add(-time.Hour).Unix()
		_, err := s.db.Exec("DELETE FROM sessions WHERE updated_at < ?", cutoff)
		if err != nil {
			log.Printf("cleanup error: %v", err)
		}
	}
}

func generateSessionID() string {
	b := make([]byte, 16)
	rand.Read(b)
	return hex.EncodeToString(b)
}
