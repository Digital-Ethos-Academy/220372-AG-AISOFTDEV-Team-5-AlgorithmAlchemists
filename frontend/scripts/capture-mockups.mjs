#!/usr/bin/env node
// Using @playwright/test (already in devDependencies) to access chromium
import { chromium } from '@playwright/test';
import fs from 'fs';
import path from 'path';

// Story IDs to capture – extend as new visual states are introduced
const stories = [
  // Existing base set
  { id: 'components-metricscard--variants', name: 'metrics-cards' },
  { id: 'components-scorebar--high', name: 'scorebar-high' },
  { id: 'components-scorebar--medium', name: 'scorebar-medium' },
  { id: 'components-scorebar--low', name: 'scorebar-low' },
  { id: 'components-qaresultpanel--high-confidence', name: 'qa-high' },
  { id: 'components-qaresultpanel--low-confidence-fallback', name: 'qa-low-fallback' },
  { id: 'layout-pageshell--overview-example', name: 'overview-shell' },
  // Newly added coverage
  { id: 'components-qaresultpanel--escalated-no-answer', name: 'qa-escalated' },
  { id: 'components-runtimemetricstable--snapshot', name: 'runtime-metrics' },
  { id: 'components-runtimemetricstable--unauthorized', name: 'runtime-metrics-unauthorized' },
  { id: 'components-rolessearchpanel--empty-initial', name: 'roles-empty' },
  { id: 'components-rolessearchpanel--with-results', name: 'roles-results' },
  { id: 'components-rolessearchpanel--no-results', name: 'roles-none' },
  { id: 'components-metricsdashboard--healthy', name: 'metrics-healthy' },
  { id: 'components-metricsdashboard--degraded', name: 'metrics-degraded' },
  { id: 'components-quizform--perfect-score-static', name: 'quiz-perfect' },
  { id: 'components-quizform--validation-hints', name: 'quiz-validation' }
];

const outDir = path.join(process.cwd(), '..', 'docs', 'mockups');
if(!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const base = 'file://' + path.join(process.cwd(), 'storybook-static');

(async () => {
  let browser;
  try {
    browser = await chromium.launch();
  } catch (e) {
    console.warn('Standard chromium launch failed, attempting system Chrome path fallback. Error:', e.message);
    const candidates = [
      'C:/Program Files/Google/Chrome/Application/chrome.exe',
      'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
    ];
    let launched = false;
    for (const execPath of candidates) {
      try {
        browser = await chromium.launch({ executablePath: execPath });
        console.log('Launched system Chrome at', execPath);
        launched = true;
        break;
      } catch (_) { /* try next */ }
    }
    if(!launched) {
      console.error('Failed to launch any Chromium/Chrome binary. Aborting screenshots.');
      process.exit(1);
    }
  }
  const page = await browser.newPage({ viewport:{ width:1280, height:800 }});
  for (const s of stories) {
    const url = `${base}/iframe.html?id=${s.id}`;
    console.log('Capturing', s.id);
    await page.goto(url, { waitUntil:'load' });
    // allow layout paint
    await page.waitForTimeout(400);
    const filePath = path.join(outDir, `${s.name}.png`);
    await page.screenshot({ path: filePath, fullPage: true });
  }
  await browser.close();
  console.log('Mockup screenshots saved to', outDir);
})();
