import { useState, useRef, useEffect } from "react";
import axios from "axios";


function App() {

  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages]);

  const sendMessage = async () => {
    if (!query.trim()) return;
    const updatedMessages = [
      ...messages,
      {
        role: "user",
        content: query
      }
    ];
    setMessages(updatedMessages);
    setLoading(true);
    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          query: query,
          chat_history: updatedMessages
        }
      );

      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
        route: response.data.route
      };

      setMessages([
        ...updatedMessages,
        assistantMessage
      ]);

    } catch (error) {

      console.error(error);
      setMessages([
        ...updatedMessages,
        {
          role: "assistant",
          content:
            "Error connecting to backend."
        }
      ]);
    }

    setLoading(false);
    setQuery("");
  };


  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };


  return (
    <div className="h-screen bg-[#0f172a] flex justify-center items-center p-4">
      <div className="w-full max-w-5xl h-full bg-[#111827] rounded-3xl shadow-2xl flex flex-col overflow-hidden">
        <div className="p-6 border-b border-gray-800 bg-[#0b1220]">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-semibold text-white tracking-tight">
                HR AI Assistant
              </h1>
              <p className="text-gray-400 mt-1 text-sm">
                Your HR workspace assistant
              </p>
            </div>
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-6 space-y-6">

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.role === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] px-5 py-4 rounded-2xl shadow-md ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-800 text-gray-100"
                }`}
              >
                <div className="text-sm font-semibold mb-2 opacity-80">
                  {msg.role === "user"
                    ? "You"
                    : "Assistant"}

                </div>
                <div className="whitespace-pre-wrap leading-relaxed">
                  {msg.content}
                </div>
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 text-white px-5 py-4 rounded-2xl">
                Thinking...
              </div>
            </div>
          )}
          <div ref={bottomRef}></div>
        </div>
        <div className="p-4 border-t border-gray-700 bg-[#111827]">
          <div className="flex gap-3">
            <input
              type="text"
              value={query}
              placeholder="Ask HR related questions..."
              onChange={(e) =>
                setQuery(e.target.value)
              }
              onKeyDown={handleKeyDown}
              className="flex-1 bg-gray-800 text-white border border-gray-700 rounded-2xl px-5 py-4 outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={sendMessage}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 rounded-2xl transition font-medium"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
export default App;
