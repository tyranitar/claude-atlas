import { Button, Card, Input, theme } from "antd";
import { useRouter } from "next/router";
import { useState } from "react";

const styles = require("./index.module.scss");

const { useToken } = theme;

export default function LandingPage() {
  const [dest, setDest] = useState("");
  const { token } = useToken();
  const router = useRouter();

  const callback = () => {
    router.push(`/main-quests?location=${encodeURIComponent(dest)}`);
  };

  return (
    <div className={styles.LandingPage}>
      <Card className={styles["card"]}>
        <div
          className={styles["card-body"]}
          onKeyDown={(evt) => {
            if (evt.key !== "Enter") {
              return;
            }

            callback();
          }}
        >
          <div
            style={{
              color: token.colorPrimary,
              fontSize: "32px",
              textAlign: "center",
            }}
          >
            🪄 ClaudeWander
          </div>
          <div style={{ textAlign: "center" }}>
            Where do you want to travel to?
          </div>
          <Input value={dest} onChange={(evt) => setDest(evt.target.value)} />
          <Button type="primary" block onClick={callback}>
            Show me some itineraries!
          </Button>
        </div>
      </Card>
    </div>
  );
}
