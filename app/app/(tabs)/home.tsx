import ScreenContainer from "../../src/components/ScreenContainer";
import ServiceStatusCard from "../../src/components/ServiceStatusCard";

export default function HomeScreen() {
  return (
    <ScreenContainer title="WarnX" subtitle="Predict → Alert → Community → Recover">
      <ServiceStatusCard />
    </ScreenContainer>
  );
}
