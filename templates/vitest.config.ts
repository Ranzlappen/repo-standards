// Vitest configuration — https://vitest.dev/config/
//
// Sibling to templates/pyproject.toml.example's [tool.pytest.ini_options]:
// each ecosystem ships its own testing starter. Drop into the repo root
// and adjust paths per project.

import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    // Match common test-file conventions across both `tests/` and co-located.
    include: [
      'tests/**/*.{test,spec}.{js,mjs,ts,jsx,tsx}',
      'src/**/*.{test,spec}.{js,mjs,ts,jsx,tsx}',
    ],
    exclude: [
      'node_modules/**',
      'dist/**',
      'build/**',
      '_site/**',
      'coverage/**',
    ],

    // jsdom for browser-flavored code; node for plain modules. Override per
    // file with `// @vitest-environment node` (or jsdom) at the top.
    environment: 'jsdom',

    globals: false,

    // Reporter defaults that work in both local and CI runs.
    reporters: process.env.CI ? ['default', 'junit'] : ['default'],
    outputFile: process.env.CI ? { junit: 'coverage/junit.xml' } : undefined,

    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**/*.{js,mjs,ts,jsx,tsx}'],
      exclude: [
        'src/**/*.{test,spec}.{js,mjs,ts,jsx,tsx}',
        'src/**/__tests__/**',
        'src/**/*.d.ts',
      ],
      thresholds: {
        // Tune per project. Defaults match pytest's fail_under = 80.
        lines: 80,
        statements: 80,
        functions: 80,
        branches: 75,
      },
    },

    // Common defaults. Override per project if flaky tests need more.
    testTimeout: 10_000,
    hookTimeout: 10_000,
  },
});
