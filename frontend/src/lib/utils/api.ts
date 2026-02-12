export type RequestOptions = {
	method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
	data?: Record<string, any> | FormData;
	token?: string;
	headers?: Record<string, string>;
};

export async function theBlueAllianceApiFetch<T = any>(url: string) {
	const response = await fetch(`/internal/tba/${url}`);
	return response.json() as Promise<T>;
}

