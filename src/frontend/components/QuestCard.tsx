import { Card } from "antd";
import NextImage from "next/image";
import { SimpleImage } from "./SimpleImage";
import { ReactNode } from "react";

const styles = require("./QuestCard.module.scss");

export function QuestCard({
  imageSrc,
  children,
}: {
  imageSrc: string;
  children: ReactNode;
}) {
  return (
    <Card
      cover={<SimpleImage className={styles["image"]} src={imageSrc} />}
      className={styles.QuestCard}
      bordered={true}
    >
      {children}
    </Card>
  );
}
