from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)


@app.route("/")
def browsing():
    return render_template("browse.html")


if __name__ == "__main__":
    app.run(debug=True)
