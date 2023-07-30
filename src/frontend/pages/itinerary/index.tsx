import { QuestCard } from "components/QuestCard";
import { Card, theme } from "antd";
import { useLazyItineraryQuery } from "store/services/quests";
import GoogleMapReact from "google-map-react";
import { useEffect, useState } from "react";
import { LoadingOutlined } from "@ant-design/icons";

const { useToken } = theme;

const styles = require("./index.module.scss");

const MapPoint = ({ index }: { index: number }) => {
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
            {/* <QuestCard imageSrc="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/33/dc/8a/caption.jpg?w=700&h=-1&s=1">
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
            </QuestCard> */}
            {isLoading ? (
              <div>
                <LoadingOutlined />
              </div>
            ) : (
              data?.map(
                (
                  {
                    imageUrl,
                    name,
                    description,
                    // latitude,
                    // longitude,
                    startTime,
                    endTime,
                  },
                  idx
                ) => (
                  <QuestCard key={idx} imageSrc={imageUrl}>
                    <div>
                      {idx + 1}. {name}
                    </div>
                  </QuestCard>
                )
              )
            )}
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
              {data && (
                <GoogleMapReact
                  bootstrapURLKeys={{
                    key: "AIzaSyDR39HxOW9dvteOXkmHU1sgqGOjCmgj9Qc",
                  }}
                  defaultCenter={{
                    lat: data[0]!.latitude,
                    lng: data[0]!.longitude,
                  }}
                  defaultZoom={12}
                >
                  {/* <MapPoint
                  // @ts-ignore
                  lat={59.955413}
                  lng={30.337844}
                  index={1}
                /> */}
                  {data.map(({ latitude, longitude }, idx) => (
                    <MapPoint
                      // @ts-ignore
                      lat={latitude}
                      lng={longitude}
                      index={idx + 1}
                      key={idx}
                    />
                  ))}
                </GoogleMapReact>
              )}
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
