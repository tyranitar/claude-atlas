import { z } from "zod";

export const zQuest = z.object({
  imageUrl: z.string(),
  name: z.string(),
  description: z.string(),
  funFacts: z.string().array(),
  isMain: z.boolean().optional(),
});

export type Quest = z.infer<typeof zQuest>;

export const zMessage = z.object({
  sender: z.enum(["user", "assistant"]),
  text: z.string(),
});

export type Message = z.infer<typeof zMessage>;
