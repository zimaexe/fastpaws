import React from 'react'
import './Prompt.css'

interface PromptProps {
    isShort: boolean;
    text: string;
    placeholder: string;
    handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onSend: () => void;
}

export default function Prompt({ isShort, text, placeholder, handleChange, onSend }: PromptProps) {
    return (
        <div className={isShort ? 'prompt short' : 'prompt'}>
            <input
                className='prompt-input'
                type="text"
                value={text}
                onChange={handleChange}
                placeholder={placeholder}
            />
            <button className="send-button" onClick={onSend}>
                <img src="/images/bottom.png" alt="Icon" />
            </button>
        </div>
    )
}
