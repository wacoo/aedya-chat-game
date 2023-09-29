import { useEffect, useRef, useState } from "react";
import Chat from "./Chat";
import './ChatBox.css';
import { useDispatch, useSelector } from "react-redux";
import { fetchChats, sendChat } from "../redux/chat/chatSlice";
import { render } from "@testing-library/react";
import { fetchGame, newGame, updateChatCount, updateEvaluation, updateScore  } from "../redux/games/gamesSlice";
import { fetchUser } from "../redux/user/userSlice";

const ChatBox = () => {

    const dispatch = useDispatch();
    const chats = useSelector((state) => state.chat.chatList.chats) ?? [];
    const game = useSelector((state) => state.games.data);
    const chatCount = useSelector((state) => state.games.chatCount);
    const usResult = useSelector((state) => state.games.updateScoreResult);
    const user = useSelector((state) => state.user.userData);
    const [message, setMessage] = useState({
        sent_from: '',
        sent_to: '',
        msg: ''
    });
    const bottomRef = useRef(null);
    const token = JSON.parse(localStorage.getItem('token'));
    const [cls, setCls] = useState('');
    const [gameStatusClass, setGameStatusClass] = useState('input-box');
    console.log(token.email);

    useEffect(() => {
        dispatch(fetchGame({email: token.email}));
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView();
    }, [chats]);

    useEffect(() => {
        dispatch(fetchUser({email: token.email}))
    }, [dispatch])

    useEffect(() => {
        console.log(usResult);
    }, [usResult]);

    useEffect(() => {
        console.log(chatCount.count);
        if (chatCount.count >= 5) {
            localStorage.setItem('gameStatusClass', 'input-box game-done');
            setGameStatusClass(localStorage.getItem('gameStatusClass'));
            setCls('promote-wrapper');
        }
    }, [chatCount]);

    useEffect(() => {
        if (game?.opponent) {
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

    const handleChange = (e) => {
        setMessage({sent_from: token.email, sent_to: game.opponent, msg: e.target.value});
        const doneCLass = localStorage.getItem('gameStatusClass');
        if (doneCLass) {
            setGameStatusClass(localStorage.getItem('gameStatusClass'));
            setCls('promote-wrapper');
        }
    }

    const handleThumbsup = (e) => {
        e.preventDefault();
        dispatch(updateEvaluation({'game_id': game.game_id, 'email': token.email, 'value': 1}));
        dispatch(updateScore({game_id: game.game_id}));
        setCls('hide');
    }

    const handleThumbsdown = (e) => {
        e.preventDefault();
        dispatch(updateEvaluation({'game_id': game.game_id, 'email': token.email, 'value': 0}));
        setCls('hide');
    }

    return (
        <>
            <dialog className={cls}>
                <div className="modal-wrapper">
                    <h2>How do evaluate<br />your opponent?</h2>
                    <div className="promote">
                        <a className=".disabled-button" href="" onClick={(e) => handleThumbsup(e)}><i className="fa-solid fa-thumbs-up"></i></a>
                        <a className=".disabled-button" href="" onClick={(e) => handleThumbsdown(e)}><i className="fa-solid fa-thumbs-down"></i></a>
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
                    {game?.error ? <h2>{game.error}</h2> : null}
                    <h2>{token?.email ? token.email.split('@')[0].toUpperCase() : 'PLAYER 1'} VS {game?.opponent ? game.opponent.split('@')[0].toUpperCase() : 'PLAYER 2'}</h2>
                    <h2>SCORE: {user.total_score}</h2>
                    <div className={gameStatusClass}>
                        <input type="text" placeholder="Say hi ..." value={message.msg} onChange={(e) => {handleChange(e)}}/>
                        <button type="button" onClick={() => handleClick()}>Send</button>
                    </div> 
            </div>
                               
        </div>
        </>        
    );
}

export default ChatBox;