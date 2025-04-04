from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.post_routes import post_bp
from app.routes.report_routes import report_bp
from app.routes.swagger import swagger_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/")
    app.register_blueprint(post_bp, url_prefix="/")
    app.register_blueprint(report_bp, url_prefix="/")
    app.register_blueprint(swagger_bp)