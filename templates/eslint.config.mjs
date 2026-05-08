// ESLint flat config (ESLint 9.x and later).
// Reference: https://eslint.org/docs/latest/use/configure/configuration-files
//
// This is a starter for vanilla / Node / browser projects. Frameworks (React,
// Vue, Svelte, etc.) should compose their official config on top — see the
// commented-out sections below.
//
// Legacy `.eslintrc.json` projects can keep their existing config; the flat
// config takes over only if `eslint.config.mjs` (or `.js`/`.cjs`) is present.

import js from '@eslint/js';
import globals from 'globals';

export default [
  // ESLint's own recommended rules.
  js.configs.recommended,

  // --- Project-wide settings ---
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    linterOptions: {
      reportUnusedDisableDirectives: 'warn',
    },
    rules: {
      // Defer formatting to Prettier — these would conflict.
      'indent': 'off',
      'quotes': 'off',
      'semi': 'off',

      // Catch obvious mistakes.
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'no-debugger': 'error',
      'no-var': 'error',
      'prefer-const': 'warn',
      'eqeqeq': ['error', 'always', { null: 'ignore' }],
    },
  },

  // --- Test files ---
  {
    files: ['**/*.test.{js,mjs,cjs,ts,tsx}', '**/*.spec.{js,mjs,cjs,ts,tsx}'],
    languageOptions: {
      globals: {
        ...globals.jest,
        ...globals.vitest,
      },
    },
  },

  // --- Ignored paths ---
  {
    ignores: [
      'dist/',
      'build/',
      'out/',
      '.next/',
      '.nuxt/',
      'coverage/',
      'node_modules/',
      '_site/',
      '*.min.js',
    ],
  },

  // --- Framework / TypeScript overlays (uncomment as needed) ---
  // import tseslint from 'typescript-eslint';
  // ...tseslint.configs.recommended,
  //
  // import react from 'eslint-plugin-react';
  // react.configs.flat.recommended,
];
