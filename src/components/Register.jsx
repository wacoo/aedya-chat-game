
import { useEffect, useState } from 'react';
import './Register.css';
import { useDispatch, useSelector } from 'react-redux';
import { registerUser } from '../redux/user/userSlice';
import NavBar from './NavBar';

const Register = () => {
    const countries = [
        'Armenia',
        'Australia',
        'Austria',
        'Azerbaijan',
        'Bahamas',
        'Bahrain',
        'Bangladesh',
        'Barbados',
        'Bolivia',
        'Bosnia and Herzegovina',
        'Botswana',
        'Jamaica',
        'Japan',
        'Jordan',
        'Kazakhstan',
        'Kenya',
        'Kiribati',
        'Korea, North',
        'Korea, South',
        'Kuwait',
        'Kyrgyzstan',
        'Laos',
        'Latvia',
        'Lebanon',
        'Luxembourg',
        'Madagascar',
        'Malawi',
        'Malaysia',
        'Maldives',
        'Mali',
        'Syria',
        'Taiwan',
        'Tajikistan',
        'Tanzania',
        'Thailand',
        'Togo',
        'Tonga',
        'Trinidad and Tobago',
        'Tunisia',
        'Turkey',
        'Turkmenistan',
        'Tuvalu',
        'Uganda',
        'Ukraine',
        'United Arab Emirates'];
                               
    const dispatch = useDispatch();
    const successMsg = useSelector((state) => state.user.message);
    const [fname, setFname] = useState('');
    const [lname, setLname] = useState('');
    const [email, setEmail] = useState('');
    const [country, setCountry] = useState('');
    const [score, setScore] = useState('');
    const [password, setPassword] = useState('');
    const [msgClass, setMsgClass] = useState('neutral');

    const handleSubmit = (e) => {
        e.preventDefault();
        const userData = {
            fname, lname, email, country, score, password,
        }
        dispatch(registerUser(userData));    
    }

    useEffect(() => {
        console.log(successMsg);
    }, [successMsg]);
    
    const handleMsgStyle = (msg) => {
        if (msg.message) {
            setMsgClass('success');
        } else {
            setMsgClass('failure');
        }

        setTimeout(() => {
            setMsgClass('neutral');
        }, 5000);
        
    }

    useEffect(() => {
        handleMsgStyle(successMsg);
    }, [successMsg]);

    return (
        <>
            <NavBar />
            <div className="container">
                <div className="reg-wrapper">
                    <form action="" method="post" onSubmit={((e) => handleSubmit(e))}>
                        <input type="text" id="fname" name="fname" onChange={(e) => setFname(e.target.value)} placeholder="First name"/>
                        <br />
                        <br />
                        <input type="text" id="lname" name="lname" onChange={(e) => setLname(e.target.value)} placeholder="Last name"/>
                        <br />
                        <br />
                        <input type="email" id="email" name="email" onChange={(e) => setEmail(e.target.value)} placeholder="Email"/>
                        <br />
                        <br />
                        <select name="country" id="country" onChange={(e) => setCountry(e.target.value)} placeholder="Country">
                            { countries.map((country) => (
                                <option value={country}>{country}</option>
                            ))}
                        </select>
                        <br />
                        <br />
                        <input type="number" id="score" onChange={(e) => setScore(e.target.value)} name="score" placeholder="Score"/>
                        <br />
                        <br />
                        <input type="password" name="passwd" onChange={(e) => setPassword(e.target.value)} id="passwd" />
                        <br />
                        <br />
                        <button type="submit">Register</button>
                        <br />
                        <small className={`${msgClass}`}>{successMsg.message ? successMsg.message : successMsg.error}</small>
                    </form>
                </div>
            </div>
        </>
    );
}

export default Register;