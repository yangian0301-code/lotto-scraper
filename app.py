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

        response = requests.get(URL, headers=headers, timeout=10)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        result_item = soup.find("div", class_="result-item")

        # 🚨 防止抓不到直接 crash
        if not result_item:
            return {"error": "抓不到資料（可能網站變動或被擋）"}

        period = result_item.find("div", class_="period-title").text.strip()
        date = result_item.find("div", class_="period-date").text.strip()

        balls = result_item.find_all("span", class_="ball ball-orange")

        numbers = [ball.text.strip() for ball in balls]

        special = result_item.find("span", class_="ball ball-red").text.strip()

        return {
            "period": period,
            "date": date,
            "numbers": numbers,
            "special": special
        }

    except Exception as e:
        return {"error": str(e)}


@app.route("/")
def home():
    data = fetch_lottery()

    # 🚨 避免 Render 直接 500
    if "error" in data:
        return f"系統暫時異常：{data['error']}", 200

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
