import React, { useState } from 'react';

function Chatgpt() {
  const [inputValue, setInputValue] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:5000/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data: inputValue })
    });
    const data = await response.json();
    console.log("the response :",data.response)
    setResponse(data.response);
  }

  const handleChange = (e) => {
    setInputValue(e.target.value);
  }

  return (
    <div >
      <h1>Chatgpt</h1>
      
      <form onSubmit={handleSubmit}>
        <label>
          Ask me anything
          <input type="text" value={inputValue} onChange={handleChange} />
        </label>
        <button type="submit">Send</button>
      </form>
      {response && <p>Response: {response}</p>}
    </div>
  );
}

export default Chatgpt;
