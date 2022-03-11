import {useContext, useEffect, useState} from 'react'
import "./styles.css"
import io from "socket.io-client"

let endPoint = "http://192.168.68.121:8080"
let socket = io(endPoint, {transports: ["websocket", "polling", "flashsocket"]})

const Modules = () => {
    const [power, setPower] = useState(false)
    const [angle, setAngle] = useState(0)

    useEffect(() => {
        socket.emit("power", power)
        socket.emit("servo", angle)
    },[power, angle])

    return (
        <div className="container">
            <button onClick={() => setPower(!power)}>{power ? "TURN OFF" : "TURN ON"}</button>
        <div className="servo">
            <button onClick={() => setAngle(100)}>LEFT</button>
            <button onClick={() => setAngle(200)}>RIGHT</button>
        </div>
        </div>
    )
}

export default Modules;

