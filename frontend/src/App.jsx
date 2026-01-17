import { useState } from "react";
import Login from "./auth/Login";

function App() {
  const [loggedIn, setLoggedIn] = useState(
    Boolean(localStorage.getItem("token"))
  );

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)} />;
  }

  return <h1>Logged in</h1>;
}

export default App;
