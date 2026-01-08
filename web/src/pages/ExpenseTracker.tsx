import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    DollarSign, TrendingUp, TrendingDown, PieChart, Calendar,
    Plus, Trash2, Mail, Bell, AlertCircle, CheckCircle2, Wallet
} from 'lucide-react';
import { BarChart, Bar, PieChart as RechartsPie, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import clsx from 'clsx';
import { apiRequest } from '../utils/api';

interface Expense {
    id: number;
    amount: number;
    category: string;
    description: string;
    date: string;
    aiSuggestion?: string;
}

interface Budget {
    category: string;
    limit: number;
    spent: number;
    percentage: number;
}

const COLORS = ['#00d4ff', '#a855f7', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const CATEGORIES = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Bills & Utilities',
    'Healthcare',
    'Other'
];

export default function ExpenseTracker() {
    const [expenses, setExpenses] = useState<Expense[]>([]);
    const [budgets, setBudgets] = useState<Budget[]>([]);
    const [totalSpent, setTotalSpent] = useState(0);
    const [monthlyBudget, setMonthlyBudget] = useState(5000);

    // Form states
    const [showAddExpense, setShowAddExpense] = useState(false);
    const [amount, setAmount] = useState('');
    const [category, setCategory] = useState(CATEGORIES[0]);
    const [description, setDescription] = useState('');

    // User email from Firebase Auth
    const [userEmail, setUserEmail] = useState('');
    const [notifications, setNotifications] = useState<any[]>([]);

    useEffect(() => {
        // Get user email from localStorage (set during Firebase login)
        const email = localStorage.getItem('userEmail') || 'user@example.com';
        setUserEmail(email);

        fetchExpenses();
        fetchBudgets();
    }, []);

    const fetchExpenses = async () => {
        try {
            const res = await apiRequest('/api/expenses');
            const data = await res.json();
            setExpenses(data.expenses || []);

            // Calculate total spent
            const total = (data.expenses || []).reduce((sum: number, exp: Expense) => sum + exp.amount, 0);
            setTotalSpent(total);
        } catch (err) {
            console.error('Failed to fetch expenses:', err);
        }
    };

    const fetchBudgets = async () => {
        try {
            const res = await apiRequest('/api/budgets');
            const data = await res.json();
            setBudgets(data.budgets || []);
        } catch (err) {
            console.error('Failed to fetch budgets:', err);
        }
    };

    const addExpense = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!amount || !description) {
            alert('Please fill all fields');
            return;
        }

        try {
            const newExpense = {
                amount: parseFloat(amount),
                category,
                description,
                date: new Date().toISOString(),
                userEmail // Send user email for n8n workflow
            };

            const res = await apiRequest('/api/expenses', {
                method: 'POST',
                body: JSON.stringify(newExpense)
            });

            const data = await res.json();

            // Check if budget exceeded and notification sent
            if (data.budgetExceeded) {
                setNotifications(prev => [...prev, {
                    type: 'warning',
                    message: `Budget exceeded for ${category}! Email sent to ${userEmail}`,
                    timestamp: new Date().toISOString()
                }]);
            }

            // Reset form
            setAmount('');
            setDescription('');
            setShowAddExpense(false);

            // Refresh data
            fetchExpenses();
            fetchBudgets();
        } catch (err) {
            console.error('Failed to add expense:', err);
            alert('Failed to add expense');
        }
    };

    const deleteExpense = async (id: number) => {
        try {
            await apiRequest(`/api/expenses/${id}`, { method: 'DELETE' });
            fetchExpenses();
            fetchBudgets();
        } catch (err) {
            console.error('Failed to delete expense:', err);
        }
    };

    // Calculate category breakdown for pie chart
    const categoryData = CATEGORIES.map(cat => {
        const total = expenses
            .filter(exp => exp.category === cat)
            .reduce((sum, exp) => sum + exp.amount, 0);
        return { name: cat, value: total };
    }).filter(item => item.value > 0);

    const budgetPercentage = (totalSpent / monthlyBudget) * 100;

    return (
        <div className="min-h-screen bg-aurora-bg text-white p-8">
            <div className="max-w-7xl mx-auto space-y-8">

                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex items-center justify-between"
                >
                    <div>
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-aurora-blue to-purple-500 bg-clip-text text-transparent">
                            Smart Expense Tracker
                        </h1>
                        <p className="text-gray-400 mt-2">AI-powered insights • Budget alerts via email</p>
                        <p className="text-sm text-aurora-blue mt-1">Logged in as: {userEmail}</p>
                    </div>
                    <button
                        onClick={() => setShowAddExpense(true)}
                        className="flex items-center gap-2 bg-gradient-to-r from-aurora-blue to-purple-600 px-6 py-3 rounded-xl font-semibold hover:shadow-lg hover:shadow-aurora-blue/30 transition-all"
                    >
                        <Plus className="w-5 h-5" />
                        Add Expense
                    </button>
                </motion.div>

                {/* Notifications */}
                <AnimatePresence>
                    {notifications.map((notif, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, x: 100 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 100 }}
                            className="glass-card p-4 rounded-xl border-l-4 border-orange-500 flex items-center gap-3"
                        >
                            <AlertCircle className="w-5 h-5 text-orange-500" />
                            <div className="flex-1">
                                <p className="text-white font-medium">{notif.message}</p>
                                <p className="text-xs text-gray-400">{new Date(notif.timestamp).toLocaleString()}</p>
                            </div>
                            <Mail className="w-5 h-5 text-aurora-blue animate-pulse" />
                        </motion.div>
                    ))}
                </AnimatePresence>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <Wallet className="w-8 h-8 text-aurora-blue" />
                            <span className="text-xs px-2 py-1 bg-aurora-blue/20 text-aurora-blue rounded-full">This Month</span>
                        </div>
                        <h3 className="text-gray-400 text-sm">Total Spent</h3>
                        <p className="text-3xl font-bold text-white mt-2">${totalSpent.toFixed(2)}</p>
                        <p className={clsx("text-sm mt-2", budgetPercentage > 100 ? "text-red-400" : "text-aurora-success")}>
                            {budgetPercentage.toFixed(1)}% of ${monthlyBudget} budget
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <TrendingUp className="w-8 h-8 text-green-500" />
                            <span className="text-xs px-2 py-1 bg-green-500/20 text-green-400 rounded-full">Active</span>
                        </div>
                        <h3 className="text-gray-400 text-sm">Total Expenses</h3>
                        <p className="text-3xl font-bold text-white mt-2">{expenses.length}</p>
                        <p className="text-sm text-gray-400 mt-2">Tracked this month</p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <Bell className="w-8 h-8 text-purple-500" />
                            <span className="text-xs px-2 py-1 bg-purple-500/20 text-purple-400 rounded-full">n8n Active</span>
                        </div>
                        <h3 className="text-gray-400 text-sm">Email Alerts</h3>
                        <p className="text-3xl font-bold text-white mt-2">{notifications.length}</p>
                        <p className="text-sm text-gray-400 mt-2">Sent to {userEmail}</p>
                    </motion.div>
                </div>

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Category Breakdown */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <PieChart className="w-5 h-5 text-aurora-blue" />
                            Category Breakdown
                        </h3>
                        <ResponsiveContainer width="100%" height={300}>
                            <RechartsPie>
                                <Pie
                                    data={categoryData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                                    outerRadius={100}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {categoryData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </RechartsPie>
                        </ResponsiveContainer>
                    </motion.div>

                    {/* Budget Status */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="glass-card p-6 rounded-2xl"
                    >
                        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                            <TrendingDown className="w-5 h-5 text-purple-500" />
                            Budget Status
                        </h3>
                        <div className="space-y-4">
                            {budgets.map((budget, idx) => (
                                <div key={idx} className="space-y-2">
                                    <div className="flex justify-between text-sm">
                                        <span className="text-gray-300">{budget.category}</span>
                                        <span className={clsx(
                                            "font-semibold",
                                            budget.percentage > 100 ? "text-red-400" : "text-aurora-success"
                                        )}>
                                            ${budget.spent.toFixed(2)} / ${budget.limit}
                                        </span>
                                    </div>
                                    <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                                        <div
                                            className={clsx(
                                                "h-full transition-all duration-500",
                                                budget.percentage > 100 ? "bg-red-500" : "bg-aurora-blue"
                                            )}
                                            style={{ width: `${Math.min(budget.percentage, 100)}%` }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                </div>

                {/* Recent Expenses */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-6 rounded-2xl"
                >
                    <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                        <Calendar className="w-5 h-5 text-aurora-blue" />
                        Recent Expenses
                    </h3>
                    <div className="space-y-3">
                        {expenses.slice(0, 10).map((expense) => (
                            <div
                                key={expense.id}
                                className="flex items-center justify-between p-4 bg-white/5 rounded-xl border border-white/5 hover:bg-white/10 transition-all group"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-aurora-blue to-purple-600 flex items-center justify-center">
                                        <DollarSign className="w-6 h-6 text-white" />
                                    </div>
                                    <div>
                                        <p className="font-semibold text-white">{expense.description}</p>
                                        <p className="text-sm text-gray-400">{expense.category} • {new Date(expense.date).toLocaleDateString()}</p>
                                        {expense.aiSuggestion && (
                                            <p className="text-xs text-aurora-blue mt-1">💡 AI: {expense.aiSuggestion}</p>
                                        )}
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    <span className="text-xl font-bold text-white">${expense.amount.toFixed(2)}</span>
                                    <button
                                        onClick={() => deleteExpense(expense.id)}
                                        className="opacity-0 group-hover:opacity-100 p-2 text-red-400 hover:bg-red-500/20 rounded-lg transition-all"
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.div>

                {/* Add Expense Modal */}
                <AnimatePresence>
                    {showAddExpense && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
                            onClick={() => setShowAddExpense(false)}
                        >
                            <motion.div
                                initial={{ scale: 0.9, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                exit={{ scale: 0.9, opacity: 0 }}
                                className="glass-card p-8 rounded-2xl max-w-md w-full"
                                onClick={(e) => e.stopPropagation()}
                            >
                                <h2 className="text-2xl font-bold text-white mb-6">Add New Expense</h2>
                                <form onSubmit={addExpense} className="space-y-4">
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Amount ($)</label>
                                        <input
                                            type="number"
                                            step="0.01"
                                            value={amount}
                                            onChange={(e) => setAmount(e.target.value)}
                                            className="w-full bg-aurora-bg border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-aurora-blue"
                                            placeholder="0.00"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Category</label>
                                        <select
                                            value={category}
                                            onChange={(e) => setCategory(e.target.value)}
                                            className="w-full bg-aurora-bg border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-aurora-blue"
                                        >
                                            {CATEGORIES.map(cat => (
                                                <option key={cat} value={cat}>{cat}</option>
                                            ))}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="block text-sm text-gray-400 mb-2">Description</label>
                                        <input
                                            type="text"
                                            value={description}
                                            onChange={(e) => setDescription(e.target.value)}
                                            className="w-full bg-aurora-bg border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-aurora-blue"
                                            placeholder="What did you spend on?"
                                            required
                                        />
                                    </div>
                                    <div className="flex gap-3 pt-4">
                                        <button
                                            type="button"
                                            onClick={() => setShowAddExpense(false)}
                                            className="flex-1 px-4 py-3 bg-white/5 text-white rounded-xl hover:bg-white/10 transition-all"
                                        >
                                            Cancel
                                        </button>
                                        <button
                                            type="submit"
                                            className="flex-1 px-4 py-3 bg-gradient-to-r from-aurora-blue to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-aurora-blue/30 transition-all"
                                        >
                                            Add Expense
                                        </button>
                                    </div>
                                </form>
                            </motion.div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
