import { BrowserRouter,Routes, Route } from "react-router-dom";
import Window from "./components/Window";
import Register from "./components/Register";
import Login from "./components/Login";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/">
          <Route element={<PrivateRoute />}>
            <Route index element={<Window />} />
          </Route>          
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<Error />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
