import router from '@/router';

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

function getAuthHeaders(headers = {}) {
    const token = localStorage.getItem('access_token');

    return {
        ...headers,
        'Authorization': `Bearer ${token}`,
    };
}

export async function getRequest(endPoint, headers = {}) {
    const url = `${BASE_URL}${endPoint}`;
    const options = {
        method: 'GET',
        headers: getAuthHeaders(headers),
    };

    return handleResponse(await fetch(url, options));
}

export async function postRequest(endPoint, body = {}, headers = {}) {
    const url = `${BASE_URL}${endPoint}`;
    const options = {
        method: 'POST',
        headers: {
        ...getAuthHeaders(headers),
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
    };

    return handleResponse(await fetch(url, options));
}

export async function putRequest(endPoint, body = {}, headers = {}) {
    const url = `${BASE_URL}${endPoint}`;
    const options = {
        method: 'PUT',
        headers: {
        ...getAuthHeaders(headers),
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
    };

    return handleResponse(await fetch(url, options));
}

export async function deleteRequest(endPoint, headers = {}) {
    const url = `${BASE_URL}${endPoint}`;
    const options = {
        method: 'DELETE',
        headers: getAuthHeaders(headers),
    };

    return handleResponse(await fetch(url, options));
}

async function handleResponse(response) {
    if (response.status === 401) {
        router.push({ name: 'login' });
        throw new Error('Unauthorized');
    }

    if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
    }

    return response.json();
}
