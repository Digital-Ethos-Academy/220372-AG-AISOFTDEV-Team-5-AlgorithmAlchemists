#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

// Basic story IDs to capture (add more as needed)
const stories = [
  { id: 'components-metricscard--variants', name: 'metrics-cards' },
  { id: 'components-scorebar--high', name: 'scorebar-high' },
  { id: 'components-scorebar--medium', name: 'scorebar-medium' },
  { id: 'components-scorebar--low', name: 'scorebar-low' },
  { id: 'layout-pageshell--overview-example', name: 'overview-shell' }
];

const outDir = path.join(process.cwd(), '..', 'docs', 'mockups');
if(!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const base = 'file://' + path.join(process.cwd(), 'storybook-static');

(async () => {
  const browser = await chromium.launch();
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
