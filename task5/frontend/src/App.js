import React, { useState, useEffect } from "react";
import Chat from "./components/Chat";

function App() {
  return (
    <div className="App">
      <h1>WebSocket Chat</h1>
      <Chat />
    </div>
  );
}

export default App;
