import React, { useState, useEffect } from 'react';
import './App.css';

function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [voices, setVoices] = useState([]);

    useEffect(() => {
        const handleVoicesChanged = () => {
            console.log(speechSynthesis.getVoices());
            setVoices(speechSynthesis.getVoices());
        };

        speechSynthesis.onvoiceschanged = handleVoicesChanged;

        // Initial load of voices
        handleVoicesChanged();

        return () => {
            speechSynthesis.onvoiceschanged = null; // Cleanup
        };
    }, []);

    const speech = (text) => {
        if (!text) return;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = voices[2]; // Choose a specific voice
        speechSynthesis.speak(utterance);
    };

    const formatMessage = (msg) => {
        // Check if the message is a heading
        if (msg.startsWith('**') && msg.endsWith('**')) {
            const heading = msg.slice(2, -2); // Remove the asterisks
            return <strong key={msg}>{heading}</strong>; // Return bold heading
        }
        return msg; // Return the message as is
    };

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages((prevMessages) => [...prevMessages, userMessage]);

        setLoading(true);
        setInput("");

        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: input }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const aiMessage = { role: 'ai', content: data.response };
            setMessages((prevMessages) => [...prevMessages, aiMessage]);
            speech(data.response); // Speak the AI response
        } catch (error) {
            console.error('Error fetching AI response:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <strong><h1>AI TUTOR</h1></strong>
            <div className="messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.role}`}>
                        <strong>{msg.role === 'user' ? 'You' : 'AI'}:</strong>
                        <pre>
                            <button className='speech-icon' onClick={() => speech(msg.content)} aria-label="Speak message">
                                🔊
                            </button>
                            {formatMessage(msg.content)} {/* Format the message here */}
                        </pre>
                    </div>
                ))}
                {loading && (
                    <div className="message ai">
                        <strong>AI:</strong>
                        <pre>Loading...</pre>
                    </div>
                )}
            </div>
            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Type your message..."
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
}

export default ChatApp;
