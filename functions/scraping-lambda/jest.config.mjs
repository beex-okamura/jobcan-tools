/** @type {import('jest').Config} */
const config = {
  clearMocks: true,
  collectCoverage: true,
  coverageDirectory: "coverage",
  coverageProvider: "v8",
  globals: {
    'ts-jest': {
      useEsm: true
    }
  },
  preset: "ts-jest/presets/default-esm",
};

export default config;
