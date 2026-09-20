import { ReactNode } from "react";
import { ScrollView, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

type Props = {
  title: string;
  subtitle?: string;
  children?: ReactNode;
};

export default function ScreenContainer({ title, subtitle, children }: Props) {
  const insets = useSafeAreaInsets();

  return (
    <View className="flex-1 bg-slate-50" style={{ paddingTop: insets.top }}>
      <ScrollView contentContainerStyle={{ padding: 20, gap: 16 }}>
        <View>
          <Text className="text-3xl font-bold text-slate-900">{title}</Text>
          {subtitle ? <Text className="mt-1 text-base text-slate-600">{subtitle}</Text> : null}
        </View>
        {children}
      </ScrollView>
    </View>
  );
}
