import { useState } from "react";
import "./App.css";

//import { socket, SocketContext } from "./context/socket";
import Modules from "./components/modules";

function App() {
  return (
    <div className="App">
      <Modules/>
    </div>
  );
}

export default App;
