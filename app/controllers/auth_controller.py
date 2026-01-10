from flask import Blueprint, request, render_template, redirect, url_for, flash, session, make_response
from app.database.connection import DatabaseConnection
from app.controllers.model.user_model import UserModel
from app.controllers.model.auth_model import AuthModel
# Importamos el TeamModel para contar los pokémon
from app.controllers.model.team_model import TeamModel
from app.controllers.model.pokedex_model import PokedexModel
import datetime

def auth_blueprint():
    bp = Blueprint('auth', __name__)
    db = DatabaseConnection()
    user_model = UserModel(db)
    auth_model = AuthModel(db)
    
    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            remember_me = request.form.get('remember_me') == 'on'
            
            user = user_model.verify_password(username, password)
            
            if user:
                # Comprobar si el usuario está aprobado
                if not user['is_approved']:
                    flash('Zure kontua oraindik ez da onartu. Itxaron administratzailearen baieztapena', 'warning')
                    return redirect(url_for('auth.login'))
                
                # Crear sesión
                session_token = auth_model.create_session(user['id'], remember_me)
                
                # Guardar en sesión de Flask
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                session['token'] = session_token
                
                # Si es "recordarme", guardar cookie
                response = make_response(redirect(url_for('auth.dashboard')))
                if remember_me:
                    expires = datetime.datetime.now() + datetime.timedelta(days=30)
                    response.set_cookie('remember_token', session_token, expires=expires)
                
                flash('Saioa ongi hasi duzu!', 'success')
                return response
            else:
                flash('Erabiltzailea edo pasahitza okerrak', 'danger')
        
        return render_template('login.html')
    
    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Validaciones
            if password != confirm_password:
                flash('Pasahitzak ez datoz bat', 'danger')
                return redirect(url_for('auth.register'))
            
            if len(password) < 6:
                flash('Pasahitzak gutxienez 6 karaktere izan behar ditu', 'danger')
                return redirect(url_for('auth.register'))
            
            try:
                user_id = user_model.create_user(username, email, password)
                flash('Erregistroa ondo burutu da! Administratzaileak zure kontua baieztatu behar du. Mezu bat bidaliko dizugu onartzen denean.', 'success')
                return redirect(url_for('auth.login'))
            except ValueError as e:
                flash(str(e), 'danger')
        
        return render_template('register.html')
    
    @bp.route('/logout')
    def logout():
        if 'token' in session:
            auth_model.delete_session(session['token'])
        
        # Limpiar sesión
        session.clear()
        
        # Limpiar cookie
        response = make_response(redirect(url_for('auth.login')))
        response.set_cookie('remember_token', '', expires=0)
        
        flash('Saioa ongi itxi duzu', 'info')
        return response
    
    # --- AQUÍ ESTABA EL ERROR DE INDENTACIÓN (Ahora corregido) ---
    @bp.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            flash('Mesedez, hasi saioa', 'warning')
            return redirect(url_for('auth.login'))
        
        user = user_model.get_user_by_id(session['user_id'])
        if not user:
            flash('Erabiltzailea ez da aurkitu', 'danger')
            return redirect(url_for('auth.logout'))
        
        # 1. Contamos el equipo
        team_model = TeamModel(db)
        count = team_model.count_team_members(session['user_id'])
        
        # 2. NUEVO: Contamos la Pokédex (Capturados vs Faltan) 👇
        pokedex_model = PokedexModel(db)
        stats = pokedex_model.get_counts(session['user_id'])
        
        # 3. Pasamos 'poke_stats=stats' a la vista 👇
        return render_template('dashboard.html', 
                             user=dict(user), 
                             team_count=count, 
                             poke_stats=stats)
    
    @bp.route('/')
    def index():
        return render_template('index.html')
    
    @bp.before_app_request
    def load_logged_in_user():
        # Verificar si hay usuario en sesión
        user_id = session.get('user_id')
        
        # Si no hay sesión pero hay cookie "recordarme"
        if not user_id and 'remember_token' in request.cookies:
            token = request.cookies.get('remember_token')
            session_data = auth_model.validate_session(token)
            
            if session_data:
                session['user_id'] = session_data['user_id']
                session['username'] = session_data['username']
                # Obtener rol del usuario
                user = user_model.get_user_by_id(session_data['user_id'])
                if user:
                    session['role'] = user['role']
                session['token'] = token
    
    return bp