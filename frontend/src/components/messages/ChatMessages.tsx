import './ChatMessages.css';

interface Message {
	type: 'user' | 'bot' | 'error';
	text: string;
}

export default function ChatMessages({ messages } : { messages: Message[] }) {
	const chooseMessageClass = (message: Message) => {
		switch (message['type']) {
			case 'user':
				return 'message user';
			case 'bot':
				return 'message bot';
			case 'error':
				return 'message bot error';
		}
	}

	return (<>
		<div className='messages'>
			{messages.map((message, index) => (
				<div key={index} className={chooseMessageClass(message)}>
					<span>{message['text']}</span>
				</div>
			))}
		</div>
		</>
	)
}

export type { Message };
