import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function ChatPage() {
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
				<div className='prompt' style={{ marginLeft: '50px' }}>
					<input
						className='prompt-input'
						type="text"
						value={text}
						onChange={handleChange}
						placeholder="tell me about you"
					/>
					<button className="image-button" onClick={handleClick}>
						<img className='image-of-bottom' src="./images/bottom.png" alt="Icon" />
					</button>
				</div>
			</div >
		</>
	);
}
