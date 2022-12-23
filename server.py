from flask_app import app
from flask_app.controllers import usersControllers, login_regControllers, recipesControllers


if __name__=="__main__":
    app.run(port=5001, debug=True)