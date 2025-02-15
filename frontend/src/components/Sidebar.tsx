import React from "react";
import { HomeIcon, UserGroupIcon, ChatBubbleLeftIcon } from "@heroicons/react/24/outline"; // Import icons

const agents = [
  { id: "schrute_bot", name: "Dwight Schrute", icon: UserGroupIcon },
  { id: "jimster", name: "Jim Halpert", icon: HomeIcon }
];

interface SidebarProps {
  selectedAgent: string;
  onSelectAgent: (agentId: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ selectedAgent, onSelectAgent }) => {
  return (
    <div className="w-64 h-screen bg-gray-900 text-white flex flex-col p-4">
      {/* Sidebar Header */}
      <h2 className="text-2xl font-bold mb-6">Dunder Mifflin AI</h2>

      {/* Sidebar List */}
      <ul className="space-y-2">
        {agents.map((agent) => {
          const Icon = agent.icon;
          return (
            <li
              key={agent.id}
              className={`flex items-center space-x-3 p-3 rounded-lg cursor-pointer transition ${
                selectedAgent === agent.id
                  ? "bg-gray-700 text-white"
                  : "text-gray-400 hover:bg-gray-700 hover:text-white"
              }`}
              onClick={() => onSelectAgent(agent.id)}
            >
              <Icon className="h-5 w-5" />
              <span>{agent.name}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default Sidebar;
