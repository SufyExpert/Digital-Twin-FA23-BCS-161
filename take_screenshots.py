import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(30000)
        
        # UI Screenshot
        print("Taking UI screenshot...")
        await page.goto('http://20.255.118.236')
        await page.wait_for_selector('.chat-view')
        await page.screenshot(path=r'C:\University\Semester\Dev Ops\lab_project\FA23-BCS-161-Screenshots\7_Final_Output\1_React_UI_Working.png')
        
        # Dashboard Screenshot
        print("Taking Dashboard screenshot...")
        await page.click('button.nav-toggle') # Toggle dashboard
        await page.wait_for_selector('.repo-card') # Wait for repos to load
        # Scroll down slightly to show repos clearly
        await page.evaluate("window.scrollBy(0, 300)")
        await asyncio.sleep(1) # wait for smooth scroll
        await page.screenshot(path=r'C:\University\Semester\Dev Ops\lab_project\FA23-BCS-161-Screenshots\7_Final_Output\1b_Dashboard_Repos.png')

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
