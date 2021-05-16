from flask import Flask,request,render_template,url_for,redirect,session
from flask_restful import Resource,Api,reqparse
import sqlite3
from passlib.hash import pbkdf2_sha256
import json
import fps as fp
from flask_session  import Session
from migration import student
fp.DEVICE_NAME = "/dev/ttyAMA0"
print(fp.DEVICE_NAME)
app = Flask("TTL")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'jeetcreation'
api = Api(app)
#Session(app)

@app.route("/",methods=["get","post"])
def home():
	if not session.get("authenticated",""):
		return redirect("/login")
	students_data = student.get_all();
	return render_template("home.html",name="TTL",students=students_data)
@app.route("/student_registration/",methods=["GET","POST"])
def add_student():
	if not session.get("authenticated",""):
		return redirect("/login")
	else:
		if request.method == "GET":
			return render_template("add_form.html")
		else:
			_id = request.form.get("id","")
			_name = request.form.get("name","")
			_class = request.form.get("class","")
			_fp_id = request.form.get("fp_id","")
			student.insert({"id":_id,"name":_name,"class":_class,"finger_print":_fp_id})
			return redirect("/")

@app.route("/login",methods=["post","get"])
def login():
	if request.method == "POST":
		password = request.form.get("password")
		secret = open("docs/secret.json","r")
		json_data = json.load(secret)
		pass2 = json_data["hash"]
		print(pass2,password)
		if pbkdf2_sha256.verify(password,pass2):
			session['authenticated'] = True
			return redirect("/")

	return render_template("login.html")
	

app.run()
