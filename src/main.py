import random

from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash
from os import path, walk
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wad"
app.secret_key = 'soursoursoursour'
app.config["UPLOAD_FOLDER"] = "uploads"

mongo = PyMongo(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
BOTIQ_SAYS = ["Hehe", "funny", "yeah, indeed", "whoah!", "NO WAY", "Havaian pizza is ok"]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("first/signup.html")
    username = request.form.get("login")
    password = request.form.get("password")
    if not username or not password:
        flash("Something is missing......................................................................")
        return redirect(url_for("register"))

    existing = mongo.db.users.find_one({"username": username})
    if existing:
        # user exists
        flash("Error")
        return redirect(url_for("register"))

    password_hash = generate_password_hash(password)
    result = mongo.db.users.insert_one({"username": username, "password": password_hash})
    if result:
        flash("Successfully registered")
        return redirect(url_for("login"))
    flash("Error")
    return redirect(url_for("register"))


@app.route('/signin', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("first/signin.html")
    username = request.form.get("login")
    password = request.form.get("password")
    print(username, password)
    if not username or not password:
        flash("Something's missing")
        return render_template("first/signin.html")

    result = mongo.db.users.find_one({"username": username})
    if result and check_password_hash(result.get("password"), password):
        return render_template("first/signin.html", user=result.get("username"))
    flash("Vas zdes ne stoyalo")
    return redirect(url_for('login'))

@app.route("/upload", methods=["GET", "POST"])
def file_upload():
    filenames = next(walk(app.config["UPLOAD_FOLDER"]), (None, None, []))[2]
    if request.method == "GET":
        return render_template("second/fileupload.html", files=filenames)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for("file_upload"))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f"File {filename} was successfully uploaded")
        filenames.append(filename)
        return render_template("second/fileupload.html", files=filenames)
    flash("don't hack")
    return redirect(url_for("file_upload"))

@app.route("/api/erase", methods=["POST"])
def clean_mess_history():
    print(request.form)
    print(request.form.get("secret_param"))
    if request.form.get("secret_param") != "sainou":
        return ""
    mongo.db.messages.delete_many({})
    return "1"

@app.route("/uploaded/<path:path>")
def serve_uploaded(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    messages = mongo.db.messages.find({})
    if request.method == "GET":
        return render_template("fifth/chatbot.html", messages=messages)
    # message = request.form.get("message")
    # if not message:
    #     flash("No message")
    #     return redirect(url_for('chatbot'))
    # botiq_message = random.choice(BOTIQ_SAYS)
    # messages_to_insert = [{"message":message}, {"message": botiq_message}]
    # result = mongo.db.messages.insert_many(messages_to_insert)
    # if result:
    #     return render_template("fifth/chatbot.html", messages=messages.append(messages_to_insert))


@app.route("/api/send", methods=["POST"])
def messaging():
    message = request.json.get("message")
    if not message:
        return jsonify({"error":"Error"})
    botiq_message = random.choice(BOTIQ_SAYS)
    messages_to_insert = [{"message":message}, {"message": botiq_message}]
    result = mongo.db.messages.insert_many(messages_to_insert)
    return jsonify({"error":False, "result":botiq_message})

@app.route('/static/<path:path>')
def statics(path):
    return send_from_directory('static', path)


app.run(host="localhost", port=5000, debug=True)