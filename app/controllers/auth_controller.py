from flask import Blueprint, request, render_template, redirect, url_for, flash, session, make_response
from app.database.connection import DatabaseConnection
from app.controllers.model.user_model import UserModel
from app.controllers.model.auth_model import AuthModel
from app.controllers.model.team_model import TeamModel
from app.controllers.model.pokedex_model import PokedexModel
import datetime
import re  # Necesario para validar email

def auth_blueprint():
    bp = Blueprint('auth', __name__)
    db = DatabaseConnection()
    user_model = UserModel(db)
    auth_model = AuthModel(db)
    
    # ---  (SAIOA HASI) ---
    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            #  Botón registro (Gestionado en HTML con <a>, pero si fuera submit...)
            if 'register_btn' in request.form:
                 return redirect(url_for('auth.register'))

            username = request.form.get('username')
            password = request.form.get('password')
            remember_me = request.form.get('remember_me') == 'on'
            
            # Campos vacíos
            if not username or not password:
                flash('Eremu guztiak bete behar dira', 'danger')
                return render_template('login.html')

            user = user_model.verify_password(username, password)
            
            #  Usuario no existe o contraseña mal
            if user:
                if not user['is_approved']:
                    flash('Zure kontua oraindik ez da onartu. Itxaron administratzailearen baieztapena', 'warning')
                    return redirect(url_for('auth.login'))
                
                #Login correcto
                session_token = auth_model.create_session(user['id'], remember_me)
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                session['token'] = session_token
                
                response = make_response(redirect(url_for('auth.dashboard')))
                if remember_me:
                    expires = datetime.datetime.now() + datetime.timedelta(days=30)
                    response.set_cookie('remember_token', session_token, expires=expires)
                
                flash('Saioa ongi hasi duzu!', 'success')
                return response
            else:
                flash('Erabiltzailea edo pasahitza okerrak', 'danger')
        
        return render_template('login.html')
    
    # ---  (ERREGISTRATU) ---
    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            #  Cancelar (Gestionado en HTML, pero por si acaso)
            if 'cancel' in request.form:
                return redirect(url_for('auth.login'))

            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            
            #  Campos vacíos
            if not username or not email or not password or not confirm_password:
                flash('Eremu guztiak bete behar dira', 'danger')
                return render_template('register.html')

            #  Pasahitz ezberdinak
            if password != confirm_password:
                flash('Pasahitzak ez datoz bat', 'danger')
                return render_template('register.html')
            
            #  Pasahitz laburregia
            if len(password) < 6:
                flash('Pasahitzak gutxienez 6 karaktere izan behar ditu', 'danger')
                return render_template('register.html')

            #  Izen motzegia ( min 3 chars)
            if len(username) < 3:
                flash('Erabiltzaile izena motzegia da', 'danger')
                return render_template('register.html')

            #  Izen luzegia ( max 20 chars)
            if len(username) > 20:
                flash('Erabiltzaile izena luzegia da', 'danger')
                return render_template('register.html')

            #  Email formatu okerra
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                flash('Email formatua okerra da', 'danger')
                return render_template('register.html')
            
            try:
                #  (Duplicado) y Caso 1 (Éxito)
                user_id = user_model.create_user(username, email, password)
                flash('Erregistroa ondo burutu da! Administratzaileak zure kontua baieztatu behar du.', 'success')
                return redirect(url_for('auth.login'))
            except ValueError as e:
                flash(str(e), 'danger') # Aquí salta el error de duplicado del modelo
        
        return render_template('register.html')
    
    # ---  (ERABILTZAILE KUDEAKETA)  ---
    @bp.route('/profile/edit', methods=['GET', 'POST'])
    def edit_profile():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        user_id = session['user_id']
        
        if request.method == 'POST':
            #  Cancelar / Atrás
            if 'back' in request.form:
                return redirect(url_for('auth.dashboard'))

            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            bio = request.form.get('bio', '').strip()
            
            # Casos 2, 3, 4, 5: Campos vacíos
            if not username or not email or not bio:
                flash('Eremu guztiak bete behar dira (Bio barne)', 'danger')
                return redirect(url_for('auth.edit_profile'))

            #  Formato nombre/bio (Simulamos validación simple)
            if len(username) < 3:
                flash('Izena motzegia da', 'danger')
                return redirect(url_for('auth.edit_profile'))
            
            if len(bio) > 100: # Validación bio
                flash('Biografia luzegia da', 'danger')
                return redirect(url_for('auth.edit_profile'))

            #  Email formato
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                flash('Email formatua okerra da', 'danger')
                return redirect(url_for('auth.edit_profile'))

            try:
                # Caso 1 (Éxito) y Caso 9 (Email duplicado)
                
                user_model.update_user(user_id, username=username, email=email, bio=bio)
                flash('Profila ondo editatu da', 'success')
                return redirect(url_for('auth.dashboard'))
            except Exception as e:
                flash('Errorea: Email hori sisteman existitzen da jada', 'danger')
                return redirect(url_for('auth.edit_profile'))

        # GET: Cargar datos actuales
        user = user_model.get_user_by_id(user_id)
        return render_template('edit_profile.html', user=user)

    @bp.route('/logout')
    def logout():
        if 'token' in session:
            auth_model.delete_session(session['token'])
        session.clear()
        response = make_response(redirect(url_for('auth.login')))
        response.set_cookie('remember_token', '', expires=0)
        flash('Saioa ongi itxi duzu', 'info')
        return response
    
    @bp.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            flash('Mesedez, hasi saioa', 'warning')
            return redirect(url_for('auth.login'))
        
        user = user_model.get_user_by_id(session['user_id'])
        if not user:
            flash('Erabiltzailea ez da aurkitu', 'danger')
            return redirect(url_for('auth.logout'))
        
        team_model = TeamModel(db)
        count = team_model.count_team_members(session['user_id'])
        
        pokedex_model = PokedexModel(db)
        stats = pokedex_model.get_counts(session['user_id'])
        
        return render_template('dashboard.html', user=dict(user), team_count=count, poke_stats=stats)
    
    @bp.route('/')
    def index():
        return render_template('index.html')
    
    @bp.before_app_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if not user_id and 'remember_token' in request.cookies:
            token = request.cookies.get('remember_token')
            session_data = auth_model.validate_session(token)
            if session_data:
                session['user_id'] = session_data['user_id']
                session['username'] = session_data['username']
                user = user_model.get_user_by_id(session_data['user_id'])
                if user:
                    session['role'] = user['role']
                session['token'] = token
    
    return bp