from flask import Flask , g , render_template ,request, redirect, session
from pyscripts.database import database
from pyscripts.user import User




#from pyscripts import routes

app = Flask(__name__)
#REMOVE TO CONFIG FILE LATER
app.secret_key = "something-very-secret-and-random"

@app.before_request
def load_current_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:

        g.user = db.pull_user_data_id(user_id)
        g.user.password_hash = None


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
    if not email or not password:
        return render_template("login.html", error="Please fill in all fields.")
    temp_user=db.pull_user_data_email(email)
    if temp_user is None:
        return render_template("login.html", error="No Account Asociated with Email, please check spelling or create account.")
    pass_is_cor=temp_user.verify_password(password)
    if pass_is_cor==True:
        session["user_id"] = temp_user.id
        return redirect("/")
    else:
        return render_template("login.html", error="Incorrect Password")

@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.get("/create-account")
def create_account_get():
    return render_template("create_account.html")

@app.post("/create-account")
def create_account_post():
    user_name=request.form["user_name"]
    email = request.form["email"]
    password = request.form["password"]
    if not user_name or not email or not password:
        return render_template("create_account.html", error="All fields are required.")
    temp_user=User.create(-343,user_name,email,password)
    creation_status=db.new_user(temp_user)
    if creation_status==True:
        return redirect("/login")
    elif creation_status=="username_taken":
        return render_template("create_account.html", error="User name taken please choose another.")
    elif creation_status=="email_taken":
        return render_template("create_account.html", error="This email is already asociated with an account.")
    else:
        return render_template("create_account.html", error="Unknown error please try again")

if __name__ == "__main__":
    db=database()
    toReadData=input("Do you want to read the quotes in: ")
    if toReadData=="Yes" or toReadData == "Y":
        db.readCSV("The Better SMP - Main - quotes [837444835472441414].csv")
    app.run(debug=True)

