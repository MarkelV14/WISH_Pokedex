from flask import Blueprint, render_template, session, redirect, url_for, request
from app.database.connection import DatabaseConnection
from app.controllers.model.message_model import MessageModel

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
        
        # FILTROA LORTU (URL parameter: ?filter=mine)
        filter_type = request.args.get('filter', 'all') # Por defecto 'all'
        
        if filter_type == 'mine':
            messages = msg_model.get_my_messages(user_id)
        else:
            messages = msg_model.get_all_messages()
            
        return render_template('notifications.html', 
                             messages=messages, 
                             filter_type=filter_type,
                             current_user=username)
    
    return bp