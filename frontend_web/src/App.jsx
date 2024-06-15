import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");


  const send = async (event) => {

    event.preventDefault();

    setPrompt("")
    setResponse("")

    fetch("http://127.0.0.1:5000",{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"prompt":prompt})
    })
    .then((response)=>{
      return response.json()
    })
    .then((data) => {
      setResponse(data.response);
    })
    .catch((err)=>{
      console.error(err)
    })
  }

  return (
    <>
      <p className='chat'>{response}</p>
      <form onSubmit={send} method="GET" className='chat-window'>
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="chat-window-message"
        />
      </form>
    </>
  )
}

export default App
