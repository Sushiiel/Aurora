import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Rocket, Lock, Mail, ArrowRight, AlertCircle, UserPlus, User, CheckCircle2 } from 'lucide-react';
import {
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    updateProfile,
    sendEmailVerification,
    signOut
} from 'firebase/auth';
import { auth } from '../lib/firebase';

export default function Login() {
    const navigate = useNavigate();
    const [isSignUp, setIsSignUp] = useState(false);
    const [loading, setLoading] = useState(false);
    const [verificationSent, setVerificationSent] = useState(false);

    // Form State
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [error, setError] = useState('');

    const handleAuth = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            if (isSignUp) {
                // 1. Create User
                const userCredential = await createUserWithEmailAndPassword(auth, email, password);

                // 2. Update Profile
                if (name) {
                    await updateProfile(userCredential.user, { displayName: name });
                }

                // 3. Send Verification Email
                await sendEmailVerification(userCredential.user);

                // 4. Force Logout so they can't enter without verifying
                await signOut(auth);

                // 5. Show Success UI
                setVerificationSent(true);
                setIsSignUp(false); // Switch back to login view context

            } else {
                // Login Request
                const userCredential = await signInWithEmailAndPassword(auth, email, password);

                // Check if email is verified
                if (!userCredential.user.emailVerified) {
                    // Block access
                    await signOut(auth);
                    setError("Please verify your email address before logging in. Check your inbox.");

                    // Allow resending if they are stuck? (Complex, for now just block)
                } else {
                    // Success
                    navigate('/home');
                }
            }
        } catch (err: any) {
            // Fallback for demo admin
            if (!isSignUp && email === 'admin@aurora.ai' && password === 'password') {
                navigate('/home');
                return;
            }

            console.error("Auth Error", err);
            let msg = "Authentication failed.";
            if (err.code === 'auth/email-already-in-use') msg = "That email is already registered.";
            if (err.code === 'auth/weak-password') msg = "Password should be at least 6 characters.";
            if (err.code === 'auth/invalid-credential') msg = "Invalid email or password.";
            if (err.code === 'auth/operation-not-allowed') msg = "Email/Password login is not enabled in Firebase Console.";
            setError(msg);
        } finally {
            setLoading(false);
        }
    };

    if (verificationSent) {
        return (
            <div className="min-h-screen bg-aurora-bg flex items-center justify-center p-4">
                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="glass-card w-full max-w-md p-8 rounded-2xl text-center"
                >
                    <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                        <CheckCircle2 className="w-8 h-8 text-green-500" />
                    </div>
                    <h2 className="text-2xl font-bold text-white mb-2">Verification Sent!</h2>
                    <p className="text-gray-300 mb-6">
                        We sent a verification link to <span className="text-white font-medium">{email}</span>.
                        Please check your inbox (and spam folder) and click the link to activate your account.
                    </p>
                    <button
                        onClick={() => {
                            setVerificationSent(false);
                            setEmail('');
                            setPassword('');
                        }}
                        className="w-full glass-button py-3 rounded-xl font-semibold"
                    >
                        Return to Sign In
                    </button>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-aurora-bg flex items-center justify-center p-4 relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] bg-aurora-blue/10 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-20%] right-[-10%] w-[500px] h-[500px] bg-purple-600/10 rounded-full blur-[120px]" />
            </div>

            <motion.div
                layout
                className="glass-card w-full max-w-md p-8 rounded-2xl relative z-10"
            >
                <div className="flex flex-col items-center mb-8">
                    <motion.div
                        initial={{ scale: 0.8 }} animate={{ scale: 1 }}
                        className="p-4 bg-aurora-card rounded-full mb-4 border border-aurora-blue/30 shadow-[0_0_15px_rgba(0,212,255,0.3)]"
                    >
                        {isSignUp ? <UserPlus className="w-8 h-8 text-aurora-blue" /> : <Rocket className="w-8 h-8 text-aurora-blue" />}
                    </motion.div>
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-aurora-blue mb-2">
                        {isSignUp ? 'Create Account' : 'Welcome Back'}
                    </h1>
                    <p className="text-gray-400">
                        {isSignUp ? 'Join the autonomous future' : 'Sign in to access AURORA'}
                    </p>
                </div>

                <form onSubmit={handleAuth} className="space-y-6">
                    <AnimatePresence>
                        {error && (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center gap-2 text-sm text-red-400 overflow-hidden text-left"
                            >
                                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                                <div>{error}</div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Name Field (Sign Up Only) */}
                    <AnimatePresence>
                        {isSignUp && (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                className="space-y-2 overflow-hidden"
                            >
                                <label className="text-sm text-gray-400 ml-1">Full Name</label>
                                <div className="relative group">
                                    <User className="absolute left-3 top-3 w-5 h-5 text-gray-500 group-focus-within:text-aurora-blue transition-colors" />
                                    <input
                                        type="text"
                                        value={name}
                                        onChange={(e) => setName(e.target.value)}
                                        className="w-full bg-aurora-dark border border-aurora-blue/20 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-600 focus:outline-none focus:border-aurora-blue/50 focus:ring-1 focus:ring-aurora-blue/50 transition-all"
                                        placeholder="John Doe"
                                    />
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <div className="space-y-2">
                        <label className="text-sm text-gray-400 ml-1">Email Address</label>
                        <div className="relative group">
                            <Mail className="absolute left-3 top-3 w-5 h-5 text-gray-500 group-focus-within:text-aurora-blue transition-colors" />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-aurora-dark border border-aurora-blue/20 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-600 focus:outline-none focus:border-aurora-blue/50 focus:ring-1 focus:ring-aurora-blue/50 transition-all"
                                placeholder="name@company.com"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm text-gray-400 ml-1">Password</label>
                        <div className="relative group">
                            <Lock className="absolute left-3 top-3 w-5 h-5 text-gray-500 group-focus-within:text-aurora-blue transition-colors" />
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full bg-aurora-dark border border-aurora-blue/20 rounded-xl py-3 pl-10 pr-4 text-white placeholder-gray-600 focus:outline-none focus:border-aurora-blue/50 focus:ring-1 focus:ring-aurora-blue/50 transition-all"
                                placeholder="••••••••"
                                required
                                minLength={6}
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full glass-button py-3 rounded-xl font-semibold flex items-center justify-center gap-2 group relative overflow-hidden disabled:opacity-50"
                    >
                        {loading ? (
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <>
                                {isSignUp ? 'Create Account' : 'Sign In'}
                                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </button>

                    <div className="text-center pt-2">
                        <span className="text-gray-500 text-sm">
                            {isSignUp ? 'Already have an account?' : "Don't have an account?"}
                        </span>
                        <button
                            type="button"
                            onClick={() => {
                                setIsSignUp(!isSignUp);
                                setError('');
                            }}
                            className="ml-2 text-sm text-aurora-blue hover:text-white transition-colors font-medium"
                        >
                            {isSignUp ? 'Sign In' : 'Sign Up'}
                        </button>
                    </div>
                </form>

                <div className="mt-8 text-center text-xs text-gray-600">
                    Protected by <span className="text-gray-500">AURORA Identity</span> &bull;
                    <span className="ml-1 text-gray-500">Firebase Secure</span>
                </div>
            </motion.div>
        </div>
    );
}
