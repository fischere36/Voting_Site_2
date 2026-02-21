from flask import Flask , render_template
from pyscripts.database import database

#from pyscripts import routes

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Login")
def Login():

    return "Login Page PH."


if __name__ == "__main__":
    db=database()
    toReadData=input("Do you want to read the quotes in: ")
    if toReadData=="Yes" or toReadData == "Y":
        db.readCSV("The Better SMP - Main - quotes [837444835472441414].csv")
    app.run(debug=True)

