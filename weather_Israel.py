from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

mcp = FastMCP("weather-Israel")


@mcp.tool()
async def get_israel_weather(city: str) -> str:
    """
    מביא תחזית מזג אויר לעיר בישראל

    Args:
        city: שם העיר בעברית (לדוגמא: תל אביב, ירושלים, חיפה)
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.weather2day.co.il/forecast")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(5000)

        # פתיחת תיבת חיפוש
        search_icon = await page.query_selector(
            "a[href*='search'], .search-icon, [class*='search']"
        )
        if search_icon:
            await search_icon.click(force=True)
            await page.wait_for_timeout(2000)

        # הזנת שם עיר
        await page.evaluate("""(city) => {
            const input = document.getElementById('city_search');
            input.style.display = 'block';
            input.style.visibility = 'visible';
            input.style.opacity = '1';
            input.value = city;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
        }""", city)

        await page.wait_for_timeout(2000)

        # בחירת עיר מהרשימה
        items = await page.query_selector_all("li")
        navigated = False
        for item in items:
            text = await item.inner_text()
            if city in text:
                link = await item.query_selector("a")
                if link:
                    href = await link.get_attribute("href")
                    await page.goto("https://www.weather2day.co.il" + href)
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(3000)
                    navigated = True
                    break

        if not navigated:
            await browser.close()
            return f"לא נמצאה העיר '{city}' ברשימה"

        # שליפת תוכן
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "meta", "link"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        lines = [line for line in text.splitlines() if line.strip()]
        clean_text = "\n".join(lines)

        if len(clean_text) > 4000:
            clean_text = clean_text[:4000] + "\n...[תוכן קוצר]"

        await browser.close()
        return clean_text


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()