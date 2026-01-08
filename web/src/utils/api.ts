/**
 * API Configuration Utility
 * Automatically detects the correct API URL based on environment
 */

/**
 * Get the base API URL
 * - In development: uses Vite proxy (relative URLs)
 * - In production: uses the same origin as the frontend
 */
export const getApiUrl = (): string => {
    // Check if we have an environment variable override
    const envApiUrl = import.meta.env.VITE_API_URL;
    if (envApiUrl) {
        return envApiUrl;
    }

    // In production (built app), use relative URLs
    // This works because nginx proxies /api to the backend
    if (import.meta.env.PROD) {
        return window.location.origin;
    }

    // In development, use relative URLs (Vite proxy handles it)
    return '';
};

/**
 * Make an API request with automatic URL resolution
 */
export const apiRequest = async (
    endpoint: string,
    options?: RequestInit
): Promise<Response> => {
    const baseUrl = getApiUrl();
    const url = `${baseUrl}${endpoint}`;

    return fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
        },
    });
};

/**
 * Get the API docs URL
 */
export const getApiDocsUrl = (): string => {
    const baseUrl = getApiUrl();
    return `${baseUrl}/docs`;
};

/**
 * Check if the API is healthy
 */
export const checkApiHealth = async (): Promise<boolean> => {
    try {
        const response = await apiRequest('/health');
        return response.ok;
    } catch (error) {
        console.error('API health check failed:', error);
        return false;
    }
};

export default {
    getApiUrl,
    apiRequest,
    getApiDocsUrl,
    checkApiHealth,
};
