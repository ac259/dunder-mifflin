import { useState } from "react";
import Sidebar from "./components/Sidebar";

export default function App() {
  const [selectedAgent, setSelectedAgent] = useState("schrute_bot");

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar selectedAgent={selectedAgent} onSelectAgent={setSelectedAgent} />

      {/* Chat Area */}
      <div className="flex-1 flex items-center justify-center bg-gray-100">
        <h1 className="text-2xl font-semibold text-gray-800">
          Chat with {selectedAgent.replace("_", " ")}
        </h1>
      </div>
    </div>
  );
}
