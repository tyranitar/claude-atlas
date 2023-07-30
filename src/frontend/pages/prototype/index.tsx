import { Button, Card, Typography, theme } from "antd";
import { QuestCard } from "components/QuestCard";

const styles = require("./index.module.scss");

const { useToken } = theme;

export default function PrototypePage() {
  const { token } = useToken();

  return (
    <div className={styles["PrototypePage"]}>
      <div className={styles["header"]} style={{ color: token.colorPrimary }}>
        Choose your main quest
      </div>
      <div className={styles["quests"]}>
        <QuestCard>
          <div className={styles["card-content"]}>
            <div className={styles["description"]}>Description</div>
            <Button type="primary" block>
              {"Let's go with this!"}
            </Button>
          </div>
        </QuestCard>
        <QuestCard>
          <div className={styles["card-content"]}>
            <div className={styles["description"]}>Description</div>
            <Button type="primary" block>
              {"Let's go with this!"}
            </Button>
          </div>
        </QuestCard>
        <QuestCard>
          <div className={styles["card-content"]}>
            <div className={styles["description"]}>Description</div>
            <Button type="primary" block>
              {"Let's go with this!"}
            </Button>
          </div>
        </QuestCard>
      </div>
    </div>
  );
}
