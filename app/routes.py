# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request,jsonify
from flask_wtf import FlaskForm
from flask_login import current_user, login_required, login_user, logout_user
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email
from app.models import User, Product
from flask_bcrypt import Bcrypt
from app import db
from app import app
from wtforms import StringField, PasswordField, SubmitField, TextAreaField




auth_blueprint = Blueprint('auth', __name__)
product_blueprint = Blueprint('product', __name__)

bcrypt = Bcrypt()







# Formes Flask-WTF pour l'authentification
class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur ou Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')



from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo






class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=8, message='Le mot de passe doit avoir au moins 8 caractères.'),
        Regexp(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])", 
            message="Le mot de passe doit contenir au moins une lettre majuscule, une lettre minuscule, un chiffre et un caractère spécial (!@#$%^&*)."
        ),
        EqualTo('confirm_password', message='Les mots de passe doivent correspondre')
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired()])
    submit = SubmitField('S\'inscrire')

class AlertForm(FlaskForm):
    product_name = StringField('Nom du produit', validators=[DataRequired()])
    barcode = StringField('Code-barres', validators=[Length(min=8, max=14, message='Le code-barres doit avoir entre 8 et 14 caractères')])
    description = TextAreaField('Description du problème', validators=[DataRequired()])
    submit = SubmitField('Signaler', render_kw={"class": "btn btn-primary"})  # Classe Bootstrap pour le style





@app.route('/')
def home():
    return render_template('home.html')

# Routes d'authentification
@auth_blueprint.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('product.list_products'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.username.data) | (User.email == form.username.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Connexion réussie!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Échec de la connexion. Vérifiez votre nom d\'utilisateur/email et votre mot de passe.', 'danger')
    return render_template('login.html', form=form)





@auth_blueprint.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect to the home page if already logged in

    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).first()

        if existing_user:
            flash('Cet utilisateur ou email existe déjà. Veuillez choisir d\'autres informations.', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Inscription réussie! Connectez-vous maintenant.', 'success')
            return redirect(url_for('auth.login'))  # Redirect to login page after successful registration
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erreur dans le champ "{getattr(form, field).label.text}": {error}', 'danger')
    
    return render_template('register.html', form=form)





@auth_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect( url_for('home'))


















import requests

@product_blueprint.route('/products', methods=['GET'])
def product_list():
    search_query = request.args.get('search_query', '')

    if search_query:
        # Recherchez des produits dont le nom contient la chaîne de recherche
        products = Product.query.filter(Product.product_name.like(f'%{search_query}%')).all()
    else:
        # Si aucun terme de recherche n'est fourni, récupérez tous les produits
        products = Product.query.all()

    return render_template('products.html', products=products, search_query=search_query)


from functools import wraps
from flask import abort
from flask_login import current_user






@app.route('/form', methods=['GET', 'POST'])

def product_form():

    if request.method == 'POST':
        barcode = request.form.get('barcode')
        return jsonify({'barcode': barcode})
    return render_template('index.html')

# Route pour récupérer et enregistrer le produit
@app.route('/fetch_and_store_product', methods=['POST'])
 
def fetch_and_store_product():
    barcode = request.form.get('barcode')
    product_api_url = f'https://world.openfoodfacts.org/api/v2/product/{barcode}.json'
   
    try:
        # Appel à l'API pour obtenir les données du produit
        response = requests.get(product_api_url)
        data = response.json()

        # Vérification de la présence des données du produit dans la réponse JSON
        if 'product' in data and isinstance(data['product'], dict):
            product_data = data['product']

            # Création d'une instance de produit avec les données récupérées
            product = Product(
                id=barcode,
                generic_name=product_data.get('generic_name', ''),
                brands=product_data.get('brands', ''),
                categories=product_data.get('categories', ''),
                ingredients_text=product_data.get('ingredients_text', ''),
                image_url=product_data.get('image_url', ''),
                labels=product_data.get('labels', ''),
                product_name=product_data.get('product_name', ''),
                quantity=product_data.get('quantity', ''),
                proteins=product_data['nutriments'].get('proteins', 0.0),
                fiber=product_data['nutriments'].get('fiber', 0.0),
                energy=product_data['nutriments'].get('energy-kj', 0.0),
                sugars=product_data['nutriments'].get('sugars', 0.0),
                saturated_fat=product_data['nutriments'].get('saturated-fat', 0.0),
                sodium=product_data['nutriments'].get('sodium', 0.0)
            )

            # Ajout du produit à la session de la base de données et enregistrement
            db.session.add(product)
            db.session.commit()

            return jsonify({'status': 'success', 'message': 'Product data saved to the database!'})
        else:
            return jsonify({'status': 'error', 'message': 'Product data not found in the response'}), 500

    except Exception as e:
        # Gestion des erreurs et renvoi d'une réponse appropriée
        print('Error:', str(e))
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500


from flask_login import login_required

from flask_login import current_user
@auth_blueprint.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    form = AlertForm()

    if form.validate_on_submit():
        try:
            existing_product = Product.query.filter_by(id=form.barcode.data).first()
            if existing_product:
                alert = Alert(
                    product_name=existing_product.product_name,
                    barcode=form.barcode.data,
                    description=form.description.data,
                    user_id=current_user.id 
                )
                db.session.add(alert)
                db.session.commit()
                flash('Votre signalement a été enregistré avec succès.', 'success')
            else:
                flash('Le produit spécifié n\'existe pas.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'enregistrement: {str(e)}', 'danger')
        return redirect(url_for('auth.alerts'))
    else:
        flash('Le formulaire n\'est pas valide. Veuillez vérifier vos données.', 'danger')

    return render_template('report.html', form=form)


from app.models import Alert
@auth_blueprint.route('/alerts')
@login_required
def alerts():
    try:
        alerts = Alert.query.all()
        return render_template('alerts.html', alerts=alerts)
    except Exception as e:
        # Vous pouvez ajouter un logging ici pour les erreurs
        flash(f'Une erreur est survenue: {str(e)}', 'danger')
        return render_template('alerts.html')
