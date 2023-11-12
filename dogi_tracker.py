import argparse
import asyncio
import telegram
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


URL = "https://drc-20.org/marketplace/drc20/dogi"
XPATH_MARKET_CAP = '//*[@id="root"]/section/main/div/div/div[1]/div[2]/div/div/div[2]/span'


def get_market_cap(counter=0):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.page_load_strategy = "none"
    driver = Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(URL)
    time.sleep(3)
    content = driver.find_elements(By.XPATH, XPATH_MARKET_CAP)
    counter = counter + 1
    market_cap = content[0].text
    if market_cap:
        return market_cap
    else:
        if counter > 5:
            return "ERROR"
        else:
            get_market_cap(counter)


async def notify_chat(api_key, chat_id):
    bot = telegram.Bot(api_key)
    async with bot:
        message = "Current MC of Dogi: " + str(get_market_cap())
        await bot.send_message(text=message, chat_id=chat_id)


def main():
    parser = argparse.ArgumentParser(description="Track and notify about Dogi MC")

    parser.add_argument("chat_id", help="Chat ID")
    parser.add_argument("api_key", help="API Key")

    args = parser.parse_args()
    asyncio.run(notify_chat(str(args.api_key), str(args.chat_id)))


if __name__ == "__main__":
    main()
