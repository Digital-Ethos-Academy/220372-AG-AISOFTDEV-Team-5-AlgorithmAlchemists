const { test, expect } = require('@playwright/test');

async function mockCommon(page){
  await page.route('**/overview', route=> route.fulfill({ status:200, contentType:'application/json', body: JSON.stringify({
    mission: 'Accelerate orientation clarity',
    problem: 'Context loss',
    value: 'Faster onboarding',
    team_count: 10,
    rationale: 'Compression unlocks impact'
  }) }));
  await page.route('**/metrics', route=> route.fulfill({ status:200, contentType:'application/json', body: JSON.stringify({
    baseline_hours: 56,
    tool_hours: 20,
    compression_pct: 64.29,
    quiz_accuracy: 1.0,
    confidence_coverage: 0.98
  }) }));
  await page.route('**/quiz', route=> route.fulfill({ status:200, contentType:'application/json', body: JSON.stringify({
    questions: [ { id: 'Q1', question_text: 'Sample question 1' }, { id: 'Q2', question_text: 'Sample question 2' } ]
  }) }));
  await page.route('**/health', route=> route.fulfill({ status:200, contentType:'application/json', body: JSON.stringify({
    status: 'ok', version: '1.0.0', git_commit: 'abcdef1', build_time: '2025-11-05T00:00:00Z'
  }) }));
}

// Pages chosen: overview (/), metrics, quiz, recommendation (pre-interaction), roles (idle state)

test.describe('Visual baseline pages', ()=>{
  test('overview page', async ({ page }) => {
    await mockCommon(page);
    await page.goto('http://localhost:3000/');
    await expect(page).toHaveScreenshot('overview.png');
  });
  test('metrics page', async ({ page }) => {
    await mockCommon(page);
    await page.goto('http://localhost:3000/metrics');
    await expect(page).toHaveScreenshot('metrics.png');
  });
  test('quiz page', async ({ page }) => {
    await mockCommon(page);
    await page.goto('http://localhost:3000/quiz');
    await expect(page).toHaveScreenshot('quiz.png');
  });
  test('recommendation page (idle)', async ({ page }) => {
    await mockCommon(page);
    await page.goto('http://localhost:3000/recommendation');
    await expect(page).toHaveScreenshot('recommendation-idle.png');
  });
  test('roles page (idle)', async ({ page }) => {
    await mockCommon(page);
    await page.goto('http://localhost:3000/roles');
    await expect(page).toHaveScreenshot('roles-idle.png');
  });
});
