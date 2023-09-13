import Chat from "./Chat";
import './ChatBox.css';

const ChatBox = () => {

    const chats = [
        {
            direction: 'incoming',
            msg: 'Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?',
        },
        {
            direction: 'outgoing',
            msg: 'Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?',
        },
        {
            direction: 'incoming',
            msg: 'Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?',
        },
        {
            direction: 'outgoing',
            msg: 'Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?Hi, how are you? I fine How is life?',
        }
    ];

    return (
        <div className="box">
            {chats.map((chat) => (
                <Chat chat={chat}/>
            ))
            }
            <div className="input-box">
                <input type="text" placeholder="Say hi ..."/>
                <button type="button">Send</button>
            </div>
        </div>
    );
}

export default ChatBox;