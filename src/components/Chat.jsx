import './Chat.css';

const Chat = (props) => {
    const { chat } = props;
    return (
        <div className={chat.direction}>
            <p>{chat.msg}</p>
        </div>
    );
}

export default Chat;