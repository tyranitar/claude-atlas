import { SyncOutlined } from "@ant-design/icons";
import { Button, Card, Typography, theme } from "antd";
import { QuestCard } from "components/QuestCard";

const styles = require("./index.module.scss");

const { useToken } = theme;

function RegenerateOptions() {
  return (
    <div className={styles.RegenerateOptions}>
      <div>{"🤔 Don't like any of the options?"}</div>
      <Button icon={<SyncOutlined />} type="primary">
        {"Give me new recommendations"}
      </Button>
    </div>
  );
}

export default function MainQuestsPage() {
  const { token } = useToken();

  return (
    <div className={styles["MainQuestsPage"]}>
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
      <RegenerateOptions />
    </div>
  );
}
