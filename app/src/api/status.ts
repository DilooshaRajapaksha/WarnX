import { apiRequest } from "./client";

export type ServiceStatus = Record<string, "up" | "down">;

export function getServiceStatus() {
  return apiRequest<ServiceStatus>("/api/status");
}
