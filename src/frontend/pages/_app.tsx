import "../styles/global.scss";

import { ConfigProvider } from "antd";
import { AppProps } from "next/app";
import Head from "next/head";

const styles = require("./App.module.scss");

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#536dfe",
        },
      }}
    >
      <div className={styles["App"]}>
        {/* <Head></Head> */}
        <Component {...pageProps} />
      </div>
    </ConfigProvider>
  );
}
