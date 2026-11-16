const path = require("node:path");
const { pathToFileURL } = require("node:url");
const ROOT = path.resolve(__dirname, "..");
const { chromium } = require(
  process.env.PLAYWRIGHT_MODULE ||
    path.join(ROOT, ".cache/browser/node_modules/playwright"),
);
const shots = path.join(ROOT, ".cache/dashboard-previews");
const fs = require("node:fs/promises");
const assert = require("node:assert/strict");
(async () => {
  await fs.mkdir(shots, { recursive: true });
  const edge = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
  const executable =
    process.env.BROWSER_EXECUTABLE ||
    (require("node:fs").existsSync(edge) ? edge : undefined);
  const browser = await chromium.launch({
    headless: true,
    ...(executable ? { executablePath: executable } : {}),
  });
  const page = await browser.newPage({
    viewport: { width: 1536, height: 1100 },
    deviceScaleFactor: 1,
  });
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(
    pathToFileURL(path.join(ROOT, "dashboards/preview/delivery_dashboard.html"))
      .href,
  );
  const text = (id) => page.locator("#" + id).innerText();
  const checks = [];
  async function check(ok, name) {
    assert.ok(ok, name);
    checks.push(name);
  }
  await check(
    (await text("overview-kpis")).includes("62.897"),
    "Overview count matches full non-canceled population",
  );
  await check(
    (await text("overview-kpis")).includes("57,31%"),
    "Overview late rate matches source",
  );
  await page.screenshot({
    path: path.join(shots, "overview.png"),
    fullPage: true,
  });
  await page.selectOption("#mode", "Standard Class");
  await check(
    (await text("overview-kpis")).includes("37.632"),
    "Mode filter changes overview denominator",
  );
  await page.click("#reset");
  await page.click("[data-tab=risk]");
  await check(
    (await text("risk-kpis")).includes("4.560"),
    "Default threshold produces 4,560 alerts",
  );
  await check(
    (await text("confusion")).includes("3.467"),
    "Default confusion matrix includes 3,467 false negatives",
  );
  await page.screenshot({ path: path.join(shots, "risk.png"), fullPage: true });
  await page.locator("#threshold").evaluate((el) => {
    el.value = "0.4";
    el.dispatchEvent(new Event("input", { bubbles: true }));
  });
  await check(
    (await text("risk-kpis")).includes("13.071"),
    "Threshold 0.4 alerts all test orders",
  );
  await page.locator("#threshold").evaluate((el) => {
    el.value = "0.5";
    el.dispatchEvent(new Event("input", { bubbles: true }));
  });
  await page.selectOption("#mode", "Standard Class");
  await check(
    (await page.locator("#risk-kpis strong").nth(1).innerText()) === "0",
    "No alerts for Standard Class at threshold 0.5",
  );
  await check(
    (await page.locator("#risk-kpis strong").nth(2).innerText()) === "—",
    "Undefined precision is blank rather than zero",
  );
  await page.click("#reset");
  await page.selectOption("#month", "2015-01");
  await check(
    (await page.locator("#risk-kpis strong").first().innerText()) === "0",
    "No train orders leak into the risk page",
  );
  await page.click("#reset");
  await page.click("[data-tab=promises]");
  await check(
    (await text("promise-kpis")).includes("26,82%"),
    "Default promise policy matches TV5 test rate",
  );
  await page.screenshot({
    path: path.join(shots, "promises.png"),
    fullPage: true,
  });
  await page.selectOption("#policy", "current");
  await check(
    (await text("promise-kpis")).includes("57,56%"),
    "Current promise policy preserves test baseline",
  );
  await page.selectOption("#policy", "q90_min100");
  await check(
    (await page.locator("#promise-kpis strong").nth(1).innerText()) === "0,00%",
    "Q90 policy has zero retrospective exceedance on the test sample",
  );
  await page.click("[data-tab=routing]");
  await check(
    (await text("route-kpis")).includes("828,94"),
    "Routing distance matches C101 OR-Tools",
  );
  const before = await page.locator("#route-kpis strong").nth(3).innerText();
  await page.fill("#fuel-price", "26000");
  const after = await page.locator("#route-kpis strong").nth(3).innerText();
  await check(before !== after, "Fuel price changes simulated cost");
  await page.fill("#fuel-price", "22000");
  await page.screenshot({
    path: path.join(shots, "routing.png"),
    fullPage: true,
  });
  await page.selectOption("#route-case", "c101|fleet10|nearest_feasible");
  await check(
    (await page.locator("#route-kpis strong").nth(1).innerText()) === "—",
    "No-solution distance is missing, not zero",
  );
  await check(
    (await text("route-map")).includes("Chưa tìm"),
    "No-solution case does not show a stale route map",
  );
  await page.setViewportSize({ width: 390, height: 844 });
  await page.click("[data-tab=overview]");
  await page.screenshot({
    path: path.join(shots, "mobile.png"),
    fullPage: true,
  });
  await check(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
    "Mobile page has no horizontal overflow",
  );
  await check(errors.length === 0, "No browser JavaScript errors");
  const result = {
    checks_passed: checks.length,
    checks,
    scope: "Offline preview only, not native Power BI rendering",
    browser: "Microsoft Edge headless",
    errors,
  };
  await fs.writeFile(
    path.join(ROOT, "reports/dashboard/preview_validation.json"),
    JSON.stringify(result, null, 2) + "\n",
  );
  console.log(JSON.stringify(result));
  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
