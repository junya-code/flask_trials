from junya_flask import app
from flask import render_template, request, redirect, url_for
import sqlite3

DATABASE = "database.db"


@app.route("/")
def index():
    con = sqlite3.connect(DATABASE)
    db_books = con.execute("SELECT * FROM books").fetchall()
    con.close()

    books = []
    for row in db_books:
        books.append({"title": row[0], "price": row[1], "arrival_day": row[2]})

    return render_template("index.html", books=books)


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/register", methods=["POST"])
def register():
    title = request.form["title"]
    price = request.form["price"]

    # 年月日を分割して受け取り、結合
    year = request.form.get("year")
    month = request.form.get("month")
    day = request.form.get("day")

    # 例: "2025年10月05日" のような形式に整形
    arrival_day = f"{year}年{month.zfill(2)}月{day.zfill(2)}日"

    # DB登録
    con = sqlite3.connect(DATABASE)
    con.execute("INSERT INTO books VALUES(?, ?, ?)", [title, price, arrival_day])
    con.commit()
    con.close()

    return redirect(url_for("index"))


@app.route("/clear")
def clear():
    con = sqlite3.connect(DATABASE)
    con.execute("DELETE FROM books")  # 全レコード削除
    con.commit()
    con.close()
    return redirect(url_for("index"))
