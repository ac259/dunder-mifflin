import { useState } from "react";
import BootScreen from "./components/BootScreen";
import MainInterface from "./components/MainInterface";

export default function App() {
  const [bootComplete, setBootComplete] = useState(false);

  return (
    <div>
      {!bootComplete ? (
        <BootScreen onComplete={() => setBootComplete(true)} />
      ) : (
        <MainInterface />
      )}
    </div>
  );
}
