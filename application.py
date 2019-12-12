# import flask server and create it
from flaskr import create_app

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
