import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Rocket, Activity, Brain, Shield } from 'lucide-react';

export default function Home() {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-aurora-bg flex flex-col items-center justify-center p-4 relative overflow-hidden">
            {/* Dynamic Background */}
            <div className="absolute inset-0">
                <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-aurora-blue/5 rounded-full blur-[150px] animate-pulse-slow" />
                <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-purple-600/5 rounded-full blur-[150px] animate-pulse-slow" style={{ animationDelay: '2s' }} />
            </div>

            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 1 }}
                className="z-10 text-center max-w-4xl"
            >
                <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="flex justify-center mb-8"
                >
                    <div className="p-6 bg-aurora-card/50 backdrop-blur-md rounded-2xl border border-aurora-blue/20 shadow-[0_0_30px_rgba(0,212,255,0.2)]">
                        <Rocket className="w-16 h-16 text-aurora-blue" />
                    </div>
                </motion.div>

                <motion.h1
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.4 }}
                    className="text-6xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-aurora-blue to-purple-400 mb-6 drop-shadow-2xl"
                >
                    AURORA
                </motion.h1>

                <motion.p
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.6 }}
                    className="text-xl md:text-2xl text-gray-300 mb-12 max-w-2xl mx-auto leading-relaxed"
                >
                    Agentic Unified Reasoning & Optimization Runtime for AI Systems
                </motion.p>

                {/* Feature Grid */}
                <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.8 }}
                    className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16"
                >
                    {[
                        { icon: Activity, title: "Self-Observing", desc: "Real-time drift detection" },
                        { icon: Brain, title: "Self-Reasoning", desc: "RAG-powered decisions" },
                        { icon: Shield, title: "Self-Optimizing", desc: "Autonomous actions" },
                    ].map((feature, idx) => (
                        <div key={idx} className="glass-card p-6 rounded-xl hover:bg-aurora-card/80 transition-colors">
                            <feature.icon className="w-8 h-8 text-aurora-blue mb-3 mx-auto" />
                            <h3 className="font-semibold text-white mb-1">{feature.title}</h3>
                            <p className="text-sm text-gray-400">{feature.desc}</p>
                        </div>
                    ))}
                </motion.div>

                <motion.button
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 1 }}
                    onClick={() => navigate('/dashboard')}
                    className="bg-white text-aurora-bg px-12 py-4 rounded-full text-xl font-bold hover:scale-105 hover:shadow-[0_0_30px_rgba(255,255,255,0.3)] transition-all duration-300"
                >
                    Initialize System
                </motion.button>
            </motion.div>
        </div>
    );
}
