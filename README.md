# Weather Israel MCP 🌤️

MCP Server לתחזית מזג אויר בישראל באמצעות Playwright.

## מה הפרויקט עושה

MCP Server שמאפשר ל-LLM לשלוף תחזית מזג אויר עדכנית לערים בישראל.
השרת פותח דפדפן באמצעות Playwright, מנווט לאתר weather2day.co.il ומחזיר את תוכן התחזית ל-LLM.

## סטאק טכנולוגי

- **MCP SDK** — פרוטוקול לחיבור כלים חיצוניים ל-LLM
- **Playwright** — אוטומציה של דפדפן
- **BeautifulSoup** — ניקוי תוכן HTML
- **uv** — ניהול תלויות Python

## התקנה והרצה

```bash
# התקנת תלויות
uv sync

# התקנת דפדפן
uv run playwright install chromium

# הגדרת API Key בקובץ .env
ANTHROPIC_API_KEY=sk-ant-...

# הרצה
uv run host.py
```

## דוגמאות לשאלות
מה התחזית היום בתל אביב?

מה מזג האויר בירושלים?

האם יהיה גשם בחיפה השבוע?

## מבנה הפרויקט
project-template/

├── weather_Israel.py   # MCP Server עם Playwright

├── weather_USA.py      # MCP Server לארה"ב (דוגמא מקורית)

├── client.py           # MCP Client גנרי

├── host.py             # צ'אט טרמינל

└── pyproject.toml      # תלויות

## איך זה עובד

1. ה-LLM מקבל בקשה לתחזית מזג אויר
2. הוא מפעיל את הכלי `get_israel_weather` עם שם העיר
3. Playwright פותח דפדפן ומנווט לאתר weather2day.co.il
4. השרת מחלץ את תוכן הדף ומחזיר אותו ל-LLM
5. ה-LLM מנתח את המידע ועונה למשתמש