from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.database.connection import DatabaseConnection
from app.controllers.model.pokedex_model import PokedexModel
from app.controllers.model.message_model import MessageModel

def pokedex_blueprint():
    bp = Blueprint('pokedex', __name__)

    # 1. IKUSI POKEDEX
    @bp.route('/pokedex')
    def view_pokedex():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user_id = session['user_id']
        db = DatabaseConnection()
        poke_model = PokedexModel(db)
        
        captured = poke_model.get_captured_list(user_id)
        missing = poke_model.get_missing_list(user_id)
        
        return render_template('pokedex.html', captured=captured, missing=missing)

    # 2. HARRAPATU / ASKATU
    @bp.route('/pokedex/toggle/<int:pokemon_id>/<action>')
    def toggle_capture(pokemon_id, action):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        user_id = session['user_id']
        db = DatabaseConnection()
        poke_model = PokedexModel(db)
        
        # Izena bilatu mezurako
        query = "SELECT Izena FROM Pokemon_Pokedex WHERE PokemonID = ?"
        result = db.get_one(query, (pokemon_id,))
        pokemon_name = result['Izena'] if result else f"Pokémon #{pokemon_id}"

        msg_model = MessageModel(db)

        if action == 'add':
            poke_model.mark_as_captured(user_id, pokemon_id)
            # Mezua (Neutrala, 'Taldea' gabe)
            msg_text = f"{pokemon_name} harrapatu du!"
            msg_model.create_message(user_id, msg_text)
            
            flash('Pokémon harrapatuta! 🎉', 'success')
            
        elif action == 'remove':
            poke_model.unmark_captured(user_id, pokemon_id)
            # Mezua (Neutrala)
            msg_model.create_message(user_id, f"{pokemon_name} askatu du.")
            
            flash('Pokémon askatuta.', 'info')
            
        return redirect(url_for('pokedex.view_pokedex'))



    @bp.route('/pokedex/search')
    def search():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        db = DatabaseConnection()
        poke_model = PokedexModel(db)
        
        # 1. Parametro guztiak jaso URLtik
        name_query = request.args.get('name', '')
        type_query = request.args.get('type', 'Guztiak')
        gen_query = request.args.get('gen', 'Guztiak')   
        evo_query = request.args.get('evo', 'Guztiak')   
        
        # 2. Iragazkiak prestatu ('Guztiak' kudeatu)
        type_filter = type_query if type_query != 'Guztiak' else None
        gen_filter = gen_query if gen_query != 'Guztiak' else None
        evo_filter = evo_query if evo_query != 'Guztiak' else None
        
        # 3. Bilaketa egin (4 parametroekin)
        results = poke_model.search_pokemon(name_query, type_filter, gen_filter, evo_filter)
        
        # 4. Desplegableak betetzeko datuak lortu
        all_types = poke_model.get_all_types()
        all_gens = poke_model.get_all_generations() 
        
        return render_template('search_pokemon.html', 
                             pokemon_list=results, 
                             types=all_types,
                             generations=all_gens,      
                             current_name=name_query,
                             current_type=type_query,
                             current_gen=gen_query,     
                             current_evo=evo_query)     
    

    @bp.route('/pokedex/details/<int:pokemon_id>')
    def view_details(pokemon_id):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
            
        db = DatabaseConnection()
        poke_model = PokedexModel(db)
        
        # 1. Oinarrizko datuak
        pokemon = poke_model.get_pokemon_by_id(pokemon_id)
        if not pokemon:
            flash("Ez da Pokemon hori aurkitu.", "danger")
            return redirect(url_for('pokedex.search'))
            
        # 2. Motak
        types = poke_model.get_pokemon_types(pokemon_id)
        
        # 3. Ahuleziak (BERRIA)
        weaknesses = poke_model.get_weaknesses(types)
        strengths = poke_model.get_strengths(types)  
        
        # 4. Eboluzioak (BERRIA)
        evolutions = poke_model.get_evolution_family(pokemon_id)
        
        return render_template('pokemon_details.html', 
                             p=pokemon, 
                             types=types,
                             weaknesses=weaknesses,
                             strengths=strengths,  
                             evolutions=evolutions,  
                             previous_filters=request.args)
    
    return bp