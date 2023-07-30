import classNames from "classnames";

const styles = require("./SimpleImage.module.scss");

export function SimpleImage({
  src,
  className,
}: {
  src: string;
  className?: string;
}) {
  return (
    <div
      className={classNames([styles.Image, className])}
      style={{ backgroundImage: `url(${src})` }}
    ></div>
  );
}
