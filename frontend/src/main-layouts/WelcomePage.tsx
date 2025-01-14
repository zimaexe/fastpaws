import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Prompt from '../components/prompt/Prompt';

export default function WelcomePage() {
	const navigate = useNavigate();
	const [text, setText] = useState('');

	const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setText(event.target.value);
	};
	
    const handleClick = () => {
		navigate("/chat");
	};

	return (
		<>
			<div className="white_field">
				<div className="text_part_of_white_field">
					<p className='title'>Hello, I'm <span style={{ color: '#0096C7' }}>FastPaws</span></p>
					<p className='bot-description'>I'm here to help you quickly access your information! Enter a name and your question, and I'll fetch the details about policies, claims, or medication coverage for you in no time.</p>
				</div>
                <Prompt
                    isShort={false}
                    text={text}
                    placeholder="tell me about you"
                    handleChange={handleChange}
                    onSend={handleClick}
                />
				<img className='doctor-cat' src="./images/doctor-cat.png" alt="Icon" />
			</div >
		</>
	);
}
