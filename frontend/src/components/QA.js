import React, { useState } from 'react';

function QA() {
  const [inputValue1, setInputValue1] = useState('');
  const [inputValue2, setInputValue2] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data1: inputValue1, data2: inputValue2 })
    });
    const data = await response.json();
    setResponse(data.response);
  }

  const handleChange1 = (e) => {
    setInputValue1(e.target.value);
  }

  const handleChange2 = (e) => {
    setInputValue2(e.target.value);
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <form onSubmit={handleSubmit}>
        <label>
          Enter data 1:
          <input type="text" value={inputValue1} onChange={handleChange1} />
        </label>
        <label>
          Enter data 2:
          <input type="text" value={inputValue2} onChange={handleChange2} />
        </label>
        <button type="submit">Send</button>
      </form>
      {response && <p>Response: {response}</p>}
    </div>
  );
}

export default QA;
