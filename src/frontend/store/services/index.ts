import { createApi } from "@reduxjs/toolkit/query/react";
import { HYDRATE } from "next-redux-wrapper";
import { baseQuery } from "./base-query";

// export type CacheTagType = (typeof TAG_TYPES)[number];
// export type CacheTag = { type: CacheTagType; id: string };

export const baseApi = createApi({
  reducerPath: "baseApi",
  tagTypes: [],
  baseQuery,

  extractRehydrationInfo(action, { reducerPath }) {
    if (action.type === HYDRATE) {
      return action.payload[reducerPath];
    }
  },

  endpoints: () => ({}),
});

export const {
  util: { getRunningQueriesThunk, invalidateTags },
} = baseApi;

export const reducers = {
  [baseApi.reducerPath]: baseApi.reducer,
};

export const middleware = [baseApi.middleware];
