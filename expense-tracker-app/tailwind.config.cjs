/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'aurora-bg': '#0a0e27',
                'aurora-blue': '#00d4ff',
                'aurora-purple': '#a855f7',
                'aurora-success': '#10b981',
            },
        },
    },
    plugins: [],
}
