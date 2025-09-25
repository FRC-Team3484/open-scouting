import { PUBLIC_FAST_API_URL } from "$env/static/public";

export type RequestOptions = {
	method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
	data?: Record<string, any> | FormData;
	token?: string;
	headers?: Record<string, string>;
};

export async function apiFetch<T = any>(
	url: string,
	{ method = "GET", data, token, headers = {} }: RequestOptions = {}): Promise<T> {
	let body: BodyInit | undefined;
	let contentType: string | undefined;

	if (data instanceof FormData) {
		body = data;
	} else if (data !== undefined) {
		body = JSON.stringify(data);
		contentType = "application/json";
	}

	const response = await fetch(PUBLIC_FAST_API_URL + url, {
		method,
		body: method === "GET" ? undefined : body,
		headers: {
			...(contentType ? { "Content-Type": contentType } : {}),
			...(token ? { Authorization: `Bearer ${token}` } : {}),
			...headers
		}
	});

	if (!response.ok) {
		let errorMsg;
		try {
			const errData = await response.json();
			errorMsg = errData.detail || JSON.stringify(errData);
		} catch {
			errorMsg = await response.text();
		}
		throw new Error(errorMsg || `Request failed: ${response.status}`);
	}

	const contentTypeResp = response.headers.get("content-type");
	if (contentTypeResp?.includes("application/json")) {
		return response.json() as Promise<T>;
	} else {
		return (response.text() as unknown) as T;
	}
}
