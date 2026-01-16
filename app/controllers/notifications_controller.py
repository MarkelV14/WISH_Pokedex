from flask import Blueprint, render_template, session, redirect, url_for, request
from app.database.connection import DatabaseConnection
from app.controllers.model.message_model import MessageModel
from app.controllers.model.user_model import UserModel

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
        
        
        # El botón envía ?filter=mine, así que debemos capturarlo aquí.
        filter_type = request.args.get('filter', 'all')
        
        # Aplicar la lógica según el filtro
        if filter_type == 'mine':
            messages = msg_model.get_my_messages(user_id)
        else:
            messages = msg_model.get_all_messages()
            
        return render_template('notifications.html', 
                             messages=messages, 
                             filter_type=filter_type, # Pasamos el tipo real para que el botón cambie
                             current_user=username)

    # --- (Checkboxes) ---
    @bp.route('/notifications/filter', methods=['GET', 'POST'])
    def filter_notifications():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        db = DatabaseConnection()
        
        # GET: Mostrar pantalla de selección
        if request.method == 'GET':
            user_model = UserModel(db)
            
            all_users = user_model.get_all_users() 
            return render_template('notifications_filter.html', 
                                 users=all_users, 
                                 current_user=session['username'])
        
        # POST: Procesar el filtro seleccionado
        if request.method == 'POST':
            msg_model = MessageModel(db)
            
            filter_option = request.form.get('filter_users')
            
            if filter_option == 'all':
                 messages = msg_model.get_all_messages()
                 current_filter = 'all'
            else:
                 # Recoger IDs seleccionados
                 selected_ids = request.form.getlist('user_ids')
                 
                 
                 if hasattr(msg_model, 'get_messages_by_users'):
                    messages = msg_model.get_messages_by_users(selected_ids)
                 else:
                    
                    messages = msg_model.get_all_messages()
                 
                 current_filter = 'custom'
            
            return render_template('notifications.html', 
                                 messages=messages, 
                                 filter_type=current_filter,
                                 current_user=session['username'])
    
    return bp