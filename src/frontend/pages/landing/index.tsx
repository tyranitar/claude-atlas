import { Card, Input } from "antd";
import { useState } from "react";

const styles = require("./index.module.scss");

export default function LandingPage() {
  const [dest, setDest] = useState("");

  return (
    <div className={styles.LandingPage}>
      <Card className={styles["card"]}>
        <div className={styles["card-body"]}>
          <div>Where do you want to travel to?</div>
          <Input value={dest} onChange={(evt) => setDest(evt.target.value)} />
        </div>
      </Card>
    </div>
  );
}
