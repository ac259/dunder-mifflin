import ChatHeader from "./ChatHeader";

const ChatWindow = () => {
  return (
    <div className="w-3/4 h-[60vh] bg-[#0A0A0A] shadow-lg border-2 border-gray-600 flex flex-col">
      {/* Chat Header */}
      <ChatHeader />

      {/* Chat Messages */}
      <div className="flex-1 p-4 overflow-y-auto text-green-400 font-mono">
        <p>&gt; Welcome. What would you like to do?</p>
        <p>&gt; Add Task: "Prepare Monthly Report"</p>
        <p>&gt; Task Added.</p>
      </div>

      {/* Chat Input */}
      <div className="border-t-2 border-gray-600 p-2">
        <input
          type="text"
          placeholder="Type here..."
          className="w-full bg-transparent text-green-400 font-mono border-none outline-none placeholder-gray-500"
        />
      </div>
    </div>
  );
};

export default ChatWindow;
