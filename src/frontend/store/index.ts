import { createWrapper } from "next-redux-wrapper";
import { createStore } from "./creator";
import { setStore } from "./accessor";

function makeStore() {
  const store = createStore();

  setStore(store);

  return store;
}

export type RootState = ReturnType<Store["getState"]>;
export type Store = ReturnType<typeof makeStore>;
export type Dispatch = Store["dispatch"];

export const wrapper = createWrapper<Store>(makeStore);
