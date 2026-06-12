// @ts-check
import tseslint from "typescript-eslint";

export default [
  {
    ignores: ["node_modules/", ".next/", "types/", "package-lock.json"],
  },
  ...tseslint.configs.recommended,
  {
    files: ["**/*.ts", "**/*.tsx"],
    rules: {
      "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
    },
  },
];
