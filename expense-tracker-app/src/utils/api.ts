export async function apiRequest(endpoint: string, options: RequestInit = {}) {
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };

    const response = await fetch(endpoint, {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    });

    if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
    }

    return response;
}
