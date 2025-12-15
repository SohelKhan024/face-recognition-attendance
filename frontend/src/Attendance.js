import React, { useState } from 'react';
import Camera from './Camera';

function Attendance() {
  const [image, setImage] = useState(null);

  const markAttendance = async () => {
    const formData = new FormData();
    formData.append('image', image);

    const res = await fetch('http://localhost:5000/attendance', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    alert(data.message);
  };

  return (
    <div>
      <h2>Mark Attendance</h2>
      <Camera onCapture={setImage} />
      <button onClick={markAttendance}>Submit</button>
    </div>
  );
}

export default Attendance;
