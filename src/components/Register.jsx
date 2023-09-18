
import './Register.css';

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
    return (
        <div className="container">
            <div className="reg-wrapper">
                <form action="" method="post">
                    <input type="text" id="fname" name="fname" placeholder="First name"/>
                    <br />
                    <br />
                    <input type="text" id="lname" name="lname" placeholder="Last name"/>
                    <br />
                    <br />
                    <input type="email" id="email" name="email" placeholder="Email"/>
                    <br />
                    <br />
                    <select name="country" id="country" placeholder="Country">
                        { countries.map((country) => (
                            <option value={country}>{country}</option>
                        ))}
                    </select>
                    <br />
                    <br />
                    <input type="number" id="score" name="score" placeholder="Score"/>
                    <br />
                    <br />
                    <input type="password" name="passwd" id="passwd" />
                    <br />
                    <br />
                    <button type="submit">Register</button>
                </form>
            </div>
        </div>
    );
}

export default Register;