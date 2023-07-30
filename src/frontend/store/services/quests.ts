import { Quest } from "types";
import { baseApi } from ".";

const questsApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    mainQuests: build.query<[Quest, Quest, Quest], string>({
      query: (location: string) => ({
        method: "POST",
        url: `quests`,
        body: {
          location,
        },
      }),

      transformResponse: (res: any) => {
        console.log(res);

        return res;
      },
    }),
  }),
});

export const { useMainQuestsQuery, useLazyMainQuestsQuery } = questsApi;
