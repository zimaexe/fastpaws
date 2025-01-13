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
        <img className='doctor-cat' src="./images/doctor-cat.png" alt="Icon" />
      </div >
    </>
  );
}


function Page2() {
  const navigate = useNavigate();
  const [text, setText] = useState('');
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setText(event.target.value);
  };
  const handleClick = () => {
    navigate("/");
  };
  return (
    <>
      <div
        className="white_field"
        style={{
          width: "1000px",
          height: "100%",
          display: 'flex',
          justifyContent: 'flex-start',
          flexDirection: 'column',
          padding: '40px',
          paddingBottom: '60px'
        }}
      >
        <h1 style={{ fontFamily: "PoppinsExtraBold" }}>Chat</h1>
        <div className='messages'>
          <div className="messageUser">Hello, my name is Polina. Tell me smth about medecine.</div>
          <div className="messageBot">Advancements in modern medicine have drastically improved the quality of life for many people around the world. From groundbreaking cancer treatments to innovative surgeries, the healthcare field is constantly evolving. The use of technology, such as robotic-assisted surgeries and AI-driven diagnostics, has paved the way for more accurate and less invasive procedures. In addition, telemedicine has made healthcare more accessible, allowing patients to consult with doctors remotely. However, as medical science progresses, ethical questions about privacy, accessibility, and the long-term effects of new treatments continue to spark debate in the field.</div>
          <div className="messageUser">It's very intresting!!</div>
        </div>
        <div className='prompt' style={{ marginLeft: '50px' }}><label>
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
    </>
  );
}

export default App
