from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.database.connection import DatabaseConnection
from app.controllers.model.user_model import UserModel

def admin_blueprint():
    bp = Blueprint('admin', __name__)
    db = DatabaseConnection()
    user_model = UserModel(db)
    
    @bp.before_request
    def check_admin():
        if 'user_id' not in session:
            flash('Administratzaile gisa saioa hasi behar duzu', 'warning')
            return redirect(url_for('auth.login'))
        
        user_id = session.get('user_id')
        role = user_model.get_user_role(user_id)
        
        if role != 'admin':
            flash('Baimenik ez duzu orri honetarako', 'danger')
            return redirect(url_for('auth.dashboard'))
    
    @bp.route('/admin')
    def admin_panel():
        pending_users = user_model.get_pending_users()
        all_users = user_model.get_all_users()
        return render_template('admin_panel.html', 
                             pending_users=pending_users,
                             all_users=all_users)
    
    @bp.route('/admin/approve/<int:user_id>')
    def approve_user(user_id):
        user_model.approve_user(user_id)
        flash(f'Erabiltzailea onartu da (ID: {user_id})', 'success')
        return redirect(url_for('admin.admin_panel'))
    
    @bp.route('/admin/reject/<int:user_id>')
    def reject_user(user_id):
        user_model.reject_user(user_id)
        flash(f'Erabiltzailea baztertu da (ID: {user_id})', 'warning')
        return redirect(url_for('admin.admin_panel'))
    
    @bp.route('/admin/delete/<int:user_id>')
    def delete_user(user_id):
        # Prevenir que el admin se elimine a sí mismo
        if session.get('user_id') == user_id:
            flash('Ezin duzu zure burua ezabatu', 'danger')
            return redirect(url_for('admin.admin_panel'))
        
        user_model.delete_user_permanently(user_id)
        flash(f'Erabiltzailea ezabatu da (ID: {user_id})', 'danger')
        return redirect(url_for('admin.admin_panel'))
    
    return bp
