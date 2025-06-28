import React, { useState } from "react";
import AudioFeed from "./AudioFeed";
import AuthPage from "./AuthPage";

function App() {
  const [user, setUser] = useState(null);

  return user ? (
    <AudioFeed user={user} />
  ) : (
    <AuthPage onAuth={setUser} />
  );
}

export default App;