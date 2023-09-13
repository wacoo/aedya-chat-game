import ChatBox from "./ChatBox";
import SideBar from "./SideBar";
import './Window.css';

const Window = () => {
    return (
        <div className="container">
            <SideBar />
            <div className="chatbox-wrapper">
                <ChatBox />
            </div>
        </div>
    );
}

export default Window;