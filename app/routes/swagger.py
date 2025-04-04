from flask_swagger_ui import get_swaggerui_blueprint

swagger_bp = get_swaggerui_blueprint("/swagger", "/static/swagger.json")


