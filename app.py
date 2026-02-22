from flask import Flask , render_template ,request, redirect, session
from pyscripts.database import database

#from pyscripts import routes

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.get("/login")
def login_get():
    return render_template("login.html")

@app.post("/login")
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    #try:
        


@app.route("/create-account")
def create_account():

    return render_template("login.html")



if __name__ == "__main__":
    db=database()
    toReadData=input("Do you want to read the quotes in: ")
    if toReadData=="Yes" or toReadData == "Y":
        db.readCSV("The Better SMP - Main - quotes [837444835472441414].csv")
    app.run(debug=True)

