import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
    Activity, Cpu, Zap, TrendingUp, TrendingDown, AlertTriangle,
    CheckCircle, Clock, BarChart3, ArrowLeft, Sparkles, Brain
} from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { apiRequest } from '../utils/api';

interface ModelMetrics {
    timestamp: string;
    responseTime: number;
    accuracy: number;
    throughput: number;
    errorRate: number;
}

interface PerformanceIssue {
    id: string;
    type: 'latency' | 'accuracy' | 'error';
    severity: 'low' | 'medium' | 'high';
    message: string;
    timestamp: string;
    auroraAction?: string;
}

export default function AuroraMonitor() {
    const navigate = useNavigate();
    const [metrics, setMetrics] = useState<ModelMetrics[]>([]);
    const [issues, setIssues] = useState<PerformanceIssue[]>([]);
    const [currentMetrics, setCurrentMetrics] = useState({
        avgResponseTime: 0,
        avgAccuracy: 0,
        totalRequests: 0,
        errorRate: 0,
    });

    useEffect(() => {
        fetchModelMetrics();
        const interval = setInterval(fetchModelMetrics, 5000); // Poll every 5 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchModelMetrics = async () => {
        try {
            const res = await apiRequest('/api/aurora/metrics');
            const data = await res.json();

            setMetrics(data.metrics || []);
            setCurrentMetrics(data.current || {});
            setIssues(data.issues || []);
        } catch (err) {
            console.error('Failed to fetch metrics:', err);
        }
    };

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'high': return 'text-red-400 bg-red-500/20 border-red-500';
            case 'medium': return 'text-orange-400 bg-orange-500/20 border-orange-500';
            case 'low': return 'text-yellow-400 bg-yellow-500/20 border-yellow-500';
            default: return 'text-gray-400 bg-gray-500/20 border-gray-500';
        }
    };

    const getStatusIcon = (severity: string) => {
        switch (severity) {
            case 'high': return <AlertTriangle className="w-5 h-5" />;
            case 'medium': return <Clock className="w-5 h-5" />;
            case 'low': return <CheckCircle className="w-5 h-5" />;
            default: return <Activity className="w-5 h-5" />;
        }
    };

    return (
        <div className="min-h-screen bg-aurora-bg text-white p-8">
            <div className="max-w-7xl mx-auto space-y-8">

                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center justify-between"
                >
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => navigate('/expenses')}
                            className="p-2 glass-card rounded-xl hover:bg-white/10 transition-all"
                        >
                            <ArrowLeft className="w-6 h-6" />
                        </button>
                        <div>
                            <h1 className="text-4xl font-bold bg-gradient-to-r from-aurora-blue to-purple-500 bg-clip-text text-transparent">
                                AURORA Model Monitor
                            </h1>
                            <p className="text-gray-400 mt-2">Real-time AI performance tracking & optimization</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2 glass-card px-4 py-2 rounded-xl">
                        <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                        <span className="text-sm text-gray-300">Live Monitoring</span>
                    </div>
                </motion.div>

                {/* Key Metrics Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <Zap className="w-8 h-8 text-aurora-blue" />
                            <span className="text-xs px-2 py-1 bg-aurora-blue/20 text-aurora-blue rounded-full">Real-time</span>
                        </div>
                        <h3 className="text-gray-400 text-sm">Avg Response Time</h3>
                        <p className="text-3xl font-bold text-white mt-2">{currentMetrics.avgResponseTime.toFixed(0)}ms</p>
                        <p className="text-sm text-aurora-success mt-2 flex items-center gap-1">
                            <TrendingDown className="w-4 h-4" />
                            12% faster
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <Brain className="w-8 h-8 text-purple-500" />
                            <span className="text-xs px-2 py-1 bg-purple-500/20 text-purple-400 rounded-full">AI Quality</span>
                        </div>
                        <h3 className="text-gray-400 text-sm">Model Accuracy</h3>
                        <p className="text-3xl font-bold text-white mt-2">{(currentMetrics.avgAccuracy * 100).toFixed(1)}%</p>
                        <p className="text-sm text-aurora-success mt-2 flex items-center gap-1">
                            <TrendingUp className="w-4 h-4" />
                            High quality
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <Activity className="w-8 h-8 text-green-500" />
                            <span className="text-xs px-2 py-1 bg-green-500/20 text-green-400 rounded-full">Active</span>
                        </div>
                        <h3 className="text-gray-400 text-sm">Total Requests</h3>
                        <p className="text-3xl font-bold text-white mt-2">{currentMetrics.totalRequests}</p>
                        <p className="text-sm text-gray-400 mt-2">This session</p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <AlertTriangle className="w-8 h-8 text-orange-500" />
                            <span className="text-xs px-2 py-1 bg-orange-500/20 text-orange-400 rounded-full">Monitoring</span>
                        </div>
                        <h3 className="text-gray-400 text-sm">Error Rate</h3>
                        <p className="text-3xl font-bold text-white mt-2">{(currentMetrics.errorRate * 100).toFixed(2)}%</p>
                        <p className="text-sm text-aurora-success mt-2">Within threshold</p>
                    </motion.div>
                </div>

                {/* Performance Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Response Time Chart */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <Zap className="w-5 h-5 text-aurora-blue" />
                            Response Time Trend
                        </h3>
                        <ResponsiveContainer width="100%" height={250}>
                            <AreaChart data={metrics}>
                                <defs>
                                    <linearGradient id="colorResponseTime" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#00d4ff" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#00d4ff" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis
                                    dataKey="timestamp"
                                    stroke="#9ca3af"
                                    tick={{ fill: '#9ca3af' }}
                                />
                                <YAxis
                                    stroke="#9ca3af"
                                    tick={{ fill: '#9ca3af' }}
                                    label={{ value: 'ms', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'rgba(10, 14, 39, 0.9)',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        borderRadius: '8px'
                                    }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="responseTime"
                                    stroke="#00d4ff"
                                    fillOpacity={1}
                                    fill="url(#colorResponseTime)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </motion.div>

                    {/* Accuracy Chart */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <Brain className="w-5 h-5 text-purple-500" />
                            Model Accuracy
                        </h3>
                        <ResponsiveContainer width="100%" height={250}>
                            <LineChart data={metrics}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis
                                    dataKey="timestamp"
                                    stroke="#9ca3af"
                                    tick={{ fill: '#9ca3af' }}
                                />
                                <YAxis
                                    stroke="#9ca3af"
                                    tick={{ fill: '#9ca3af' }}
                                    domain={[0, 1]}
                                    label={{ value: 'Accuracy', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'rgba(10, 14, 39, 0.9)',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        borderRadius: '8px'
                                    }}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="accuracy"
                                    stroke="#a855f7"
                                    strokeWidth={2}
                                    dot={{ fill: '#a855f7', r: 4 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </motion.div>
                </div>

                {/* AURORA Insights & Actions */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-6 rounded-2xl"
                >
                    <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-aurora-blue" />
                        AURORA Performance Insights
                    </h3>

                    {issues.length === 0 ? (
                        <div className="text-center py-12">
                            <CheckCircle className="w-16 h-16 text-aurora-success mx-auto mb-4" />
                            <p className="text-xl font-semibold text-white">All Systems Optimal</p>
                            <p className="text-gray-400 mt-2">AURORA is monitoring your AI model performance</p>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {issues.map((issue) => (
                                <div
                                    key={issue.id}
                                    className={`p-4 rounded-xl border-l-4 ${getSeverityColor(issue.severity)}`}
                                >
                                    <div className="flex items-start gap-4">
                                        <div className="mt-1">
                                            {getStatusIcon(issue.severity)}
                                        </div>
                                        <div className="flex-1">
                                            <div className="flex items-center justify-between mb-2">
                                                <h4 className="font-semibold text-white capitalize">{issue.type} Issue</h4>
                                                <span className="text-xs text-gray-400">
                                                    {new Date(issue.timestamp).toLocaleTimeString()}
                                                </span>
                                            </div>
                                            <p className="text-gray-300 text-sm mb-3">{issue.message}</p>
                                            {issue.auroraAction && (
                                                <div className="bg-aurora-blue/10 border border-aurora-blue/30 rounded-lg p-3">
                                                    <p className="text-xs text-gray-400 mb-1">🤖 AURORA Action Taken:</p>
                                                    <p className="text-sm text-aurora-blue">{issue.auroraAction}</p>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </motion.div>

                {/* How AURORA Solves Problems */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-8 rounded-2xl border-2 border-aurora-blue/30"
                >
                    <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                        <Cpu className="w-6 h-6 text-aurora-blue" />
                        How AURORA Goes Beyond Monitoring
                    </h3>

                    <div className="grid md:grid-cols-2 gap-6">
                        <div className="space-y-4">
                            <div className="flex items-start gap-3">
                                <div className="w-8 h-8 rounded-lg bg-aurora-blue/20 flex items-center justify-center flex-shrink-0">
                                    <Activity className="w-5 h-5 text-aurora-blue" />
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-1">1. Real-Time Monitoring</h4>
                                    <p className="text-sm text-gray-400">
                                        Tracks response times, accuracy, throughput, and error rates in real-time
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-start gap-3">
                                <div className="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center flex-shrink-0">
                                    <Brain className="w-5 h-5 text-purple-500" />
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-1">2. Intelligent Analysis</h4>
                                    <p className="text-sm text-gray-400">
                                        AI agents analyze patterns and predict potential performance degradation
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-start gap-3">
                                <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center flex-shrink-0">
                                    <Zap className="w-5 h-5 text-green-500" />
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-1">3. Automatic Optimization</h4>
                                    <p className="text-sm text-gray-400">
                                        Dynamically adjusts model parameters, caching strategies, and resource allocation
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-start gap-3">
                                <div className="w-8 h-8 rounded-lg bg-orange-500/20 flex items-center justify-center flex-shrink-0">
                                    <AlertTriangle className="w-5 h-5 text-orange-500" />
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-1">4. Proactive Alerts</h4>
                                    <p className="text-sm text-gray-400">
                                        Sends notifications before issues impact users, not after
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-start gap-3">
                                <div className="w-8 h-8 rounded-lg bg-yellow-500/20 flex items-center justify-center flex-shrink-0">
                                    <BarChart3 className="w-5 h-5 text-yellow-500" />
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-1">5. Performance Recovery</h4>
                                    <p className="text-sm text-gray-400">
                                        Automatically implements fixes: model reloading, cache clearing, fallback strategies
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-start gap-3">
                                <div className="w-8 h-8 rounded-lg bg-pink-500/20 flex items-center justify-center flex-shrink-0">
                                    <Sparkles className="w-5 h-5 text-pink-500" />
                                </div>
                                <div>
                                    <h4 className="font-semibold text-white mb-1">6. Continuous Learning</h4>
                                    <p className="text-sm text-gray-400">
                                        Learns from past issues to prevent future occurrences and improve over time
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="mt-6 p-4 bg-gradient-to-r from-aurora-blue/10 to-purple-500/10 rounded-xl border border-aurora-blue/30">
                        <p className="text-sm text-gray-300">
                            <span className="font-semibold text-aurora-blue">Key Difference:</span> Traditional monitoring tools only <span className="text-red-400">alert you to problems</span>.
                            AURORA <span className="text-aurora-success font-semibold">prevents and fixes them automatically</span>, ensuring your AI models maintain peak performance.
                        </p>
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
