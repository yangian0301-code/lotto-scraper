import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_latest_lotto():
    url = "https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    container = soup.select_one(".contents_box02")

    period = container.select_one(".font_black15").text.strip()
    numbers = [n.text.strip() for n in container.select(".ball_tx")[:6]]
    special = container.select_one(".ball_red").text.strip()

    result = f"{period} | {' '.join(numbers)} + {special}"
    return result


if __name__ == "__main__":
    try:
        result = fetch_latest_lotto()
        print("最新開獎：", result)

        # 存檔（可選）
        with open("result.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {result}\n")

    except Exception as e:
        print("錯誤:", e)
