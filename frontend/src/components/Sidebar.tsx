import { useState } from "react";
import { ChevronRightIcon, ChevronLeftIcon } from "@heroicons/react/24/outline";

const agents = [
  { id: "schrute_bot", name: "SchruteBot", status: "[ON]" },
  { id: "jimster", name: "Jimster", status: "[ON]" },
];

export default function Sidebar({ onSelectAgent }: { onSelectAgent: (id: string) => void }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div
      className={`h-screen bg-[#1C1C1C] text-green-400 font-mono border-r border-gray-600
        flex flex-col relative transition-all duration-500 ease-in-out
        ${collapsed ? "w-16" : "w-72"}`}
    >
      {/* Collapse Button (Smoothly Positioned) */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute top-1/2 -right-5 transform -translate-y-1/2 bg-green-500 text-black p-1 rounded-full transition-all duration-500 ease-in-out"
      >
        {collapsed ? <ChevronRightIcon className="h-5 w-5" /> : <ChevronLeftIcon className="h-5 w-5" />}
      </button>

      {/* Sidebar Content - Fade Animation */}
      <div className={`flex flex-col transition-opacity duration-500 ${collapsed ? "opacity-0" : "opacity-100"}`}>
        {/* Sidebar Header */}
        <div className="text-center text-lg font-bold py-4 border-b border-gray-600">
          DUNDER MIFFLIN AI SYSTEM
        </div>

        {/* Agent Selection */}
        <ul className="mt-4 space-y-2">
          {agents.map((agent) => (
            <li
              key={agent.id}
              className="cursor-pointer px-3 py-2 rounded hover:bg-green-500 flex justify-between transition-all duration-300"
              onClick={() => onSelectAgent(agent.id)}
            >
              {agent.name} <span>{agent.status}</span>
            </li>
          ))}
        </ul>

        {/* Add New Agent */}
        <div className="mt-6">
          <p className="cursor-pointer px-3 py-2 rounded hover:bg-green-500 transition-all duration-300">
            [New Agent] <span>[Add]</span>
          </p>
        </div>
      </div>
    </div>
  );
}
