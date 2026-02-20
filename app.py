from flask import Flask , render_template


#from pyscripts import routes

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Login")
def Login():

    return "Login Page PH."


if __name__ == "__main__":
    app.run(debug=True)

