import { Navigate, Outlet } from "react-router-dom";

const PrivateRoute = () => {
    const token = JSON.parse(localStorage.getItem('token'));

    return (
        token?.token ? <Outlet /> : <Navigate to="/login" />
    );
}

export default PrivateRoute;