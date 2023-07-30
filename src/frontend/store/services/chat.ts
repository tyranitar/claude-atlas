import { Message, Quest } from "types";
import { baseApi } from ".";
import { QuestPlus } from "./quests";

const chatApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    editQuest: build.mutation<
      any,
      { message: string; itinerary: QuestPlus[]; location: string }
    >({
      query: ({ location, itinerary, message }) => ({
        method: "POST",
        url: `chat`,
        body: {
          city: location,
          input: message,
          itinerary: itinerary.map(
            ({ imageUrl, name, latitude, longitude, startTime, endTime }) => ({
              image_url: imageUrl,
              name: name,
              latitude: latitude,
              longitude: longitude,
              start_time: startTime,
              end_time: endTime,
            })
          ),
        },
      }),

      transformResponse: (res: any) => {
        console.log(res);

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

export const { useEditQuestMutation } = chatApi;
