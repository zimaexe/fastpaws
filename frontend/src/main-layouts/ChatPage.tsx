import { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
import ChatMessages, { Message } from '../components/messages/ChatMessages';
import Prompt from '../components/prompt/Prompt';

export default function ChatPage() {
	// const navigate = useNavigate();
	const [text, setText] = useState('');
	
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setText(event.target.value);
	};
	
    // const handleClick = () => {
	// 	navigate("/");
	// };

	const [messages, setMessages] = useState<Message[]>([
        { type: 'user', text: "I need help with my policy" },
        { type: 'bot', text: "Sure! I can help with that. Please provide me with your policy number." },
        { type: 'user', text: "123456" },
        { type: 'bot', text: "I found your policy. It covers your pet's medical expenses up to $10,000 per year." },
        { type: 'user', text: "Thank you!" },
        { type: 'bot', text: "You're welcome! Is there anything else I can help you with?" },
        { type: 'user', text: "No, that's all. Thanks!" },
        { type: 'bot', text: "Have a great day!" },
    ]);

    const addMessage = (text: string, type: 'user' | 'bot') => {
        setMessages([...messages, { type, text }]);
        const messagesBlock = document.querySelector('.messages');
        if (messagesBlock)
            setTimeout(() => messagesBlock.scrollTo(0, messagesBlock.scrollHeight), 100);
    }

	return (
		<>
			<div className="white_field wide">
				<p className='title-chat'>Chat</p>
                <ChatMessages messages={messages}/>
                <Prompt
                    isShort={true}
                    text={text}
                    placeholder="write your message"
                    handleChange={handleChange}
                    onSend={() => addMessage(text, 'user')}
                />
				<img className='doctor-cat-chat' src="./images/doctor-cat.png" alt="Icon" />
			</div >
		</>
	);
}
