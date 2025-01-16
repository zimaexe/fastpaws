import React from 'react'
import './Prompt.css'

interface PromptProps {
    locked?: boolean;
    isShort: boolean;
    text: string;
    placeholder: string;
    handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onSend: () => void;
}

export default function Prompt({ locked, isShort, text, placeholder, handleChange, onSend }: PromptProps) {
    return (
        <div className={'prompt '
            + (isShort ? 'short ' : '')
            + (locked ? 'locked ' : '')}>
            <input
                ref={input => input?.focus()}
                disabled={locked}
                className='prompt-input'
                type="text"
                value={text}
                onChange={handleChange}
                placeholder={placeholder}
                autoComplete="off"
            />
            <button type='submit' className="send-button" onClick={() => !locked ? onSend() : null}>
                <img src="/images/bottom.png" alt="Icon" />
            </button>
        </div>
    )
}
