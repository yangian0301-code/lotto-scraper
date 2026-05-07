from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

URL = "https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx"


def fetch_lottery():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(URL, headers=headers, timeout=10)
        r.encoding = "utf-8"

        soup = BeautifulSoup(r.text, "html.parser")

        result_item = soup.find("div", class_="result-item")

        # 🚨 防 crash 重點
        if not result_item:
            return None

        period = result_item.find("div", class_="period-title").text.strip()
        date = result_item.find("div", class_="period-date").text.strip()

        numbers = [
            x.text.strip()
            for x in result_item.find_all("span", class_="ball ball-orange")
        ]

        special = result_item.find("span", class_="ball ball-red").text.strip()

        return {
            "period": period,
            "date": date,
            "numbers": numbers,
            "special": special
        }

    except:
        return None


@app.route("/")
def home():
    data = fetch_lottery()

    # 🚨 不讓 Flask crash（避免 502）
    if not data:
        return "系統暫時無法取得資料（請稍後再試）", 200

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run()
