import "../styles/global.scss";

import { ConfigProvider } from "antd";
import { AppProps } from "next/app";
import Head from "next/head";
import { wrapper } from "store";

const styles = require("./App.module.scss");

export function App({ Component, pageProps }: AppProps) {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#82b1ff",
        },
      }}
    >
      <div className={styles["App"]}>
        <Head>
          <link rel="preconnect" href="https://fonts.googleapis.com" />
          <link rel="preconnect" href="https://fonts.gstatic.com" />
          <link
            href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500&display=swap"
            rel="stylesheet"
          />
        </Head>
        <Component {...pageProps} />
        <div className={styles["emoji"]}>☁️</div>
      </div>
    </ConfigProvider>
  );
}

export default wrapper.withRedux(App);
