from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.database.connection import DatabaseConnection
from app.controllers.model.team_model import TeamModel
from app.controllers.model.message_model import MessageModel

def team_blueprint():
    bp = Blueprint('team', __name__)
    
    #  CREAR / AÑADIR (Sortu Taldea)
    @bp.route('/team/create', methods=['GET', 'POST'])
    def create_team():
        if 'user_id' not in session:
            flash('Saioa hasi behar duzu lehenengo.', 'warning')
            return redirect(url_for('auth.login'))

        db = DatabaseConnection()
        team_model = TeamModel(db)
        user_id = session['user_id']
        
        current_team = team_model.get_user_team(user_id)
        team_count = len(current_team) if current_team else 0
        all_names = team_model.get_all_pokemon_names()

        if request.method == 'POST':
            if 'finish_team' in request.form:
                
                if team_count < 6:
                    flash('Taldeak 6 Pokémon izan behar ditu gordetzeko!', 'danger')
                    return redirect(url_for('team.create_team'))
                
                
                flash('Aldaketak gordeta!', 'success')
                return redirect(url_for('auth.dashboard'))

            pokemon_name = request.form.get('pokemon_name')
            
            
            if team_count >= 6:
                flash('Taldea beteta dago! Joan "Taldea Kudeatu" atalera ezabatzeko.', 'warning')
            elif not pokemon_name:
                flash('Mesedez, idatzi Pokémon baten izena.', 'danger')
            else:
                pokemon = team_model.get_pokemon_by_name(pokemon_name)
                
                if pokemon:
                    # --- CORRECCIÓN DE DUPLICADOS ---
                    already_in_team = False
                    if current_team:
                        for member in current_team:
                            if member['Izena'] == pokemon['Izena']:
                                already_in_team = True
                                break
                    
                    if already_in_team:
                        flash(f'{pokemon["Izena"]} jadanik zure taldean dago!', 'warning')
                    else:
                        team_model.add_pokemon_to_team(user_id, pokemon['PokemonID'], pokemon['Izena'])
                        
                        msg_model = MessageModel(db)
                        msg_text = f" {pokemon['Izena']} taldera gehitu du!" 
                        msg_model.create_message(user_id, msg_text)
                        
                        flash(f'{pokemon["Izena"]} gehituta!', 'success')
                        return redirect(url_for('team.create_team'))
                    # --------------------------------
                else:
                    flash(f'Ez da aurkitu "{pokemon_name}".', 'danger')

        return render_template('create_team.html', team=current_team, count=team_count, all_pokemon_names=all_names)
    
    # RUTA 2: GESTIONAR / BORRAR (Taldea Kudeatu)
    @bp.route('/team/manage')
    def manage_team():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        db = DatabaseConnection()
        team_model = TeamModel(db)
        user_id = session['user_id']
        
        current_team = team_model.get_user_team(user_id)
        
        return render_template('manage_team.html', team=current_team)

    # RUTA 3: BORRAR (Ezabatu)
    @bp.route('/team/delete/<int:entry_id>')
    def delete_pokemon(entry_id):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user_id = session['user_id']
        db = DatabaseConnection()
        team_model = TeamModel(db)
        
        team_model.delete_pokemon_from_team(user_id, entry_id)
        
        msg_model = MessageModel(db)
        msg_model.create_message(user_id, "Pokémon bat taldetik ezabatu du.")
        
        flash('Pokémona taldetik ezabatu da.', 'info')
        
        return redirect(url_for('team.manage_team'))
    
    return bp