from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api
from .process_telemetry_data.controller.process_turbine_power_data_controller import timesequence_bp, ProcessTimesequence
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    api = Api(app)
    swagger = Swagger(app)

    app.register_blueprint(timesequence_bp)

    SWAGGER_URL = "/api/docs"  
    API_URL = "/api/spec"  

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  
            "app_name": "Timesequence API"
        }
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    api.add_resource(ProcessTimesequence, "/process-data")

    return app