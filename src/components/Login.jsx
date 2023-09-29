import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from 'react-router-dom';
import { authenticateUser } from "../redux/user/userSlice";
import NavBar from "./NavBar";

const Login = () => {
    const token = useSelector((state) => state.user.token);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [newGClass, setNewGClass] = ['hidden'];
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const localToken = JSON.parse(localStorage.getItem('token'));

    useEffect(() => {
        if(localToken?.token) {
            console.log(localToken)
            navigate('/');
        }
    }, [localToken])

    const handleSubmit = (e) => {
        e.preventDefault();
        const credential = { email, password };
        dispatch(authenticateUser(credential));
    }

    return (
        <>
            <NavBar cls = "hidden" />
            <div className="container">
                <div className="reg-wrapper">
                    <form action="" method="post" onSubmit={(e) => {handleSubmit(e)}}>
                        <input type="email" id="email" onChange={(e) => setEmail(e.target.value)} placeholder="Email"/>
                        <br />
                        <br />
                        <input type="password" id="passwd" onChange={((e) => setPassword(e.target.value))} placeholder="Password"/>
                        <br />
                        <br />
                        <button type="submit">Login</button>
                    </form>
                </div>
            </div>
        </>
    );
}

export default Login;