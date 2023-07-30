import { Message, Quest } from "types";
import { baseApi } from ".";

const questsApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    editQuest: build.mutation<any, { messages: Message[]; itinerary: Quest[] }>(
      {
        query: ({ messages, itinerary }) => ({
          method: "POST",
          url: `quests`,
          body: {
            messages,
            itinerary,
          },
        }),

        transformResponse: (res: any) => {
          console.log(res);

          return res;
        },
      }
    ),
  }),
});

export const { useEditQuestMutation } = questsApi;
