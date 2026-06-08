import { env } from "$env/dynamic/public";

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


    const finalHeaders: HeadersInit = {
        ...(headers ?? {}),
    };

    // TODO: Make less hacky
    const includeCredentials = targetUrl.includes(`/auth/me`) || targetUrl.includes(`/auth/login`) ? false : true;

    const response = await fetch(targetUrl, {
        method,
        headers: finalHeaders,
        body,
        credentials: includeCredentials ? 'include' : 'omit',
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