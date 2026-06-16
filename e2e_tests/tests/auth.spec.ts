import { test, expect } from "@playwright/test";
import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const authLoginScenarios = JSON.parse(
  readFileSync(resolve(__dirname, "../scenarios/auth-login.json"), "utf-8"),
);

const BASE_URL = authLoginScenarios.base_url;

for (const scenario of authLoginScenarios.scenarios) {
  test(scenario.id, async ({ page }) => {
    test.info().annotations.push({
      type: "description",
      description: scenario.description,
    });

    await page.goto(BASE_URL);

    if (scenario.expected.status === "validation_error") {
      if (scenario.username) {
        await page.fill("#username", scenario.username);
      }
      if (scenario.password) {
        await page.fill("#password", scenario.password);
      }
      await page.click(".submit-btn");
      await expect(page.locator("#username")).toBeVisible();
      return;
    }

    await page.fill("#username", scenario.username);
    await page.fill("#password", scenario.password);
    await page.click(".submit-btn");

    if (scenario.expected.status === "success") {
      await expect(page.locator("text=Welcome")).toBeVisible();
      await expect(page.locator("text=Sign Out")).toBeVisible();
    } else {
      await expect(page.locator(".error")).toBeVisible();
      if (scenario.expected.message) {
        await expect(page.locator(".error")).toContainText(scenario.expected.message);
      }
    }
  });
}
