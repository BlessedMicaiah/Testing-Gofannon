import React, { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs.jsx";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "./components/ui/card.jsx";
import { Input } from "./components/ui/input.jsx";
import { Button } from "./components/ui/button.jsx";
import { Textarea } from "./components/ui/textarea.jsx";
import ResearchComponent from "./components/ResearchComponent.jsx";

export default function App() {
  const [query, setQuery] = useState("");
  const [agentResponse, setAgentResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("agent");

  const runAgentQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setAgentResponse("");
    
    try {
      const response = await fetch("http://localhost:5000/api/agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      
      const data = await response.json();
      
      if (data.error) {
        setAgentResponse(`Error: ${data.error}`);
      } else {
        setAgentResponse(data.response || "No response from agent");
      }
    } catch (error) {
      console.error("Error connecting to agent:", error);
      setAgentResponse("Error connecting to the agent. Please make sure the Python backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Advanced AI Agent Interface</h1>
        <p className="text-slate-600 mt-1">
          Interact with your AI agent using natural language
        </p>
      </header>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="mb-6">
          <TabsTrigger value="agent">AI Agent</TabsTrigger>
          <TabsTrigger value="research">Research</TabsTrigger>
          <TabsTrigger value="tools">Available Tools</TabsTrigger>
        </TabsList>

        <TabsContent value="agent">
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Ask the AI Agent</CardTitle>
              <CardDescription>
                The agent can perform math operations, reasoning tasks, and search for academic papers
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <Textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Example: 'Calculate 25 + 17', 'Explain how rainbows work', or 'Find recent research papers about quantum computing'"
                  className="min-h-32"
                />
                <Button 
                  onClick={runAgentQuery} 
                  disabled={loading || !query.trim()}
                  className="w-full"
                >
                  {loading ? "Processing..." : "Submit Query"}
                </Button>
              </div>
            </CardContent>
          </Card>

          {agentResponse && (
            <Card>
              <CardHeader>
                <CardTitle>Agent Response</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-white p-4 rounded-md border border-slate-200 whitespace-pre-line">
                  {agentResponse}
                </div>
              </CardContent>
              <CardFooter className="justify-end">
                <Button variant="outline" onClick={() => navigator.clipboard.writeText(agentResponse)}>
                  Copy Response
                </Button>
              </CardFooter>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="research">
          <ResearchComponent />
        </TabsContent>

        <TabsContent value="tools">
          <Card>
            <CardHeader>
              <CardTitle>Available Tools</CardTitle>
              <CardDescription>The following tools are available through the agent</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-4 list-disc pl-5">
                <li>
                  <strong>Math Tools</strong>: Addition, Subtraction, Multiplication, Division, Exponents
                </li>
                <li>
                  <strong>Reasoning Tools</strong>: Sequential Chain-of-Thought reasoning
                </li>
                <li>
                  <strong>Knowledge Tools</strong>: ArXiv research paper search
                </li>
                <li>
                  <strong>Optional Tools</strong> (require API keys):
                  <ul className="list-disc pl-5 mt-2">
                    <li>OpenAI API for advanced reasoning</li>
                    <li>Google Search API for web search</li>
                  </ul>
                </li>
              </ul>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
