import { useState } from "react";
import Sidebar from "../components/Sidebar/Sidebar";
import "../styles/chatPage.css";

export default function ChatPage() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const [sessionId, setSessionId] = useState(
    localStorage.getItem("chatSession") || ""
  );

  const sendMessage = async () => {
    if (!message.trim()) return;

    const token = localStorage.getItem("token");

    const currentMessage = message;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: currentMessage,
      },
    ]);

    setMessage("");

    try {
      const response = await fetch(
        "http://localhost:8080/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            session_id: sessionId,
            message: currentMessage,
          }),
        }
      );

      const data = await response.json();

      setSessionId(data.session_id);

      localStorage.setItem(
        "chatSession",
        data.session_id
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
        },
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't reach the AI assistant.",
        },
      ]);
    }
  };

  const usePrompt = (prompt) => {
    setMessage(prompt);
  };

  return (
    <div className="layout">
      <Sidebar />

      <main className="chat-page">

        <div className="chat-header">
          <div>
            <h2>🤖 SkinMax AI Assistant</h2>
            <p>Online and ready to help</p>
          </div>

          <img
            src="https://i.pravatar.cc/40"
            alt="Profile"
            className="chat-avatar"
          />
        </div>

        {/* Landing Section */}
        <div className="chat-empty">

          <div className="bot-icon">
            🤖
          </div>

          <h1>
            Start Chat with Glow
          </h1>

          <p>
            Ask me about your skincare routine,
            latest scan, or weather-based care.
          </p>

        </div>

        {/* Messages appear below landing section */}
        {messages.length > 0 && (
          <div className="chat-messages">

            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.role}`}
              >
                {msg.content}
              </div>
            ))}

          </div>
        )}

        <div className="quick-prompts">

          <button
            onClick={() =>
              usePrompt(
                "Review my skincare routine"
              )
            }
          >
            📅 Review my routine
          </button>

          <button
            onClick={() =>
              usePrompt(
                "Explain my last scan"
              )
            }
          >
            🔍 Explain my last scan
          </button>

          <button
            onClick={() =>
              usePrompt(
                "Give me weather based skincare tips"
              )
            }
          >
            ☀️ Weather tips
          </button>

          <button
            onClick={() =>
              usePrompt(
                "I want to talk to a dermatologist"
              )
            }
          >
            👨‍⚕️ Talk to Dermatologist
          </button>

        </div>

        <div className="chat-input">

          <input
            type="text"
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder="Ask anything about your skin..."
          />

          <button
            onClick={sendMessage}
          >
            ➤
          </button>

        </div>

        <p className="chat-disclaimer">
          SkinMax AI can make mistakes.
          Consider consulting a professional
          for severe conditions.
        </p>

      </main>
    </div>
  );
}