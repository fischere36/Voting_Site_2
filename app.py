from flask import Flask
from flask import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pyscripts import routes
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)

