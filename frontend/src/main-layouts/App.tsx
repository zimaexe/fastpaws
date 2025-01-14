import './App.css'
import {
	BrowserRouter as Router,
	Routes,
	Route,
} from 'react-router-dom';
import WelcomePage from './WelcomePage';
import ChatPage from './ChatPage';

export default function App() {
	return (
		<Router>
			<Routes>
				<Route path="/chat" element={<ChatPage />} />
				<Route path="/" element={<WelcomePage />} />
			</Routes>
		</Router>
	);
}
