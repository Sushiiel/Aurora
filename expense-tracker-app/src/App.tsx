import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import ExpenseTracker from './pages/ExpenseTracker';
import AuroraMonitor from './pages/AuroraMonitor';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/expenses" element={<ExpenseTracker />} />
                <Route path="/aurora-monitor" element={<AuroraMonitor />} />
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </Router>
    );
}

export default App;
