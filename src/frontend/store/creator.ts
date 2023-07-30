import { middleware as apiMiddleware } from "./services";
import { configureStore } from "@reduxjs/toolkit";
// import { isDev } from "src/helpers/dev-helpers";
import { rootReducer } from "./root-reducer";

export function createStore() {
  const store = configureStore({
    reducer: rootReducer,
    // devTools: isDev(),

    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(apiMiddleware),
  });

  return store;
}
