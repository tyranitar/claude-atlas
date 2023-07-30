import { Quest } from "types";
import { baseApi } from ".";

const questsApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    mainQuests: build.query<[Quest, Quest, Quest], string>({
      query: (location: string) => ({
        method: "POST",
        url: `quests`,
        body: {
          city: location,
        },
      }),

      transformResponse: (res: any) => {
        return res.response.map(({ fun_facts, image_url, name }: any) => ({
          imageUrl: image_url,
          name,
          description: "",
          funFacts: fun_facts,
        }));
      },
    }),

    itinerary: build.query<Quest[], { location: string; quest: string }>({
      query: ({ location, quest }) => ({
        method: "POST",
        url: "itinerary",
        body: {
          city: location,
          quest,
        },
      }),

      transformResponse: (res: any) => {
        console.log(res);

        // return res.response.map();
        return res;
      },
    }),
  }),
});

export const {
  useMainQuestsQuery,
  useLazyMainQuestsQuery,
  useLazyItineraryQuery,
} = questsApi;
