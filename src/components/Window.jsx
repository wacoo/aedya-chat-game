import { useEffect, useRef } from "react";
import ChatBox from "./ChatBox";
import SideBar from "./SideBar";
import './Window.css';
import NavBar from "./NavBar";
import { useNavigate } from 'react-router-dom';

const Window = () => {
    return (
        <>
            <NavBar />
            <div className="container">
                {/* <SideBar /> */}
                <div className="chatbox-wrapper">
                    <ChatBox />
                </div>
            </div>
        </>
    );
}

export default Window;