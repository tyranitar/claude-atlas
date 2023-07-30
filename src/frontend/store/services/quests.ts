import { baseApi } from ".";
import { z } from "zod";

const zQuest = z.object({
  imageUrl: z.string(),
  name: z.string(),
  description: z.string(),
  funFacts: z.string().array(),
  isMain: z.boolean().optional(),
});

type Quest = z.infer<typeof zQuest>;

const zMessage = z.object({
  sender: z.enum(["user", "assistant"]),
  text: z.string(),
});

type Message = z.infer<typeof zMessage>;

const questsApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    mainQuests: build.query<[Quest, Quest, Quest], string>({
      query: (location: string) => ({
        method: "GET",
        url: `main-quests?location=${encodeURIComponent(location)}`,
      }),
    }),
  }),
});

export const { useMainQuestsQuery } = questsApi;
