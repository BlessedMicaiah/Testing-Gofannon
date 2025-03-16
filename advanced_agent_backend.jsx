import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Loader } from "lucide-react";
import { motion } from "framer-motion";

export default function ResearchSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchResearch = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error("Error fetching research papers:", error);
    }
    setLoading(false);
  };

  return (
    <div className="p-8 max-w-3xl mx-auto min-h-screen flex flex-col items-center bg-gradient-to-r from-blue-50 to-gray-100">
      <motion.h1 
        className="text-3xl font-extrabold mb-6 text-gray-800" 
        initial={{ opacity: 0, y: -20 }} 
        animate={{ opacity: 1, y: 0 }}
      >
        Research Paper Search
      </motion.h1>
      <div className="w-full flex gap-3 mb-6">
        <Input 
          value={query} 
          onChange={(e) => setQuery(e.target.value)} 
          placeholder="Enter keyword or sentence..." 
          className="flex-1 p-4 rounded-lg border border-gray-300 shadow-md focus:ring focus:ring-blue-300" 
        />
        <Button onClick={searchResearch} disabled={loading} className="p-4 bg-blue-600 text-white rounded-lg shadow-lg hover:bg-blue-700 transition-all">
          {loading ? <Loader className="animate-spin" size={20} /> : "Search"}
        </Button>
      </div>
      <div className="w-full space-y-6">
        {results.map((paper, index) => (
          <motion.div 
            key={index} 
            initial={{ opacity: 0, y: 10 }} 
            animate={{ opacity: 1, y: 0 }}
          >
            <Card className="p-5 rounded-lg shadow-lg border border-gray-200 bg-white transition-transform transform hover:scale-105">
              <CardContent>
                <h2 className="text-lg font-semibold text-gray-900">{paper.title}</h2>
                <p className="text-sm text-gray-600 mt-2">{paper.summary}</p>
                <a 
                  href={paper.link} 
                  className="inline-block mt-3 text-blue-500 hover:text-blue-700 font-medium transition-all" 
                  target="_blank" 
                  rel="noopener noreferrer"
                >
                  Read More →
                </a>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
