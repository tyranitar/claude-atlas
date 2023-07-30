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

    itinerary: build.query<
      (Quest & {
        latitude: number;
        longitude: number;
        name: string;
        startTime: string;
        endTime: string;
      })[],
      { location: string; quest: string }
    >({
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
        return res.response.map(
          ({
            image_url,
            name,
            latitude,
            longitude,
            start_time,
            end_time,
          }: any) => ({
            imageUrl: image_url,
            name,
            description: "",
            funFacts: [],
            latitude,
            longitude,
            startTime: start_time,
            endTime: end_time,
          })
        );
      },
    }),
  }),
});

export const {
  useMainQuestsQuery,
  useLazyMainQuestsQuery,
  useLazyItineraryQuery,
} = questsApi;
