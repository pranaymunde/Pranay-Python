from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spiritual.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------------------
# DATABASE MODELS
# --------------------------------

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

class SwamiMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

class Aarti(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Stotra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Mantra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

# --------------------------------
# CREATE TABLES
# --------------------------------
with app.app_context():
    db.create_all()

    # --------- Preload Thoughts ---------
    if Thought.query.count() == 0:
        thoughts_list = [
            "स्वामी समर्थाचा विचार: संयम जीवनाचा पाया आहे.",
            "प्रत्येक दिवशी काहीतरी चांगले करणे आपल्या कर्तव्याचा भाग आहे.",
            "सकारात्मक विचार मानसिक शांततेसाठी आवश्यक आहेत."
        ]
        for t in thoughts_list:
            db.session.add(Thought(content=t))
        db.session.commit()

    # --------- Preload Swami Messages ---------
    if SwamiMessage.query.count() == 0:
        messages = [
            "स्वामी समर्थ सर्वांच्या पाठीशी आहेत.",
            "प्रत्येक संकटात स्वामींचा स्मरण करा.",
            "सेवा आणि भक्ती हाच जीवनाचा मार्ग आहे."
        ]
        for m in messages:
            db.session.add(SwamiMessage(content=m))
        db.session.commit()

    # --------- Preload Aartis ---------
    if Aarti.query.count() == 0:
        aartis_list = [
            {"title": "स्वामी समर्थ आरती", "content": "जय देव जय देव जय श्री स्वामी समर्था\nकरुणासिंधू दया करूनि ठेवा आम्हां पायी..."},
            {"title": "दत्त आरती", "content": "त्रिकुटीचा राजा माझा दत्त गुरू\nजय देव जय देव..."}
        ]
        for a in aartis_list:
            db.session.add(Aarti(title=a["title"], content=a["content"]))
        db.session.commit()

    # --------- Preload Stotras ---------
    if Stotra.query.count() == 0:
        stotras_list = [
            {"title": "दत्त स्तोत्र", "content": "ॐ दत्ताय नमः\nशिवदत्त स्वरूपाय नमः..."},
            {"title": "शिव स्तोत्र", "content": "ॐ नमः शिवाय\nसर्वशक्तिमानाय नमः..."}
        ]
        for s in stotras_list:
            db.session.add(Stotra(title=s["title"], content=s["content"]))
        db.session.commit()

    # --------- Preload Mantras ---------
    if Mantra.query.count() == 0:
        mantras_list = [
            {"title": "दत्त मंत्र", "content": "ॐ श्री दत्तात्रेयाय नमः"},
            {"title": "स्वामी समर्थ मंत्र", "content": "ॐ स्वामी समर्थाय नमः"}
        ]
        for m in mantras_list:
            db.session.add(Mantra(title=m["title"], content=m["content"]))
        db.session.commit()

# --------------------------------
# ROUTES (Same as before)
# --------------------------------

# Home Thoughts
@app.route("/")
def home():
    thoughts = Thought.query.all()
    return render_template("index.html", thoughts=thoughts)

@app.route("/add", methods=["POST"])
def add_thought():
    text = request.form.get("thought")
    db.session.add(Thought(content=text))
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:id>")
def delete_thought(id):
    t = Thought.query.get(id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("home"))

# Nitya Seva
@app.route("/swami")
def swami():
    msgs = SwamiMessage.query.all()
    return render_template("swami.html", msgs=msgs)

@app.route("/swami/add", methods=["POST"])
def add_swami():
    txt = request.form.get("msg")
    db.session.add(SwamiMessage(content=txt))
    db.session.commit()
    return redirect(url_for("swami"))

@app.route("/swami/delete/<int:id>")
def delete_swami(id):
    m = SwamiMessage.query.get(id)
    db.session.delete(m)
    db.session.commit()
    return redirect(url_for("swami"))

# Aartis
@app.route("/aartis")
def aartis():
    items = Aarti.query.all()
    return render_template("aartis.html", aartis=items)

@app.route("/aarti/<int:id>")
def aarti_page(id):
    a = Aarti.query.get(id)
    return render_template("aarti.html", aarti=a)

@app.route("/aartis/add", methods=["POST"])
def add_aarti():
    title = request.form.get("title")
    content = request.form.get("content")
    db.session.add(Aarti(title=title, content=content))
    db.session.commit()
    return redirect(url_for("aartis"))

# Stotras
@app.route("/stotras")
def stotras():
    items = Stotra.query.all()
    return render_template("stotras.html", stotras=items)

@app.route("/stotra/<int:id>")
def stotra_page(id):
    s = Stotra.query.get(id)
    return render_template("stotra.html", stotra=s)

@app.route("/stotras/add", methods=["POST"])
def add_stotra():
    title = request.form.get("title")
    content = request.form.get("content")
    db.session.add(Stotra(title=title, content=content))
    db.session.commit()
    return redirect(url_for("stotras"))

# Mantras
@app.route("/mantras")
def mantras():
    items = Mantra.query.all()
    return render_template("mantras.html", mantras=items)

@app.route("/mantra/<int:id>")
def mantra_page(id):
    m = Mantra.query.get(id)
    return render_template("mantra.html", mantra=m)

@app.route("/mantras/add", methods=["POST"])
def add_mantra():
    title = request.form.get("title")
    content = request.form.get("content")
    db.session.add(Mantra(title=title, content=content))
    db.session.commit()
    return redirect(url_for("mantras"))


# --------------------------------
if __name__ == "__main__":
    try:
        app.run(debug=True, port=8000)
    except SystemExit:
        pass
