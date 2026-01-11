from flask import Blueprint, render_template, session, redirect, url_for, request
from app.database.connection import DatabaseConnection
from app.controllers.model.message_model import MessageModel
from app.controllers.model.user_model import UserModel # Necesario para listar usuarios

def notifications_blueprint():
    bp = Blueprint('notifications', __name__)

    @bp.route('/notifications')
    def view_notifications():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        user_id = session['user_id']
        username = session['username']
        db = DatabaseConnection()
        msg_model = MessageModel(db)
        
        # Lógica original + soporte para filtro customizado que viene de POST
        messages = msg_model.get_all_messages()
            
        return render_template('notifications.html', 
                             messages=messages, 
                             filter_type='all',
                             current_user=username)

    # --- NUEVA RUTA PARA CUMPLIR CON LOS TESTS ---
    @bp.route('/notifications/filter', methods=['GET', 'POST'])
    def filter_notifications():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        db = DatabaseConnection()
        
        # GET: Mostrar pantalla de selección (Checkboxes)
        if request.method == 'GET':
            user_model = UserModel(db)
            all_users = user_model.get_all_users() # Necesitas este método en UserModel
            return render_template('notifications_filter.html', 
                                 users=all_users, 
                                 current_user=session['username'])
        
        # POST: Procesar el filtro "Eguneratu"
        if request.method == 'POST':
            msg_model = MessageModel(db)
            
            # Si viene "all" o una lista de IDs
            if request.form.get('filter_users') == 'all':
                 messages = msg_model.get_all_messages()
            else:
                 # Recoger IDs seleccionados (checkboxes)
                 selected_ids = request.form.getlist('user_ids')
                 # Nota: Necesitarás implementar get_messages_by_users en MessageModel
                 messages = msg_model.get_messages_by_users(selected_ids) 
            
            # Renderizar notifications.html con los mensajes filtrados
            return render_template('notifications.html', 
                                 messages=messages, 
                                 filter_type='custom',
                                 current_user=session['username'])
    
    return bp