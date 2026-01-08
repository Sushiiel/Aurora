import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Rocket, LayoutDashboard, Bot, Activity, Brain,
    Settings, Bell, Search, RefreshCw, CheckCircle2,
    AlertTriangle, Cpu, TrendingUp, Database, Command, ExternalLink, Zap, Wallet
} from 'lucide-react';
import {
    LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar
} from 'recharts';
import clsx from 'clsx';
import { apiRequest, getApiDocsUrl } from '../utils/api';

// --- Types ---
interface Metric {
    label: string;
    value: string | number;
    delta: string;
    deltaType: 'positive' | 'negative' | 'neutral';
}

interface BackendMetric {
    id: number;
    model_name: string;
    accuracy: number;
    latency_ms: number;
    timestamp: string;
    data_drift_score: number;
}

interface BackendDecision {
    id: number;
    agent_type: string;
    decision_type: string;
    reasoning: string;
    status: 'approved' | 'rejected' | 'pending';
    timestamp: string;
    approved: boolean;
}

// --- Components ---

const SidebarItem = ({ icon: Icon, label, active, onClick }: any) => (
    <button
        onClick={onClick}
        className={clsx(
            "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200",
            active
                ? "bg-gradient-to-r from-aurora-blue/20 to-transparent border-l-2 border-aurora-blue text-white"
                : "text-gray-400 hover:text-white hover:bg-white/5"
        )}
    >
        <Icon className="w-5 h-5" />
        <span className="font-medium">{label}</span>
    </button>
);

const MetricCard = ({ metric, index }: { metric: Metric; index: number }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: index * 0.1 }}
        className="glass-card p-6 rounded-2xl relative overflow-hidden group"
    >
        <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <Activity className="w-12 h-12 text-aurora-blue" />
        </div>
        <h3 className="text-gray-400 text-sm font-medium mb-2">{metric.label}</h3>
        <div className="text-3xl font-bold text-white mb-2">{metric.value}</div>
        <div className={clsx("text-sm font-medium",
            metric.deltaType === 'positive' ? 'text-aurora-success' :
                metric.deltaType === 'negative' ? 'text-red-400' : 'text-aurora-blue'
        )}>
            {metric.delta}
        </div>
    </motion.div>
);

