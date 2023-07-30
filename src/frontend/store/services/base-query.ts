import { fetchBaseQuery } from "@reduxjs/toolkit/dist/query";

type RestBaseQueryArgs = {
  // baseQueryType: RestBaseQueryType;
  url: string;
} & ({ method: "GET" } | { method: "POST"; body: Record<string, any> });

type BaseQueryArgs = RestBaseQueryArgs;

export const baseQuery = fetchBaseQuery({
  baseUrl: `${process.env.NEXT_PUBLIC_API_URL}/api`,
  //   prepareHeaders,
});
