import { LoadingOutlined, SyncOutlined } from "@ant-design/icons";
import { Button, Card, Typography, theme } from "antd";
import { QuestCard } from "components/QuestCard";
import { useRouter } from "next/router";
import { useEffect } from "react";
import {
  useLazyMainQuestsQuery,
  useMainQuestsQuery,
} from "store/services/quests";

const styles = require("./index.module.scss");

const { useToken } = theme;

function RegenerateOptions() {
  return (
    <div className={styles.RegenerateOptions}>
      <div>{"🤔 Don't like any of the options?"}</div>
      <Button icon={<SyncOutlined />}>{"Give me new recommendations"}</Button>
    </div>
  );
}

export default function MainQuestsPage() {
  const [trigger, { data: quests, isLoading }] = useLazyMainQuestsQuery();

  const { token } = useToken();
  const router = useRouter();

  useEffect(() => {
    trigger(new URLSearchParams(location.search).get("location")!);
  }, [trigger]);

  return (
    <div className={styles["MainQuestsPage"]}>
      <div className={styles["header"]} style={{ color: token.colorPrimary }}>
        Choose your main quest
      </div>
      {isLoading ? (
        <div className={styles["loading-container"]}>
          <Card>
            <div>{"Generating travel recommendations..."}</div>
            <div
              className={styles["loading-icon"]}
              style={{ color: token.colorPrimary }}
            >
              <LoadingOutlined />
            </div>
          </Card>
        </div>
      ) : (
        <>
          <div className={styles["quests"]}>
            {quests?.map(({ imageUrl, name, funFacts }, idx) => (
              <QuestCard imageSrc={imageUrl} key={idx}>
                <div className={styles["card-container"]}>
                  <div className={styles["card-content"]}>
                    <div>{name}</div>
                    <div className={styles["fun-facts"]}>
                      {funFacts.map((funFact, idx) => (
                        <div key={idx}>{funFact}</div>
                      ))}
                    </div>
                  </div>
                  <div className={styles["card-footer"]}>
                    <Button
                      type="primary"
                      block
                      onClick={() => {
                        const params = new URLSearchParams(location.search);
                        const loc = params.get("location")!;

                        router.push(
                          `/itinerary?location=${encodeURIComponent(
                            loc
                          )}&quest=${encodeURIComponent(name)}`
                        );
                      }}
                    >
                      {"Let's go with this!"}
                    </Button>
                  </div>
                </div>
              </QuestCard>
            ))}
            {/* <QuestCard>
              <div className={styles["card-content"]}>
                <div className={styles["description"]}>Description</div>
                <Button
                  // loading={isLoading}
                  type="primary"
                  block
                  // onClick={() => {
                  //   trigger("San Francisco");
                  // }}
                >
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
            </QuestCard> */}
          </div>
          <RegenerateOptions />
        </>
      )}
      <div
        className={styles["background"]}
        style={{ backgroundColor: token.colorPrimary }}
      ></div>
    </div>
  );
}
