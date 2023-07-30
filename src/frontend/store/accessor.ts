import { createStore } from "./creator";

type Store = ReturnType<typeof createStore>;

let store: Store | null = null;

export function getStore(): Store {
  if (!store) {
    throw new Error("The store hasn't been initialized yet!");
  }

  return store;
}

export function setStore(_store: Store) {
  store = _store;
}
