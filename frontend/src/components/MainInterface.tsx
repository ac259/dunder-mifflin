import { useState } from "react";
import Sidebar from "./Sidebar";
import ChatWindow from "./ChatWindow";

export default function MainInterface() {
  return (
    <div className="flex h-screen bg-[#0A0A0A] text-green-400 font-mono">
      {/* Sidebar */}
      <Sidebar />

      {/* Chat Window */}
      <div className="flex-1 flex flex-col items-center justify-center p-6">
        <ChatWindow />
      </div>
    </div>
  );
}
