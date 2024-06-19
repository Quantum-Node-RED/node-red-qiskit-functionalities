import js from "@eslint/js";

export default [
  js.configs.recommended,

  {
    ignores: ["node_modules/*"],
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "warn",
      "indent": ["error", 2],
      "comma-dangle": ["error", "never"]
    }
  }
];