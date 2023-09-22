import { NavLink, useNavigate } from 'react-router-dom';
import './NavBar.css';

const NavBar = () => {
    const token = localStorage.getItem('token');
    const navigate = useNavigate();
    // console.log(token);
    const handleLogout = (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        navigate('/login');
    }

    return (
        <header className="header">
            <div className="logo">
                <img src="" alt="" />
            </div>
            <div className="menu">
                <ul>
                    <li><NavLink exact="true" to="/">Home</NavLink> </li>
                    <li>New Game</li>
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