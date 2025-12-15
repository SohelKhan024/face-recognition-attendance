import React, { useState } from 'react';
import Camera from './Camera';

function Register() {
  const [name, setName] = useState('');
  const [image, setImage] = useState(null);

  const submit = async () => {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('image', image);

    await fetch('http://localhost:5000/register', {
      method: 'POST',
      body: formData
    });
    alert('User Registered');
  };

  return (
    <div>
      <h2>Register User</h2>
      <input onChange={e => setName(e.target.value)} placeholder="Name" />
      <Camera onCapture={setImage} />
      <button onClick={submit}>Register</button>
    </div>
  );
}

export default Register;
