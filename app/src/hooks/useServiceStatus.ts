import { useCallback, useEffect, useState } from "react";

import { getServiceStatus, ServiceStatus } from "../api/status";

export function useServiceStatus() {
  const [status, setStatus] = useState<ServiceStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      setStatus(await getServiceStatus());
      setError(null);
    } catch (e) {
      setStatus(null);
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { status, error, loading, refresh };
}
