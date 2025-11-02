from flask import Flask

app = Flask(__name__)
@app.route("/")
def home():
    return "Hello, Welcome to my website!"
app.run()