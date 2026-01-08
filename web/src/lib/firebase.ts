import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDwUwwPTYjavLyUqXnDd0EYzvJ24K0V0rs",
    authDomain: "aurora-259bb.firebaseapp.com",
    projectId: "aurora-259bb",
    storageBucket: "aurora-259bb.firebasestorage.app",
    messagingSenderId: "5987069700",
    appId: "1:5987069700:web:f054becce1cb5e8023aa51",
    measurementId: "G-KRKVPNH1F7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
