import { QuestCard } from "components/QuestCard";
import { Button, Card, Input, Tag, message, theme } from "antd";
import {
  QuestPlus,
  updateQueryData,
  useLazyItineraryQuery,
} from "store/services/quests";
import GoogleMapReact from "google-map-react";
import { KeyboardEvent, useEffect, useRef, useState } from "react";
import { LoadingOutlined } from "@ant-design/icons";
import { useEditQuestMutation } from "store/services/chat";
import classNames from "classnames";
import { getStore } from "store/accessor";
import { useSyncCalendarMutation } from "store/services/calendar";

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

function formatTime(time: string) {
  const [hour, minute] = time.split(":") as [string, string];

  if (parseInt(hour) < 12) {
    return time + " am";
  }

  if (parseInt(hour) === 12) {
    return time + " pm";
  }

  if (parseInt(hour) === 24) {
    return [12, minute].join(":") + " am";
  }

  let newHourString = (parseInt(hour) % 12).toString();

  if (newHourString.length === 1) {
    newHourString = "0" + newHourString;
  }

  return [newHourString, minute].join(":") + " pm";
}

// I hate 'as const'. That's all.
const USER = "user" as const;
const ASSISTANT = "assistant" as const;

export function Chat({ itinerary }: { itinerary: QuestPlus[] }) {
  const { token } = useToken();
  const chatboxRef = useRef<HTMLDivElement | null>(null);

  const [sendMessage, { isLoading }] = useEditQuestMutation();

  const [syncCalendar, { isLoading: isCalendarLoading }] =
    useSyncCalendarMutation();

  const [messages, setMessages] = useState<
    { sender: "user" | "assistant"; text: string }[]
  >([
    {
      sender: ASSISTANT,
      text: "Let me know if you'd like to make any changes!",
    },
    // { sender: USER, text: "test message one" },
    // { sender: ASSISTANT, text: "test message one" },
    // { sender: ASSISTANT, text: "Welcome to this awesome chat!" },
    // { sender: USER, text: "test message one" },
    // { sender: ASSISTANT, text: "test message one" },
    // { sender: ASSISTANT, text: "Welcome to this awesome chat!" },
    // { sender: USER, text: "test message one" },
    // { sender: ASSISTANT, text: "test message one" },
    // { sender: ASSISTANT, text: "Welcome to this awesome chat!" },
    // { sender: USER, text: "test message one" },
    // { sender: ASSISTANT, text: "test message one" },
  ]);

  // const fakeQuestArray = [
  //   {
  //     imageUrl: "https://example.com/image1.jpg",
  //     name: "Product A",
  //     description: "This is a cool product.",
  //     funFacts: ["Fact 1", "Fact 2", "Fact 3"],
  //     isMain: true,
  //   },
  //   {
  //     imageUrl: "https://example.com/image2.jpg",
  //     name: "Product B",
  //     description: "Check out this amazing product.",
  //     funFacts: ["Fact 4", "Fact 5"],
  //     isMain: false,
  //   },
  //   {
  //     imageUrl: "https://example.com/image3.jpg",
  //     name: "Product C",
  //     description: "Introducing the latest gadget.",
  //     funFacts: ["Fact 6", "Fact 7", "Fact 8"],
  //     isMain: true,
  //   },
  // ];

  const [currentMessage, setCurrentMessage] = useState("");

  // useEffect(() => {
  //   addMessage('Welcome to this awesome chat!', ASSISTANT);
  // }, []);

  const addMessage = (text: string, sender: "user" | "assistant") => {
    setMessages((prevMessages) => [...prevMessages, { text, sender }]);
  };

  const handleInput = async () => {
    if (isLoading) {
      return;
    }

    const params = new URLSearchParams(location.search);
    const loc = params.get("location")!;
    const quest = params.get("quest")!;

    addMessage(currentMessage, USER);
    setCurrentMessage("");

    const result = await sendMessage({
      message: currentMessage,
      location: loc,
      itinerary,
    });

    if ("error" in result) {
      addMessage("I'm sorry, there was an error. Please try again.", ASSISTANT);

      return;
    }

    addMessage("Done! Would you like to make any other changes?", ASSISTANT);

    const { data: newItinerary } = result;

    getStore().dispatch(
      updateQueryData(
        "itinerary",
        { location: loc, quest },
        (itinerary) => newItinerary
      )
    );

    chatboxRef.current?.scrollTo({
      top: Number.MAX_SAFE_INTEGER,
      behavior: "smooth",
    });

    // console.log(res);
    // console.log(messages);
  };

  const handleEnter = (evt: KeyboardEvent) => {
    if (evt.key === "Enter") {
      handleInput();
    }
  };

  return (
    <div className={styles.Chat}>
      {/* <Card className={styles["chat-card"]}> */}
      <div className={styles["chatbox"]} ref={chatboxRef}>
        {messages.map((message, index) => {
          const msgStyle =
            message.sender === USER
              ? styles["message-user"]
              : styles["message-assistant"];

          return (
            <Card
              key={index}
              className={`${styles["chat-card"]} ${msgStyle}`}
              style={{
                backgroundColor:
                  message.sender === "user" ? token.colorPrimary : undefined,
                color: message.sender === "user" ? "white" : undefined,
              }}
            >
              <div>{`${message.sender === "assistant" ? "🤖" : "🤔"}: ${
                message.text
              }`}</div>
            </Card>
          );
        })}
      </div>
      <div onKeyDown={handleEnter} className={styles["flex"]}>
        <Input
          placeholder="Ask Claude to modify the itinerary"
          className={styles["input"]}
          value={currentMessage}
          onChange={(evt) => setCurrentMessage(evt.target.value)}
        />
        <Button
          className={styles["send-btn"]}
          onClick={handleInput}
          loading={isLoading}
          // type="primary"
        >
          {isLoading ? "Working..." : "Send"}
        </Button>
        <Button
          loading={isCalendarLoading}
          type="primary"
          onClick={async () => {
            if (!itinerary) {
              return;
            }

            await syncCalendar(itinerary);

            message.success("Synced to calendar!");
          }}
        >
          🎉 Export to calendar
        </Button>
      </div>
      {/* </Card> */}
    </div>
  );
}

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
    <div
      className={styles.ItineraryPage}
      // style={{ backgroundColor: token.colorPrimary }}
    >
      <div
        className={styles["sidebar"]}
        style={{ backgroundColor: token.colorPrimary }}
      >
        <div>
          Your trip to <i>{loc}</i>
        </div>
        <div>{quest}</div>
      </div>
      <div className={styles["left-column"]}>
        <div className={styles["itinerary"]}>
          <Card className={styles["card"]}>
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
                    <div style={{ fontSize: "16px" }}>
                      {idx + 1}. {name}
                    </div>
                    {/* <div>{description}</div> */}
                    <div>
                      Start:{" "}
                      <Tag color={token.colorPrimary}>
                        {formatTime(startTime)}
                      </Tag>
                      End:{" "}
                      <Tag color={token.colorPrimary}>
                        {formatTime(endTime)}
                      </Tag>
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
          <Card className={styles["card"]}>
            {data && <Chat itinerary={data} />}
          </Card>
        </div>
      </div>
      <div
        className={styles["sidebar"]}
        style={{ backgroundColor: token.colorPrimary }}
      >
        {/* <div>Your </div> */}
      </div>
    </div>
  );
}
