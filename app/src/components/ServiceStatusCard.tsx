import { ActivityIndicator, Pressable, Text, View } from "react-native";

import { useServiceStatus } from "../hooks/useServiceStatus";

const SERVICE_LABELS: Record<string, string> = {
  weather: "Weather Monitoring",
  action: "Action Suggestion",
  coordination: "Coordination",
  learning: "Learning",
};

export default function ServiceStatusCard() {
  const { status, error, loading, refresh } = useServiceStatus();

  return (
    <View className="rounded-2xl bg-white p-4 shadow-sm">
      <View className="flex-row items-center justify-between">
        <Text className="text-lg font-semibold text-slate-900">System status</Text>
        <Pressable onPress={refresh} className="rounded-full bg-brand px-3 py-1">
          <Text className="text-sm font-medium text-white">Refresh</Text>
        </Pressable>
      </View>

      {loading ? <ActivityIndicator className="mt-4" /> : null}

      {error ? (
        <Text className="mt-3 text-alert-extreme">{error}</Text>
      ) : null}

      {status
        ? Object.entries(status).map(([name, state]) => (
            <View key={name} className="mt-3 flex-row items-center">
              <View
                className={state === "up" ? "h-3 w-3 rounded-full bg-alert-low" : "h-3 w-3 rounded-full bg-alert-extreme"}
              />
              <Text className="ml-3 text-base text-slate-800">{SERVICE_LABELS[name] ?? name}</Text>
              <Text className="ml-auto text-sm text-slate-500">{state}</Text>
            </View>
          ))
        : null}
    </View>
  );
}
