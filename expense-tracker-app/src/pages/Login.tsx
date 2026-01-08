import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../config/firebase';
import { Mail, Lock, Sparkles, TrendingUp } from 'lucide-react';

export default function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSignUp, setIsSignUp] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleAuth = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            let userCredential;
            if (isSignUp) {
                userCredential = await createUserWithEmailAndPassword(auth, email, password);
            } else {
                userCredential = await signInWithEmailAndPassword(auth, email, password);
            }

            // Store user email for expense tracking
            localStorage.setItem('userEmail', userCredential.user.email || '');
            localStorage.setItem('userId', userCredential.user.uid);

            navigate('/expenses');
        } catch (error: any) {
            alert(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-aurora-bg flex items-center justify-center p-4">
            <div className="max-w-6xl w-full grid md:grid-cols-2 gap-8 items-center">

                {/* Left: Branding */}
                <motion.div
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="space-y-6"
                >
                    <div className="flex items-center gap-3">
                        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-aurora-blue to-purple-600 flex items-center justify-center">
                            <Sparkles className="w-8 h-8 text-white" />
                        </div>
                        <div>
                            <h1 className="text-4xl font-bold bg-gradient-to-r from-aurora-blue to-purple-500 bg-clip-text text-transparent">
                                AURORA
                            </h1>
                            <p className="text-gray-400">Expense Tracker</p>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <h2 className="text-3xl font-bold text-white">
                            Smart Budget Management with AI
                        </h2>
                        <p className="text-gray-400 text-lg">
                            Track expenses, get AI insights, and receive real-time budget alerts powered by AURORA agents.
                        </p>
                    </div>

                    <div className="space-y-3">
                        <div className="flex items-center gap-3 text-aurora-blue">
                            <TrendingUp className="w-5 h-5" />
                            <span>AI-powered expense analysis</span>
                        </div>
                        <div className="flex items-center gap-3 text-purple-400">
                            <Mail className="w-5 h-5" />
                            <span>Automated email budget alerts</span>
                        </div>
                        <div className="flex items-center gap-3 text-green-400">
                            <Sparkles className="w-5 h-5" />
                            <span>Real-time model performance monitoring</span>
                        </div>
                    </div>
                </motion.div>

                {/* Right: Login Form */}
                <motion.div
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="glass-card p-8 rounded-2xl"
                >
                    <h3 className="text-2xl font-bold text-white mb-6">
                        {isSignUp ? 'Create Account' : 'Welcome Back'}
                    </h3>

                    <form onSubmit={handleAuth} className="space-y-4">
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Email</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full bg-aurora-bg border border-white/10 rounded-xl pl-12 pr-4 py-3 text-white focus:outline-none focus:border-aurora-blue"
                                    placeholder="you@example.com"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full bg-aurora-bg border border-white/10 rounded-xl pl-12 pr-4 py-3 text-white focus:outline-none focus:border-aurora-blue"
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full btn-primary disabled:opacity-50"
                        >
                            {loading ? 'Processing...' : (isSignUp ? 'Sign Up' : 'Sign In')}
                        </button>
                    </form>

                    <div className="mt-6 text-center">
                        <button
                            onClick={() => setIsSignUp(!isSignUp)}
                            className="text-aurora-blue hover:underline"
                        >
                            {isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
                        </button>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
