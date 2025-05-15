import time
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from telegram import Bot

BOT_TOKEN = "7755659289:AAFJnS6uuS7Iq2K-WP_md7D0clzuA7wEjtQ"
CHAT_ID = "1349380884"

async def main():
    # Excel faylı yaradılır
    wb = Workbook()
    ws = wb.active
    ws.title = "Oxu.az Xəbərlər"
    ws.append(["Başlıq", "Link"])

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Saytı aç
    url = "https://oxu.az/siyaset"
    driver.get(url)
    time.sleep(6)  # JavaScript

    # Xəbərləri tapir
    count = 0
    news_blocks = driver.find_elements(By.CSS_SELECTOR, "div.news-i__inner > a")

    for item in news_blocks:
        try:
            title_element = item.find_element(By.CSS_SELECTOR, "div.news-i__title")
            title = title_element.text.strip()
            link = item.get_attribute("href")
            if title and link:
                ws.append([title, link])
                count += 1
        except Exception as e:
            print("Xəta:", e)
            continue


    filename = "oxu_news.xlsx"
    wb.save(filename)
    driver.quit()

    bot = Bot(token=BOT_TOKEN)
    if count > 0:
        await bot.send_message(chat_id=CHAT_ID, text=f"✅ {count} xəbər tapıldı və Excel faylına yazıldı.")
    else:
        await bot.send_message(chat_id=CHAT_ID, text=" Xəbər tapılmadı")

    print(f"{count} xəbər tapıldı və '{filename}' adlı fayla yazıldı.")

if __name__ == "__main__":
    asyncio.run(main())
