import React, { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "./src/components/ui/card.jsx";
import { Input } from "./src/components/ui/input.jsx";
import { Button } from "./src/components/ui/button.jsx";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./src/components/ui/tabs.jsx";
import { Textarea } from "./src/components/ui/textarea.jsx";
import { Loader, FileText, Plus, LayoutDashboard, Search, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import ResearchSearch from "./advanced_agent_backend.jsx";

export default function ProjectsUI() {
  const [projects, setProjects] = useState([]);
  const [activeProject, setActiveProject] = useState(null);
  const [newProjectName, setNewProjectName] = useState("");
  const [query, setQuery] = useState("");
  const [agentResponse, setAgentResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");

  // Mock project data for demo purposes
  useEffect(() => {
    const demoProjects = [
      { id: 1, name: "Quarterly Report", slides: 12, lastEdited: new Date().toLocaleDateString() },
      { id: 2, name: "Product Pitch", slides: 8, lastEdited: new Date().toLocaleDateString() },
    ];
    setProjects(demoProjects);
  }, []);

  const createNewProject = () => {
    if (newProjectName.trim()) {
      const newProject = {
        id: Date.now(),
        name: newProjectName,
        slides: 0,
        lastEdited: new Date().toLocaleDateString()
      };
      setProjects([...projects, newProject]);
      setNewProjectName("");
    }
  };

  const runAgentQuery = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setAgentResponse("");
    
    try {
      const response = await fetch("http://localhost:5000/agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      
      const data = await response.json();
      
      if (data.error) {
        setAgentResponse(`Error: ${data.error}`);
      } else {
        setAgentResponse(data.response);
      }
    } catch (error) {
      console.error("Error connecting to agent:", error);
      setAgentResponse("Error connecting to the agent. Please make sure the Python backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-purple-50">
      <div className="container mx-auto p-6">
        <div className="flex justify-between items-center mb-8">
          <motion.h1 
            className="text-3xl font-bold text-gray-800"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            Paron Presentations
          </motion.h1>
          <div className="flex items-center gap-3">
            <Input
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
              placeholder="New presentation name..."
              className="w-60"
            />
            <Button 
              onClick={createNewProject}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <Plus className="mr-2 h-4 w-4" /> Create New
            </Button>
          </div>
        </div>

        <Tabs defaultValue="dashboard" value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="mb-6">
            <TabsTrigger value="dashboard">
              <LayoutDashboard className="mr-2 h-4 w-4" /> Dashboard
            </TabsTrigger>
            <TabsTrigger value="research">
              <Search className="mr-2 h-4 w-4" /> Research
            </TabsTrigger>
            <TabsTrigger value="assistant">
              <Sparkles className="mr-2 h-4 w-4" /> AI Assistant
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {projects.map((project) => (
                <motion.div 
                  key={project.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3 }}
                >
                  <Card className="cursor-pointer hover:shadow-lg transition-all">
                    <CardHeader>
                      <CardTitle>{project.name}</CardTitle>
                      <CardDescription>
                        {project.slides} slides • Last edited: {project.lastEdited}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="flex justify-center items-center h-32 bg-gray-50">
                      <FileText size={48} className="text-gray-400" />
                    </CardContent>
                    <CardFooter className="bg-gray-50 border-t border-gray-100 justify-between">
                      <span className="text-sm text-gray-500">Created with Paron</span>
                      <Button variant="outline" size="sm">Open</Button>
                    </CardFooter>
                  </Card>
                </motion.div>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="research">
            <ResearchSearch />
          </TabsContent>

          <TabsContent value="assistant">
            <Card className="mb-6">
              <CardHeader>
                <CardTitle>AI Presentation Assistant</CardTitle>
                <CardDescription>Ask questions or get help with your presentation</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Example: 'Create an outline for a product launch presentation' or 'Suggest visuals for my financial data'"
                    className="min-h-32"
                  />
                  <Button 
                    onClick={runAgentQuery} 
                    disabled={loading || !query.trim()}
                    className="w-full bg-indigo-600 hover:bg-indigo-700"
                  >
                    {loading ? <Loader className="mr-2 h-4 w-4 animate-spin" /> : <Sparkles className="mr-2 h-4 w-4" />}
                    Generate Response
                  </Button>
                </div>
              </CardContent>
            </Card>

            <AnimatePresence>
              {agentResponse && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 20 }}
                >
                  <Card>
                    <CardHeader>
                      <CardTitle>AI Response</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="whitespace-pre-line bg-gray-50 p-4 rounded-md border border-gray-200">
                        {agentResponse}
                      </div>
                    </CardContent>
                    <CardFooter className="justify-end">
                      <Button variant="outline" onClick={() => navigator.clipboard.writeText(agentResponse)}>
                        Copy to Clipboard
                      </Button>
                    </CardFooter>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}