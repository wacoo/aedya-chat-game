import { useEffect, useRef, useState } from "react";
import Chat from "./Chat";
import './ChatBox.css';
import { useDispatch, useSelector } from "react-redux";
import { fetchChats, sendChat } from "../redux/chat/chatSlice";
import { render } from "@testing-library/react";

const ChatBox = () => {

    const dispatch = useDispatch();
    const chats = useSelector((state) => state.chat.chatList.chats) ?? [];
    const [message, setMessage] = useState({
        sent_from: '',
        sent_to: '',
        msg: ''
    });
    const [from, setFrom] = useState('wabaham9@gmail.com');
    const [to, setTo] = useState('albert@gmail.com');
    const bottomRef = useRef(null);

    useEffect(() => {
        dispatch(fetchChats());
    }, [dispatch]);

    useEffect(() => {
        bottomRef.current?.scrollIntoView();
    }, [chats]);

    const handleClick = () => {
        dispatch(sendChat(message)).then(() => {
            dispatch(fetchChats());
            setMessage((prev) => ({ ...prev, msg: '' }));
        });
    }
    
    return (
        <>
            <div className="box">
                {chats.map((chat) => (
                    <Chat chat={chat} key={chat.id} />
                ))}
                <div className="bottom" ref={bottomRef}></div>
            </div>
            <div className="input-box">
                <input type="text" placeholder="Say hi ..." value={message.msg} onChange={(e) => {setMessage({sent_from: from, sent_to: to, msg: e.target.value})}}/>
                <button type="button" onClick={() => handleClick()}>Send</button>
            </div>
        </>        
    );
}

export default ChatBox;