import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
    apiKey: "AIzaSyBQfJJGZJVxGJCJmZJVxGJCJmZJVxGJCJm",
    authDomain: "aurora-expense-tracker.firebaseapp.com",
    projectId: "aurora-expense-tracker",
    storageBucket: "aurora-expense-tracker.appspot.com",
    messagingSenderId: "123456789012",
    appId: "1:123456789012:web:abcdef123456"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
