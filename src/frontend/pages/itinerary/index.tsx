import { QuestCard } from "components/QuestCard";
import { Card, theme } from "antd";
import { useLazyItineraryQuery } from "store/services/quests";
import GoogleMapReact from "google-map-react";
import { useEffect, useState } from "react";

const { useToken } = theme;

const styles = require("./index.module.scss");

const AnyReactComponent = ({ index }: { index: number }) => {
  const { token } = useToken();

  return (
    <div
      className={styles["point"]}
      style={{ border: `2px solid ${token.colorPrimary}` }}
    >
      {index}
    </div>
  );
};

export default function ItineraryPage() {
  const [trigger, { data, isLoading, error }] = useLazyItineraryQuery();
  const [quest, setQuest] = useState("");
  const [loc, setLoc] = useState("");
  const { token } = useToken();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const loc = params.get("location")!;
    const quest = params.get("quest")!;

    setQuest(quest);
    setLoc(loc);

    trigger({
      location: loc,
      quest,
    });
  }, [trigger]);

  return (
    <div className={styles.ItineraryPage}>
      <div
        className={styles["sidebar"]}
        style={{ backgroundColor: token.colorPrimary }}
      >
        <div>Your trip to {loc}</div>
        <div>{quest}</div>
      </div>
      <div className={styles["left-column"]}>
        <div className={styles["itinerary"]}>
          <Card className={styles["card"]}>
            <QuestCard imageSrc="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/33/dc/8a/caption.jpg?w=700&h=-1&s=1">
              <div>Test</div>
            </QuestCard>
            <QuestCard imageSrc="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/33/dc/8a/caption.jpg?w=700&h=-1&s=1">
              <div>Test</div>
            </QuestCard>
            <QuestCard imageSrc="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/33/dc/8a/caption.jpg?w=700&h=-1&s=1">
              <div>Test</div>
            </QuestCard>
            <QuestCard imageSrc="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/33/dc/8a/caption.jpg?w=700&h=-1&s=1">
              <div>Test</div>
            </QuestCard>
            <QuestCard imageSrc="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/33/dc/8a/caption.jpg?w=700&h=-1&s=1">
              <div>Test</div>
            </QuestCard>
            <QuestCard imageSrc="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/33/dc/8a/caption.jpg?w=700&h=-1&s=1">
              <div>Test</div>
            </QuestCard>
            <QuestCard imageSrc="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/33/dc/8a/caption.jpg?w=700&h=-1&s=1">
              <div>Test</div>
            </QuestCard>
          </Card>
        </div>
      </div>
      <div className={styles["right-column"]}>
        <div className={styles["map"]}>
          <Card className={styles["card"]}>
            <div
              style={{
                width: "582px",
                height: "429px",
                overflow: "hidden",
                borderRadius: "8px",
                padding: "12px",
                boxSizing: "border-box",
              }}
            >
              <GoogleMapReact
                bootstrapURLKeys={{
                  key: "AIzaSyDR39HxOW9dvteOXkmHU1sgqGOjCmgj9Qc",
                }}
                defaultCenter={{
                  lat: 59.955413,
                  lng: 30.337844,
                }}
                defaultZoom={11}
              >
                <AnyReactComponent
                  // @ts-ignore
                  lat={59.955413}
                  lng={30.337844}
                  index={1}
                />
              </GoogleMapReact>
            </div>
          </Card>
        </div>
        <div className={styles["chat"]}>
          <Card className={styles["card"]}>Test</Card>
        </div>
      </div>
      <div className={styles["sidebar"]}>{/* <div>Your </div> */}</div>
    </div>
  );
}
