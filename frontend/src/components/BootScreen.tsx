import { useState, useEffect } from "react";

export default function BootScreen({ onComplete }: { onComplete: () => void }) {
  const [lines, setLines] = useState<string[]>([]);

  useEffect(() => {
    const bootMessages = [
      "DUNDER MIFFLIN AI SYSTEM v1.0",
      "Initializing...",
      "Loading AI Modules...",
      "SchruteBot Online...",
      "Jimster Online...",
      "Welcome, User.",
      "System Ready."
    ];

    let index = 0;
    const interval = setInterval(() => {
      if (index < bootMessages.length) {
        setLines((prev) => [...prev, bootMessages[index]]);
        index++;
      } else {
        clearInterval(interval);
        setTimeout(onComplete, 1000); // Transition to main UI
      }
    }, 800);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div className="h-screen w-screen bg-black text-green-400 font-mono text-lg p-10 flex flex-col justify-center items-center">
      {lines.map((line, i) => (
        <p key={i} className="animate-fadeIn">{line}</p>
      ))}
    </div>
  );
}
