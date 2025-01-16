import './ChatMessages.css';

interface Message {
	type: 'user' | 'bot';
	text: string;
}

export default function ChatMessages({ messages } : { messages: Message[] }) {
	return (<>
		<div className='messages'>
			{messages.map((message, index) => (
				<div key={index} className={message['type'] === 'user' ? 'message user' : 'message bot'}>
					<span>{message['text']}</span>
				</div>
			))}
		</div>
		</>
	)
}

export type { Message };