export default function Dashboard() {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('dashboard');
    const [isRefreshing, setIsRefreshing] = useState(false);

    // Real Data State
    const [metrics, setMetrics] = useState<Metric[]>([]);
    const [rawMetrics, setRawMetrics] = useState<BackendMetric[]>([]);
    const [decisions, setDecisions] = useState<BackendDecision[]>([]);
    const [chartData, setChartData] = useState<any[]>([]);

    // Memory State
    const [memoryQuery, setMemoryQuery] = useState('');
    const [memoryResults, setMemoryResults] = useState<any[]>([]);
    const [memoryStats, setMemoryStats] = useState<any>(null);

    const fetchData = async () => {
        try {
            setIsRefreshing(true);

            // Fetch Metrics
            const metricsRes = await apiRequest('/api/metrics/latest?limit=50');
            const metricsJson = await metricsRes.json();
            const fetchedMetrics: BackendMetric[] = metricsJson.metrics || [];
            setRawMetrics(fetchedMetrics);

            if (fetchedMetrics.length > 0) {
                const latest = fetchedMetrics[0];
                const prev = fetchedMetrics[1] || latest;

                const accDelta = (latest.accuracy - prev.accuracy) * 100;
                const latDelta = latest.latency_ms - prev.latency_ms;

                setMetrics([
                    { label: 'Active Model', value: latest.model_name, delta: 'v1.0 Running', deltaType: 'neutral' },
                    { label: 'Current Accuracy', value: `${(latest.accuracy * 100).toFixed(1)}%`, delta: `${accDelta > 0 ? '+' : ''}${accDelta.toFixed(1)}%`, deltaType: accDelta >= 0 ? 'positive' : 'negative' },
                    { label: 'Latency', value: `${latest.latency_ms.toFixed(0)}ms`, delta: `${latDelta > 0 ? '+' : ''}${latDelta.toFixed(0)}ms`, deltaType: latDelta <= 0 ? 'positive' : 'negative' },
                    { label: 'Data Integrity', value: `${(1 - latest.data_drift_score).toFixed(2)}`, delta: 'Drift Score', deltaType: 'positive' },
                ]);

                const newChartData = fetchedMetrics.slice(0, 20).reverse().map(m => ({
                    time: new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                    acc: (m.accuracy * 100).toFixed(1)
                }));
                setChartData(newChartData);
            }

            // Fetch Decisions
            const decisionsRes = await apiRequest('/api/decisions?limit=20');
            const decisionsJson = await decisionsRes.json();
            setDecisions(decisionsJson.decisions || []);

            // Fetch Memory Stats (Only once or actively)
            if (activeTab === 'memory') {
                const memRes = await apiRequest('/api/memory/stats');
                setMemoryStats(await memRes.json());
            }

        } catch (err) {
            console.error("Failed to fetch data:", err);
        } finally {
            setIsRefreshing(false);
        }
    };

    const handleMemorySearch = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await apiRequest('/api/memory/search', {
                method: 'POST',
                body: JSON.stringify({ query: memoryQuery, top_k: 3 })
            });
            const data = await res.json();
            setMemoryResults(data.results);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 2000);
        return () => clearInterval(interval);
    }, [activeTab]); // Re-fetch when tab changes to update context

    return (
        <div className="flex h-screen bg-aurora-bg overflow-hidden text-gray-200 font-sans selection:bg-aurora-blue/30">

            {/* Sidebar */}
            <div className="w-64 bg-aurora-dark border-r border-white/5 flex flex-col">
                <div className="p-6 flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-aurora-blue to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-aurora-blue/20">
                        <Rocket className="text-white w-6 h-6" />
                    </div>
                    <div>
                        <h1 className="font-bold text-xl text-white tracking-tight">AURORA</h1>
                        <p className="text-xs text-aurora-blue font-medium">v1.2.0 Pro</p>
                    </div>
                </div>

                <div className="px-4 py-2 space-y-2 flex-1">
                    <SidebarItem icon={LayoutDashboard} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
                    <SidebarItem icon={Bot} label="Agents" active={activeTab === 'agents'} onClick={() => setActiveTab('agents')} />
                    <SidebarItem icon={Activity} label="Metrics" active={activeTab === 'metrics'} onClick={() => setActiveTab('metrics')} />
                    <SidebarItem icon={Brain} label="Memory" active={activeTab === 'memory'} onClick={() => setActiveTab('memory')} />

                    <div className="pt-4 mt-2 border-t border-white/5">
                        <SidebarItem icon={Zap} label="Connect Model" active={false} onClick={() => navigate('/connect')} />

                    </div>
                </div>

                <div className="p-4 border-t border-white/5 space-y-4">
                    {/* API Link */}
                    <a href={getApiDocsUrl()} target="_blank" rel="noopener noreferrer"
                        className="flex items-center gap-3 px-4 py-2 bg-aurora-card/50 hover:bg-aurora-card rounded-lg border border-white/5 hover:border-aurora-blue/30 transition-all text-sm text-gray-400 hover:text-white group">
                        <ExternalLink className="w-4 h-4 group-hover:text-aurora-blue" />
                        <span>API Playground</span>
                    </a>

                    <div className="bg-aurora-card rounded-xl p-4 border border-white/5">
                        <div className="flex items-center gap-2 mb-3">
                            <Cpu className="w-4 h-4 text-aurora-blue" />
                            <span className="text-sm font-medium">System Status</span>
                        </div>
                        <div className="space-y-2">
                            <div className="flex justify-between text-xs text-gray-400">
                                <span>CPU Load</span>
                                <span className="text-white">Run Simulation</span>
                            </div>
                            <div className="content-[''] w-full h-1.5 bg-gray-700 rounded-full overflow-hidden">
                                <div className="h-full bg-aurora-blue w-[80%] animate-pulse" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden relative">
                <div className="absolute top-0 left-0 w-full h-96 bg-gradient-to-b from-aurora-blue/5 to-transparent pointer-events-none" />

                {/* Header */}
                <header className="h-16 border-b border-white/5 flex items-center justify-between px-8 bg-aurora-bg/80 backdrop-blur-md z-10">
                    <div className="flex items-center gap-4">
                        <h2 className="text-xl font-semibold text-white capitalize">{activeTab}</h2>
                        <span className="px-3 py-1 bg-aurora-success/10 text-aurora-success text-xs font-medium rounded-full border border-aurora-success/20 flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-aurora-success animate-pulse" />
                            System Online
                        </span>
                    </div>
                    <div className="flex items-center gap-4">
                        <button onClick={fetchData} className="p-2 text-gray-400 hover:text-white transition-colors">
                            <RefreshCw className={clsx("w-5 h-5", isRefreshing && "animate-spin")} />
                        </button>
                        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 border-2 border-aurora-card" />
                    </div>
                </header>

                {/* Dashboard Content */}
                <main className="flex-1 overflow-y-auto p-8 scroll-smooth">
                    <AnimatePresence mode='wait'>

                        {/* --- DASHBOARD TAB --- */}
                        {activeTab === 'dashboard' && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-8">
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                                    {metrics.length > 0 ? metrics.map((m, i) => <MetricCard key={i} metric={m} index={i} />) : <div className="col-span-4 p-8 text-center glass-card"><p className="text-gray-400">Waiting for data stream...</p></div>}
                                </div>
                                <div className="grid grid-cols-1 gap-6">
                                    <div className="glass-card p-6 rounded-2xl h-[400px]">
                                        <h3 className="font-semibold text-white mb-6 flex items-center gap-2"><TrendingUp className="w-5 h-5 text-aurora-blue" /> Real-time Accuracy</h3>
                                        <ResponsiveContainer width="100%" height="85%">
                                            <AreaChart data={chartData}>
                                                <defs>
                                                    <linearGradient id="colorAcc" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#00d4ff" stopOpacity={0.3} /><stop offset="95%" stopColor="#00d4ff" stopOpacity={0} /></linearGradient>
                                                </defs>
                                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                                                <XAxis dataKey="time" stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} />
                                                <YAxis stroke="#6b7280" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                                                <RechartsTooltip contentStyle={{ backgroundColor: '#1a1f3a', border: '1px solid #ffffff20', borderRadius: '8px' }} itemStyle={{ color: '#fff' }} />
                                                <Area type="monotone" dataKey="acc" stroke="#00d4ff" strokeWidth={3} fillOpacity={1} fill="url(#colorAcc)" />
                                            </AreaChart>
                                        </ResponsiveContainer>
                                    </div>
                                </div>
                                <div className="glass-card p-6 rounded-2xl">
                                    <h3 className="font-semibold text-white mb-4">Live Agent Decisions</h3>
                                    <div className="space-y-4">
                                        {decisions.slice(0, 5).map((d, i) => (
                                            <div key={i} className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5">
                                                <div className="flex items-center gap-4">
                                                    <div className={clsx("w-10 h-10 rounded-full flex items-center justify-center", d.approved ? "bg-aurora-success/20 text-aurora-success" : "bg-red-500/20 text-red-500")}>
                                                        {d.approved ? <CheckCircle2 className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
                                                    </div>
                                                    <div>
                                                        <span className="font-semibold text-white mr-2">{d.decision_type}</span>
                                                        <span className="text-xs px-2 py-0.5 rounded-full bg-white/10 text-gray-300">{d.agent_type}</span>
                                                        <p className="text-sm text-gray-400 truncate max-w-xl">{d.reasoning}</p>
                                                    </div>
                                                </div>
                                                <span className="text-sm text-gray-500">{new Date(d.timestamp).toLocaleTimeString()}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </motion.div>
                        )}

                        {/* --- AGENTS TAB --- */}
                        {activeTab === 'agents' && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    {['Planner', 'Critic', 'Executor'].map((name, i) => (
                                        <div key={i} className="glass-card p-6 rounded-2xl border-t-2 border-t-aurora-blue">
                                            <div className="flex items-center justify-between mb-4">
                                                <Bot className="w-8 h-8 text-white" />
                                                <span className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full">Active</span>
                                            </div>
                                            <h3 className="text-lg font-bold text-white mb-1">{name} Agent</h3>
                                            <p className="text-sm text-gray-400">Model: Gemini Pro</p>
                                            <div className="mt-4 pt-4 border-t border-white/10 text-xs text-gray-500">
                                                Last Active: Just now
                                            </div>
                                        </div>
                                    ))}
                                </div>
                                <div className="glass-card p-6 rounded-2xl">
                                    <h3 className="font-semibold text-white mb-4">Full Decision History</h3>
                                    <table className="w-full text-left text-sm text-gray-400">
                                        <thead className="text-xs uppercase bg-white/5 text-gray-300">
                                            <tr><th className="p-3">Time</th><th className="p-3">Agent</th><th className="p-3">Decision</th><th className="p-3">Reasoning</th></tr>
                                        </thead>
                                        <tbody>
                                            {decisions.map((d, i) => (
                                                <tr key={i} className="border-b border-white/5 hover:bg-white/5">
                                                    <td className="p-3">{new Date(d.timestamp).toLocaleString()}</td>
                                                    <td className="p-3">{d.agent_type}</td>
                                                    <td className="p-3 font-medium text-white">{d.decision_type}</td>
                                                    <td className="p-3 truncate max-w-xs">{d.reasoning}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </motion.div>
                        )}

                        {/* --- METRICS TAB --- */}
                        {activeTab === 'metrics' && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card p-6 rounded-2xl">
                                <h3 className="font-semibold text-white mb-4 flex items-center gap-2"><Activity className="w-5 h-5 text-purple-500" /> System Telemetry Log</h3>
                                <div className="overflow-x-auto">
                                    <table className="w-full text-left text-sm text-gray-400">
                                        <thead className="text-xs uppercase bg-white/5 text-gray-300">
                                            <tr><th className="p-3">Time</th><th className="p-3">Model</th><th className="p-3">Accuracy</th><th className="p-3">Latency</th><th className="p-3">Drift</th></tr>
                                        </thead>
                                        <tbody>
                                            {rawMetrics.map((m, i) => (
                                                <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                                    <td className="p-3">{new Date(m.timestamp).toLocaleTimeString()}</td>
                                                    <td className="p-3 font-medium text-white">{m.model_name}</td>
                                                    <td className="p-3">{(m.accuracy * 100).toFixed(1)}%</td>
                                                    <td className="p-3">{m.latency_ms.toFixed(0)} ms</td>
                                                    <td className="p-3">{m.data_drift_score.toFixed(3)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </motion.div>
                        )}

                        {/* --- MEMORY TAB --- */}
                        {activeTab === 'memory' && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                                <div className="glass-card p-6 rounded-2xl bg-gradient-to-r from-aurora-card to-aurora-card/50">
                                    <h3 className="text-xl font-bold text-white mb-2">Neural Memory Bank</h3>
                                    <p className="text-gray-400 mb-6">Search the RAG (Retrieval Augmented Generation) store for past incidents.</p>

                                    <form onSubmit={handleMemorySearch} className="relative max-w-2xl">
                                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
                                        <input
                                            type="text"
                                            value={memoryQuery}
                                            onChange={(e) => setMemoryQuery(e.target.value)}
                                            placeholder="E.g., 'accuracy drop recommendation model'..."
                                            className="w-full bg-aurora-bg border border-white/10 rounded-xl py-4 pl-12 pr-4 text-white focus:outline-none focus:border-aurora-blue/50 focus:ring-1 focus:ring-aurora-blue/50"
                                        />
                                        <button type="submit" className="absolute right-2 top-2 bg-aurora-blue text-aurora-bg font-semibold px-4 py-2 rounded-lg hover:bg-cyan-300 transition-colors">
                                            Search Memory
                                        </button>
                                    </form>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="glass-card p-6 rounded-2xl">
                                        <h4 className="font-semibold text-white mb-4 flex items-center gap-2"><Database className="w-4 h-4 text-aurora-blue" /> Search Results</h4>
                                        <div className="space-y-3">
                                            {memoryResults.length > 0 ? memoryResults.map((r: any, i) => (
                                                <div key={i} className="p-3 bg-white/5 rounded-lg border border-white/5">
                                                    <p className="text-sm text-gray-300">{r.text || r.content || JSON.stringify(r)}</p>
                                                    <div className="mt-2 text-xs text-aurora-blue">Simulated Match Score: {(0.9 - i * 0.1).toFixed(2)}</div>
                                                </div>
                                            )) : <p className="text-gray-500 text-sm">Enter a query to search vector store.</p>}
                                        </div>
                                    </div>
                                    <div className="glass-card p-6 rounded-2xl">
                                        <h4 className="font-semibold text-white mb-4 flex items-center gap-2"><Command className="w-4 h-4 text-purple-500" /> Memory Stats</h4>
                                        {memoryStats ? (
                                            <div className="space-y-4">
                                                <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                                                    <span className="text-gray-400">Total Memories</span>
                                                    <span className="text-2xl font-bold text-white">{memoryStats.count || memoryStats.total_vectors || 5}</span>
                                                </div>
                                                <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                                                    <span className="text-gray-400">Vector Dimension</span>
                                                    <span className="text-xl font-bold text-white">768</span>
                                                </div>
                                                <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                                                    <span className="text-gray-400">Index Type</span>
                                                    <span className="text-xl font-bold text-white">FAISS (Flat)</span>
                                                </div>
                                            </div>
                                        ) : <p className="text-gray-500">Loading stats...</p>}
                                    </div>
                                </div>
                            </motion.div>
                        )}

                    </AnimatePresence>
                </main>
            </div>
        </div>
    );
}
