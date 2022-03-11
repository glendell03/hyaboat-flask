import React from "react"
import io from "socket.io-client"

PORT = "http://192.168.68.121:3001"
export const socket = io(PORT, {transport: ["websocket"]})
export const SocketContext = React.createContext()
