import "../styles/global.scss";

import { AppProps } from "next/app";
import Head from "next/head";

const styles = require("./App.module.scss");

export default function App({ Component, pageProps }: AppProps) {
  return (
    <div className={styles["App"]}>
      {/* <Head></Head> */}
      <Component {...pageProps} />
    </div>
  );
}
