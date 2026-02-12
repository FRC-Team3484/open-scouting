import { env } from "$env/dynamic/public";

export const getAuthToken = () => localStorage.getItem('access_token');

export const customInstance = async <T>(
    url: string,
    {
        method,
        headers,
        params,
        body,
    }: {
        method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
        headers?: HeadersInit;
        params?: Record<string, string>;
        body?: BodyType<unknown>;
    }
    ): Promise<{ data: T; status: number; headers: Headers }> => {
    let targetUrl = `${env.PUBLIC_FAST_API_URL}${url}`;

    if (params) {
        targetUrl += '?' + new URLSearchParams(params);
    }

    const token = getAuthToken();

    const finalHeaders: HeadersInit = {
        ...(headers ?? {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };

    const response = await fetch(targetUrl, {
        method,
        headers: finalHeaders,
        body,
    });

    const text = [204, 205, 304].includes(response.status) ? null : await response.text();

    const data: T = text ? JSON.parse(text) : ({} as T);

    return {
        data,
        status: response.status,
        headers: response.headers,
    };
};

export default customInstance;

// Override the return error type for react-query and swr
export type ErrorType<Error> = AxiosError<Error>;

// Wrap the body type if needed (e.g., for case transformation)
export type BodyType<BodyData> = CamelCase<BodyData>;