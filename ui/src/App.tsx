import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [query, setQuery] = useState("");
  const [ragResult, setRagResult] = useState("");
  const [agentResult, setAgentResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setRagResult("");
    setAgentResult("");
    try {
      const response = await axios.post("http://localhost:8000/query", { query });
      setRagResult(response.data.rag);
      setAgentResult(response.data.agent);
    } catch (err) {
      setRagResult("Error retrieving data");
      setAgentResult("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center p-6 gap-4">
      <h1 className="text-3xl font-bold">LLM Research Assistant</h1>
      <textarea
        className="w-full max-w-2xl p-3 border rounded"
        rows={4}
        placeholder="Ask about recent LLM research..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Loading..." : "Submit"}
      </button>
      <div className="w-full max-w-2xl mt-4">
        <h2 className="text-xl font-semibold">RAG Response</h2>
        <pre className="bg-gray-100 p-3 rounded whitespace-pre-wrap">{ragResult}</pre>
        <h2 className="text-xl font-semibold mt-4">Agent Response</h2>
        <pre className="bg-gray-100 p-3 rounded whitespace-pre-wrap">{agentResult}</pre>
      </div>
    </main>
  );
}
