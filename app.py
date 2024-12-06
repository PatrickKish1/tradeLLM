from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from routes.chat import Chat
from routes import swagger

load_dotenv()
app = Flask(__name__)
api = Api(app)

app.register_blueprint(swagger.swagger_ui_blueprint, url_prefix=swagger.SWAGGER_URL)

api.add_resource(Chat, '/api/v1/chat')


if __name__ == "__main__":
    app.run(debug=True)