const API_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:8000";
const REQUEST_TIMEOUT_MS = 8000;

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { "Content-Type": "application/json", ...(options.headers as Record<string, string>) },
      signal: controller.signal,
    });
  } catch {
    throw new ApiError("Cannot reach the WarnX server", 0);
  } finally {
    clearTimeout(timer);
  }

  if (!response.ok) {
    let message = "Something went wrong";
    try {
      const body = await response.json();
      message = body.error ?? message;
    } catch {}
    throw new ApiError(message, response.status);
  }

  return response.json() as Promise<T>;
}
