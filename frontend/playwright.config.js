// @ts-check
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30 * 1000,
  expect: {
    timeout: 5000,
    toHaveScreenshot: { maxDiffPixels: 150 } // allow tiny font/platform differences
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  reporter: [['list'], ['html', { outputFolder: 'playwright-report' }]],
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    {
      name: 'chrome-stable',
      use: { ...devices['Desktop Chrome'], channel: 'chrome' }
    }
  ],
  webServer: {
    command: 'npm start',
    port: 3000,
    reuseExistingServer: !process.env.CI,
    cwd: 'frontend'
  }
});
