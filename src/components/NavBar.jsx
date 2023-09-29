import { NavLink, useNavigate } from 'react-router-dom';
import './NavBar.css';
import { useDispatch } from 'react-redux';
import { newGame } from '../redux/games/gamesSlice';
import Logo from '../img/logo.png';

const NavBar = (props) => {
    const { cls } = props;
    const dispatch = useDispatch();
    const token = JSON.parse(localStorage.getItem('token'));
    const navigate = useNavigate();
    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        navigate('/login');
    }

    const handleNewGame = (event) => {
        event.preventDefault();
        console.log(token);
        dispatch(newGame({'player1': token.email, 'country': token.country}));
        console.log('new game2');
        localStorage.removeItem('gameStatusClass')
    }

    return (
        <header className="header">
            <div className="logo">
                <img src={Logo} alt="Logo" />
            </div>
            <div className="menu">
                <ul>
                    <li><NavLink exact="true" to="/">Home</NavLink> </li>
                    <li><NavLink  className={cls} to="" onClick={(e) => handleNewGame(e)}>New Game</NavLink></li>
                    <li><NavLink to="/register">Register</NavLink></li>
                    {
                        token ? <li><NavLink  to="/logout" onClick={(e) => handleLogout(e)}>Logout</NavLink> </li>: <li><NavLink  to="/login">Login</NavLink></li>
                    }
                    
                </ul>
            </div>
        </header>
    );
}

export default NavBar;