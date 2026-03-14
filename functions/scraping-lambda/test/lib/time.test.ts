import { trunc15Minutes, calcBreakTime, formatTime } from "../../src/lib/time.ts";

describe('trunc15Minutes', () => {
    test.each([
        [7.0, 7.0],
        [7.25, 7.25],
        [7.5, 7.5],
        [7.75, 7.75],
        [7.91, 7.75],
        [7.99, 7.75],
        [8.0, 8.0],
        [8.1, 8.0],
    ])('trunc15Minutes(%s) = %s', (input, expected) => {
        expect(trunc15Minutes(input)).toBe(expected);
    });
});

describe('calcBreakTime', () => {
    test.each([
        [5.0, 0],
        [6.0, 0],
        [6.5, 0.5],
        [7.5, 0.5],
        [7.51, 1],
        [8.0, 1],
        [10.0, 1],
    ])('calcBreakTime(%s) = %s', (input, expected) => {
        expect(calcBreakTime(input)).toBe(expected);
    });
});

describe('formatTime', () => {
    test.each([
        [6.0, { hour: 6, minute: '0' }],
        [6.25, { hour: 6, minute: '15' }],
        [6.5, { hour: 6, minute: '30' }],
        [6.75, { hour: 6, minute: '45' }],
        [17.25, { hour: 17, minute: '15' }],
        [0, { hour: 0, minute: '0' }],
    ])('formatTime(%s) = %o', (input, expected) => {
        expect(formatTime(input)).toEqual(expected);
    });
});
