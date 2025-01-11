import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useNavigate
} from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Page1 />} />
        <Route path="/page2" element={<Page2 />} />
      </Routes>
    </Router>
  );
}

function Page1() {
  const navigate = useNavigate();
  const [text, setText] = useState('');

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setText(event.target.value);
  };
  const handleClick = () => {
    navigate("/page2");
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
  );
}


function Page2() {
  const navigate = useNavigate();
  return (
    <div>
      <button onClick={() => navigate("/")}>Return on 1 page</button>
    </div>
  );
}

export default App
