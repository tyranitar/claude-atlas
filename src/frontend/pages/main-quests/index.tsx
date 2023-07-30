import { LoadingOutlined, SyncOutlined } from "@ant-design/icons";
import { Button, Card, Typography, theme } from "antd";
import { QuestCard } from "components/QuestCard";
import { useRouter } from "next/router";
import { useEffect } from "react";
import { getStore } from "store/accessor";
import {
  updateQueryData,
  useLazyMainQuestsQuery,
  useMainQuestsQuery,
} from "store/services/quests";

const styles = require("./index.module.scss");

const { useToken } = theme;

function RegenerateOptions({ questNames }: { questNames?: string[] }) {
  const [trigger, { isLoading }] = useLazyMainQuestsQuery();

  return (
    <div className={styles.RegenerateOptions}>
      <div>{"🤔 Don't like any of the options?"}</div>
      <Button
        // icon={<SyncOutlined />}
        loading={isLoading}
        onClick={async () => {
          const loc = new URLSearchParams(location.search).get("location")!;

          const result = await trigger({ location: loc, questNames });

          if ("error" in result) {
            return;
          }

          getStore().dispatch(
            updateQueryData("mainQuests", { location: loc }, () => result.data)
          );
        }}
      >
        {"Give me new recommendations"}
      </Button>
    </div>
  );
}

export default function MainQuestsPage() {
  const [trigger, { data: quests, isLoading }] = useLazyMainQuestsQuery();

  const { token } = useToken();
  const router = useRouter();

  useEffect(() => {
    trigger({
      location: new URLSearchParams(location.search).get("location")!,
    });
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
                    <div style={{ fontSize: "20px" }}>{name}</div>
                    <div className={styles["fun-facts"]}>
                      <ul style={{ paddingInlineStart: "20px" }}>
                        {funFacts.map((funFact, idx) => (
                          <li key={idx}>{funFact}</li>
                        ))}
                      </ul>
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
          <RegenerateOptions questNames={quests?.map(({ name }) => name)} />
        </>
      )}
      <div
        className={styles["background"]}
        style={{ backgroundColor: token.colorPrimary }}
      ></div>
    </div>
  );
}
