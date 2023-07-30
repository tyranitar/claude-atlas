import { Message, Quest } from "types";
import { baseApi } from ".";
import { QuestPlus } from "./quests";

const calendarApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    syncCalendar: build.mutation<any, QuestPlus[]>({
      query: (itinerary) => ({
        method: "POST",
        url: `sync_calendar`,
        body: {
          events: itinerary.map(
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

      // transformResponse: (res: any) => {
      //   console.log(res);

      //   return res.response.map(
      //     ({
      //       image_url,
      //       name,
      //       latitude,
      //       longitude,
      //       start_time,
      //       end_time,
      //     }: any) => ({
      //       imageUrl: image_url,
      //       name,
      //       description: "",
      //       funFacts: [],
      //       latitude,
      //       longitude,
      //       startTime: start_time,
      //       endTime: end_time,
      //     })
      //   );
      // },
    }),
  }),
});

export const { useSyncCalendarMutation } = calendarApi;
