from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.database.connection import DatabaseConnection
from app.controllers.model.friend_model import FriendModel
from app.controllers.model.message_model import MessageModel

def friend_blueprint():
    bp = Blueprint('friends', __name__)

    @bp.route('/friends', methods=['GET', 'POST'])
    def index():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        user_id = session['user_id']
        db = DatabaseConnection()
        friend_model = FriendModel(db)
        
        # 1. Nire lagunak lortu beti
        my_friends = friend_model.get_followed_users(user_id)
        search_results = []
        search_query = ""

        # 2. Bilaketa logika
        if request.method == 'POST':
            search_query = request.form.get('search_query', '').strip()
            if search_query:
                search_results = friend_model.search_users_to_add(user_id, search_query)
        
        return render_template('friends.html', 
                             friends=my_friends, 
                             results=search_results,
                             last_query=search_query)

    @bp.route('/friends/add/<int:friend_id>')
    def add(friend_id):
        if 'user_id' not in session: return redirect(url_for('auth.login'))
        
        user_id = session['user_id']
        db = DatabaseConnection()
        friend_model = FriendModel(db)
        msg_model = MessageModel(db)

        # Lagunak egin
        friend_model.add_friend(user_id, friend_id)
        msg_model.create_message(user_id, f"[Soziala] Lagun berria gehitu du! (ID: {friend_id})")
        # Jakinarazpena sortu
        msg_model.create_message(user_id, f"[Soziala] Lagun berria gehitu duzu! (ID: {friend_id})")
        
        flash('Laguna gehitu da! 🤝', 'success')
        return redirect(url_for('friends.index'))

    @bp.route('/friends/remove/<int:friend_id>')
    def remove(friend_id):
        if 'user_id' not in session: return redirect(url_for('auth.login'))
        
        user_id = session['user_id']
        db = DatabaseConnection()
        friend_model = FriendModel(db)
        
        friend_model.remove_friend(user_id, friend_id)
        flash('Laguna ezabatu da.', 'info')
        return redirect(url_for('friends.index'))
    
    return bp