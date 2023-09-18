
const Login = () => {
    return (
        <div className="container">
            <div className="reg-wrapper">
                <form action="" method="post">
                    <input type="email" id="email" name="email" placeholder="Email"/>
                    <br />
                    <br />
                    <input type="password" id="passwd" name="passwd" placeholder="Password"/>
                    <br />
                    <br />
                    <button type="submit">Login</button>
                </form>
            </div>
        </div>
    );
}

export default Login;