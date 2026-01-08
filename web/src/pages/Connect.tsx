import { useState } from 'react';
import { motion } from 'framer-motion';
import {
    Rocket, Code, Zap, Copy, Check, Terminal, ArrowRight,
    Server, Shield, Activity
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { apiRequest, getApiUrl } from '../utils/api';

export default function Connect() {
    const [modelName, setModelName] = useState('');
    const [copied, setCopied] = useState(false);
    const [isTesting, setIsTesting] = useState(false);
    const [testResult, setTestResult] = useState<'success' | 'error' | null>(null);

    const generateCode = () => `import requests

# Paste this where your model runs inference
API_URL = "${getApiUrl() || 'YOUR_DEPLOYED_URL'}"

requests.post(f"{API_URL}/api/metrics", json={
    "model_name": "${modelName || 'your-model-name'}",
    "accuracy": 0.95,        # Replace with real accuracy
    "latency_ms": 120,       # Replace with real latency
    "data_drift_score": 0.0, # Optional: Drift metric
    "metadata": {
        "version": "1.0",
        "env": "production"
    }
})`;

    const handleCopy = () => {
        navigator.clipboard.writeText(generateCode());
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const handleTestPing = async () => {
        if (!modelName) return;
        setIsTesting(true);
        setTestResult(null);
        try {
            const res = await apiRequest('/api/metrics', {
                method: 'POST',
                body: JSON.stringify({
                    model_name: modelName,
                    accuracy: 0.88,
                    latency_ms: 250,
                    data_drift_score: 0.1,
                    metadata: { source: 'ui-test-ping' }
                })
            });
            if (res.ok) {
                setTestResult('success');
            } else {
                setTestResult('error');
            }
        } catch (err) {
            setTestResult('error');
        } finally {
            setIsTesting(false);
        }
    };

    return (
        <div className="min-h-screen bg-aurora-bg text-gray-200 font-sans selection:bg-aurora-blue/30 flex">
            {/* Mini Sidebar */}
            <div className="w-20 bg-aurora-dark border-r border-white/5 flex flex-col items-center py-6 gap-6">
                <Link to="/home" className="w-10 h-10 bg-gradient-to-br from-aurora-blue to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-aurora-blue/20">
                    <Rocket className="text-white w-6 h-6" />
                </Link>
                <div className="w-full h-px bg-white/10" />
                <Link to="/dashboard" className="p-3 text-gray-400 hover:text-white rounded-xl hover:bg-white/5 transition-colors">
                    <Activity className="w-6 h-6" />
                </Link>
            </div>

            <div className="flex-1 overflow-y-auto">
                <div className="max-w-5xl mx-auto p-8 lg:p-12">

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mb-12"
                    >
                        <div className="flex items-center gap-3 mb-4">
                            <span className="px-3 py-1 rounded-full bg-aurora-blue/10 text-aurora-blue border border-aurora-blue/20 text-sm font-medium">Integration Wizard</span>
                        </div>
                        <h1 className="text-4xl font-bold text-white mb-4">Connect Your AI Model</h1>
                        <p className="text-xl text-gray-400 max-w-2xl">
                            Register your model to start autonomous monitoring. AURORA will track its performance, detect drift, and trigger healing agents automatically.
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">

                        {/* Left Col: Setup */}
                        <motion.div
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.2 }}
                            className="space-y-8"
                        >
                            <div className="glass-card p-8 rounded-2xl border-t-2 border-t-aurora-blue">
                                <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                                    <Server className="w-5 h-5 text-aurora-blue" />
                                    1. Model Details
                                </h3>
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Model Unique Name</label>
                                        <input
                                            type="text"
                                            value={modelName}
                                            onChange={(e) => setModelName(e.target.value)}
                                            placeholder="e.g., prod-fraud-detector-v1"
                                            className="w-full bg-aurora-dark border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-aurora-blue/50 focus:ring-1 focus:ring-aurora-blue/50 transition-all"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Environment (Metadata)</label>
                                        <select className="w-full bg-aurora-dark border border-white/10 rounded-xl py-3 px-4 text-white focus:outline-none focus:border-aurora-blue/50">
                                            <option>Production</option>
                                            <option>Staging</option>
                                            <option>Development</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div className="glass-card p-8 rounded-2xl">
                                <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                                    <Terminal className="w-5 h-5 text-purple-500" />
                                    2. Verify Connection
                                </h3>
                                <p className="text-gray-400 text-sm mb-6">
                                    Send a simulated "ping" to the AURORA Runtime to verify the pipeline is active for
                                    <span className="text-white font-medium"> {modelName || 'your model'}</span>.
                                </p>

                                <button
                                    onClick={handleTestPing}
                                    disabled={!modelName || isTesting}
                                    className="w-full py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl font-medium text-white transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {isTesting ? (
                                        'Sending Ping...'
                                    ) : testResult === 'success' ? (
                                        <>
                                            <Check className="w-5 h-5 text-green-400" />
                                            Ping Received!
                                        </>
                                    ) : testResult === 'error' ? (
                                        <>
                                            <Shield className="w-5 h-5 text-red-500" />
                                            Connection Failed
                                        </>
                                    ) : (
                                        <>
                                            <Zap className="w-5 h-5 text-yellow-500" />
                                            Send Test Ping
                                        </>
                                    )}
                                </button>

                                {testResult === 'success' && (
                                    <div className="mt-4 p-4 bg-green-500/10 border border-green-500/20 rounded-lg text-sm text-green-400">
                                        Success! Data received by ingestion agent. You can view it on the Dashboard.
                                        <Link to="/dashboard" className="block mt-2 underline font-semibold">Go to Dashboard &rarr;</Link>
                                    </div>
                                )}
                            </div>
                        </motion.div>

                        {/* Right Col: Code */}
                        <motion.div
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.4 }}
                            className="glass-card p-8 rounded-2xl bg-[#0F1117] border border-white/10 relative"
                        >
                            <h3 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                                <Code className="w-5 h-5 text-green-400" />
                                3. Integration Code
                            </h3>

                            <div className="absolute top-8 right-8">
                                <button
                                    onClick={handleCopy}
                                    className="p-2 bg-white/5 hover:bg-white/10 rounded-lg text-gray-400 hover:text-white transition-colors"
                                    title="Copy Code"
                                >
                                    {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                                </button>
                            </div>

                            <div className="bg-[#090b10] rounded-xl p-4 overflow-x-auto border border-white/5 font-mono text-sm leading-relaxed">
                                <pre>
                                    <code className="text-gray-300">
                                        {generateCode()}
                                    </code>
                                </pre>
                            </div>

                            <div className="mt-6 flex items-start gap-3 p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl">
                                <Shield className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
                                <div>
                                    <h4 className="text-blue-200 font-medium text-sm">Secure Ingestion</h4>
                                    <p className="text-blue-300/60 text-xs mt-1">
                                        The endpoint is protected. In production, your API will be available at your deployed URL.
                                    </p>
                                </div>
                            </div>

                            <Link
                                to="/dashboard"
                                className="mt-8 flex items-center justify-center gap-2 w-full py-4 bg-gradient-to-r from-aurora-blue to-blue-600 hover:from-blue-500 hover:to-blue-700 text-aurora-bg font-bold rounded-xl transition-all shadow-lg shadow-aurora-blue/20"
                            >
                                I've Integrated It - Finish <ArrowRight className="w-5 h-5" />
                            </Link>

                        </motion.div>
                    </div>
                </div>
            </div>
        </div>
    );
}
