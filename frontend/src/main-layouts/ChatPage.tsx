import { useState } from 'react';
import ChatMessages, { Message } from '../components/messages/ChatMessages';
import Prompt from '../components/prompt/Prompt';
import { useLocation } from 'react-router-dom';
import dotenv from 'dotenv';

export default function ChatPage() {
    dotenv.config({
        path: '../.env'
    });

    const [text, setText] = useState('');
    const [, setLastBotMessage] = useState('');
    const [locked, setLocked] = useState(false);

    const location = useLocation();
    const initialPrompt = location.state?.prompt || '';

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		setText(event.target.value);
	};

	const [messages, setMessages] = useState<Message[]>([
        // { type: 'bot', text: "Hello, how can I help you?" },
    ]);

    const scrollToBottom = () => {
        const messagesBlock = document.querySelector('.messages');
        if (messagesBlock) setTimeout(() => messagesBlock.scrollTo(0, messagesBlock.scrollHeight), 100);
    }


    const addMessage = (text: string, type: 'user' | 'bot' | 'error') => {
        if (text == '') return;
        setText('');
        setLocked(true);
        console.log("clearing input");
        let newMessages = [...messages, { type, text }];
        if (text == 'sosal?')
            newMessages = [...newMessages, { type: 'bot', text: 'yes' }];

        fetch(`${process.env.BACKEND_ADDRESS}/generate`, {
            method: 'POST',
            body: JSON.stringify({ text: text, chat_id: document.cookie.split('=')[1],}),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                if(response.status == 400){
                    setMessages([...newMessages, { type: 'error', text: 'I am sorry, but I can not find you in our database. Please provide your name or request some help from administrator.' }]);
                    setLocked(false);
                    return newMessages;
                }
                else
                {
                const stream = response.body;
                if (!stream)
                    throw new Error('ReadableStream is not yet supported in this browser.');
                const reader = stream.getReader();
                const readChunk = () => {
                    reader.read()
                        .then(({ value, done }) => {
                            if (done) {
                                setLocked(false);
                                console.log('Stream finished');
                                return;
                            }
                            const chunkString = new TextDecoder().decode(value);
                            setLastBotMessage(prev => {
                                const updatedMessage = prev + chunkString;
                                setMessages([...newMessages, { type: 'bot', text: updatedMessage }]);
                                return updatedMessage;
                            });
                            readChunk();
                        })
                        .catch(error => {
                            setLocked(false);
                            console.error(error);
                        });
                };
                readChunk();
            }})
            .catch(error => {
                setLocked(false);
                console.error(error);
            });

        setLastBotMessage(() => {
            scrollToBottom();
            return '';
        });
        setMessages(newMessages);
        scrollToBottom();
    }

    useState(() => {
        if (initialPrompt)
            addMessage(initialPrompt, 'user');
    });

	return (
		<>
			<div className="white_field chat">
				<p className='title-chat'>Chat</p>
                <ChatMessages messages={messages}/>
                <Prompt
                    locked={locked}
                    // lockFunction={() => setLocked(true)}
                    isShort={true}
                    text={text}
                    placeholder="write your message"
                    handleChange={handleChange}
                    onSend={() => {addMessage(text, 'user')}}
                />
				<img className='doctor-cat-chat' src="./images/doctor-cat.png" alt="Icon" />
			</div >
		</>
	);
}

