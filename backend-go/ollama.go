package main

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"time"
)

// --- Ollama request/response shapes ---

type OllamaRequest struct {
	Model    string    `json:"model"`
	Messages []Message `json:"messages"`
	Stream   bool      `json:"stream"`
}

type OllamaResponse struct {
	Message Message `json:"message"`
}

func callLLM(ctx context.Context, system string, history []Message) (string, error) {
	messages := append([]Message{{Role: "system", Content: system}}, history...)

	payload := OllamaRequest{
		Model:    "llama3.2",
		Messages: messages,
		Stream:   false,
	}

	body, err := json.Marshal(payload)
	if err != nil {
		return "", err
	}

	req, err := http.NewRequestWithContext(
		ctx, "POST",
		"http://localhost:11434/api/chat",
		bytes.NewReader(body),
	)
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 120 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result OllamaResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}

	return result.Message.Content, nil
}
