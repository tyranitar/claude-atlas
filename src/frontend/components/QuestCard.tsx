import { Card } from "antd";
import NextImage from "next/image";
import { SimpleImage } from "./SimpleImage";
import { ReactNode } from "react";

const styles = require("./QuestCard.module.scss");

export function QuestCard({ children }: { children: ReactNode }) {
  return (
    <Card
      className={styles.QuestCard}
      bordered={true}
      cover={
        <SimpleImage
          className={styles["image"]}
          src="https://media.timeout.com/images/105879414/750/422/image.jpg"
        />
      }
    >
      {children}
    </Card>
  );
}
