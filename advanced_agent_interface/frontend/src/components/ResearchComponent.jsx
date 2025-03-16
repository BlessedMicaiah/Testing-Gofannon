import React, { useState } from "react";
import { Card, CardContent } from "./ui/card.jsx";
import { Input } from "./ui/input.jsx";
import { Button } from "./ui/button.jsx";

export default function ResearchComponent() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchResearch = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("Error fetching research papers:", error);
    }
    setLoading(false);
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Research Paper Search</h2>
      <div className="flex gap-3 mb-6">
        <Input 
          value={query} 
          onChange={(e) => setQuery(e.target.value)} 
          placeholder="Enter research topic..." 
          className="flex-1" 
        />
        <Button onClick={searchResearch} disabled={loading || !query.trim()}>
          {loading ? "Searching..." : "Search"}
        </Button>
      </div>
      <div className="space-y-4">
        {results.length > 0 ? (
          results.map((paper, index) => (
            <Card key={index} className="bg-white">
              <CardContent className="p-4">
                <h3 className="text-lg font-semibold">{paper.title}</h3>
                <p className="text-sm text-gray-600 mt-2">{paper.summary}</p>
                {paper.link && (
                  <a 
                    href={paper.link} 
                    className="text-blue-500 hover:text-blue-700 mt-2 inline-block" 
                    target="_blank" 
                    rel="noopener noreferrer"
                  >
                    Read More →
                  </a>
                )}
              </CardContent>
            </Card>
          ))
        ) : (
          query.trim() && !loading && <p>No results found. Try a different query.</p>
        )}
      </div>
    </div>
  );
}
