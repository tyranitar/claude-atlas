import { QuestCard } from "components/QuestCard";
import { Card, theme } from "antd";

const { useToken } = theme;

const styles = require("./index.module.scss");

export default function ItineraryPage() {
  const { token } = useToken();

  return (
    <div className={styles.ItineraryPage}>
      <div
        className={styles["sidebar"]}
        style={{ backgroundColor: token.colorPrimary }}
      >
        <div>Your trip to Florence</div>
      </div>
      <div className={styles["left-column"]}>
        <div className={styles["itinerary"]}>
          <Card className={styles["card"]}>
            <QuestCard>
              <div>Test</div>
            </QuestCard>
            <QuestCard>
              <div>Test</div>
            </QuestCard>
            <QuestCard>
              <div>Test</div>
            </QuestCard>
            <QuestCard>
              <div>Test</div>
            </QuestCard>
            <QuestCard>
              <div>Test</div>
            </QuestCard>
          </Card>
        </div>
      </div>
      <div className={styles["right-column"]}>
        <div className={styles["map"]}>
          <Card className={styles["card"]}>Test</Card>
        </div>
        <div className={styles["chat"]}>
          <Card className={styles["card"]}>Test</Card>
        </div>
      </div>
      <div className={styles["sidebar"]}>{/* <div>Your </div> */}</div>
    </div>
  );
}
