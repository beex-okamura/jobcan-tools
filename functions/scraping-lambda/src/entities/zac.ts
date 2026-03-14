import { z } from 'zod';

export const ZacWorkTimeSchema = z.object({
  hour: z.number().int().min(0).max(23),
  minute: z.enum(['0', '15', '30', '45'])
});

export type ZacWorkTime = z.infer<typeof ZacWorkTimeSchema>

// export interface ZacWorkTime {
//   hour: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23;
//   minute: 0 | 15 | 30 | 45;
// }

export interface ZacWorkTimeInput {
  code: string;
  workTime: ZacWorkTime;
  text: string;
}

export interface ZacRegisterInput {
  workStartTime: ZacWorkTime;
  workEndTime: ZacWorkTime;
  breakTime: ZacWorkTime;
  workDetails: ZacWorkTimeInput[];
}

export const SnsEventSchema = z.object({
  tenantId: z.string(),
  loginId: z.string(),
  password: z.string(),
  registerDate: z.string(),
  workInput: z.object({
    workStartTime: ZacWorkTimeSchema,
    workEndTime: ZacWorkTimeSchema,
    breakTime: ZacWorkTimeSchema,
    workDetails: z.array(z.object({
      code: z.string(),
      workTime: ZacWorkTimeSchema,
      text: z.string(),
    })),
  }),
})
