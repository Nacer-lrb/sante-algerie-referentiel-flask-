from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from urllib.parse import quote_plus

# Initialisation de l'app Flask
app = Flask(__name__)
app.secret_key = 'nacer'

# Configuration de la base de données
encoded_password = quote_plus('nuicer2021@')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{encoded_password}@localhost/test1'

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



from flask_login import current_user
from functools import wraps
from flask import abort

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(401)  # Non autorisé si l'utilisateur n'est pas admin
        return f(*args, **kwargs)
    return decorated_function

# User loader pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import ici pour éviter les importations circulaires
    return User.query.get(int(user_id))

from app.routes import product_blueprint, auth_blueprint  # Importez les blueprints ici pour éviter les importations circulaires

# Enregistrement des blueprints
# In __init__.py

# At the end of your __init__.py file
from app.routes import auth_blueprint, product_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(product_blueprint)



from flask_migrate import Migrate

migrate = Migrate(app, db)
