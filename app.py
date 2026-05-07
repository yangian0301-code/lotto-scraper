from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

URL = "https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx"

def fetch_lottery():
    response = requests.get(URL)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    result_item = soup.find("div", class_="result-item")

    period = result_item.find(
        "div",
        class_="period-title"
    ).text.strip()

    date = result_item.find(
        "div",
        class_="period-date"
    ).text.strip()

    balls = result_item.find_all(
        "span",
        class_="ball ball-orange"
    )

    numbers = [
        ball.text.strip()
        for ball in balls
    ]

    special = result_item.find(
        "span",
        class_="ball ball-red"
    ).text.strip()

    return {
        "period": period,
        "date": date,
        "numbers": numbers,
        "special": special
    }

@app.route("/")
def home():
    data = fetch_lottery()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
