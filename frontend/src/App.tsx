import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [text, setText] = useState('');

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setText(event.target.value);
  };
  const handleClick = () => {
    alert('Кнопка натиснута!');
  };
  return (
    <>
      <div className="white_field">
        <div className="text_part_of_white_field">
          <h1>Hello, I’m <span style={{ color: '#0096C7' }}>FastPaws</span></h1>
          <p className='bot-description'>I’m here to help you quickly access your information! Enter a name and your question, and I’ll fetch the details about policies, claims, or medication coverage for you in no time.</p>
        </div>
        <div className='prompt'><label>
          <input
            className='prompt-input'
            type="text"
            value={text}
            onChange={handleChange}
            placeholder="tell me about you"
          />
        </label>
          <button className="image-button" onClick={handleClick}>
            <img className='image-of-bottom' src="./images/bottom.png" alt="Icon" />
          </button>
        </div>
      </div >
      <img className='doctor-cat' src="./images/doctor-cat.png" alt="Icon" />
    </>
  )
}

export default App
