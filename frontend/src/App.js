import { useState } from 'react';
import Login from './Login';
import Register from './Register';
import Attendance from './Attendance';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  if (!loggedIn) return <Login onLogin={setLoggedIn} />;

  return (
    <div>
      <h1>Face Recognition Attendance System</h1>
      <Register />
      <Attendance />
      <p>Made with ❤️ from Sohel</p>
    </div>
  );
}

export default App;
