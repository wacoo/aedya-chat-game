import { useEffect, useRef, useState } from "react";
import Chat from "./Chat";
import './ChatBox.css';
import { useDispatch, useSelector } from "react-redux";
import { fetchChats, sendChat } from "../redux/chat/chatSlice";
import { render } from "@testing-library/react";
import { fetchGame, newGame, updateChatCount  } from "../redux/games/gamesSlice";

const ChatBox = () => {

    const dispatch = useDispatch();
    const chats = useSelector((state) => state.chat.chatList.chats) ?? [];
    const game = useSelector((state) => state.games.data);
    const chatCount = useSelector((state) => state.games.chatCount);
    const [message, setMessage] = useState({
        sent_from: '',
        sent_to: '',
        msg: ''
    });
    const bottomRef = useRef(null);
    const token = JSON.parse(localStorage.getItem('token'));
    const [cls, setCls] = useState('');
    const [gameStatusClass, setGameStatusClass] = useState('input-box');
;    // const opponent = JSON.parse(localStorage.getItem('opponent'));

    // console.log(opponent);
    console.log(token.email);

    useEffect(() => {
        dispatch(fetchGame({email: token.email}))
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView();
    }, [chats]);

    useEffect(() => {
        console.log(chatCount.count);
        if (chatCount.count > 8) {
            setGameStatusClass('input-box game-done');
            setCls('promote-wrapper');
        }
    }, [chatCount]);

    useEffect(() => {
        if (game?.opponent) {
            // localStorage.setItem('opponent', game);
            console.log(token.email, game.opponent);
            dispatch(fetchChats({ email1: token.email, email2: game.opponent }));
        }
        console.log(game);
    }, [game]);

    const handleClick = async () => {
        const updatedMessage = {
            sent_from: token.email,
            sent_to: game.opponent,
            msg: message.msg
        };
        await dispatch(sendChat(updatedMessage));
        dispatch(fetchChats({ email1: token.email, email2: game.opponent }));
        setMessage((prev) => ({ ...prev, msg: '' }));
        dispatch(updateChatCount({game_id: game.game_id}))
    }

    const handleClose = (e) => {
        e.preventDefault();
        setCls('hide');
    }
    
    return (
        <>
            <dialog className={cls}>
                <div>
                    <h2>How do evaluate your opponent? <span className="times"><a href="" onClick={(e) => handleClose(e)}>&times;</a></span></h2>
                    <div className="promote">
                        <a className=".disabled-button" href=""><i class="fa-solid fa-thumbs-up"></i></a>
                        <a className=".disabled-button" href=""><i class="fa-solid fa-thumbs-down"></i></a>
                    </div>
                </div>
            </dialog>
            <div className="box">
                {chats.map((chat) => (
                    <Chat chat={chat} key={chat.id} />
                ))}
                <div className="bottom" ref={bottomRef}></div>
            </div>
            <div className="wrapper">
                <div className="input-wrapper">
                    <h2>{token?.email ? token.email.split('@')[0] : 'player 1'} vs {game?.opponent ? game.opponent.split('@')[0] : 'player 2'}</h2>
                    <div className={gameStatusClass}>
                        <input type="text" placeholder="Say hi ..." value={message.msg} onChange={(e) => {setMessage({sent_from: token.email, sent_to: game.opponent, msg: e.target.value})}}/>
                        <button type="button" onClick={() => handleClick()}>Send</button>
                    </div> 
            </div>
                               
        </div>
        </>        
    );
}

export default ChatBox;