from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.database.connection import DatabaseConnection
from app.controllers.model.chatbot_model import ChatbotModel

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chatbot')
def menu():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('chatbot/menu.html')

# POKEMON HOBERENA (Zure Taldekoa)
@chatbot_bp.route('/chatbot/best', methods=['GET', 'POST'])
def best_pokemon():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    db = DatabaseConnection()
    model = ChatbotModel(db)
    user_id = session['user_id']
    
    selected_pokemon = None
    
    # Botoia sakatzean
    if request.method == 'POST':
        selected_pokemon = model.get_best_from_my_team(user_id)
        
        if not selected_pokemon:
            flash("Zure taldea hutsik dago! Joan 'Taldea Sortu' atalera.", "warning")
            
    return render_template('chatbot/best.html', pokemon=selected_pokemon)

# ... (Beste ibilbideak berdin) ...
@chatbot_bp.route('/chatbot/stats', methods=['GET', 'POST'])
def stats():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # 1. Konexioa eta Modeloa hasieratu (Beti behar ditugu, GET eta POST egiteko)
    db = DatabaseConnection()
    model = ChatbotModel(db)
    
    # 2. Lortu Pokemon guztien izenak (Autokonpletaturako)
    
    all_names = model.get_all_pokemon_names()
    
    found_pokemon = None
    
    if request.method == 'POST':
        
        search_term = request.form.get('pokemon_name')
        
        # 2. Eskakizuna: Izena hutsik badago
        if not search_term:
            flash("Errorea: Mesedez, idatzi Pokemon baten izena.", "danger")
        else:
            # Bilaketa egin
            found_pokemon = model.get_pokemon_by_name(search_term)
            
            # 5. eta 9. Eskakizunak: Ez bada aurkitzen
            if not found_pokemon:
                flash(f"Ez da Pokemon hori aurkitu: '{search_term}'", "danger")

    # 3. GARRANTZITSUA: 'all_names' aldagaia pasatu behar diogu HTMLari
    return render_template('chatbot/stats.html', 
                         pokemon=found_pokemon, 
                         all_names=all_names)

@chatbot_bp.route('/chatbot/matchups', methods=['GET', 'POST'])
def matchups():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    db = DatabaseConnection()
    model = ChatbotModel(db)
    
    # Autokonpletaturako izenak
    all_names = model.get_all_pokemon_names()
    
    pokemon = None
    types = []
    weaknesses = []
    strengths = []
    
    if request.method == 'POST':
        search_term = request.form.get('pokemon_name')
        
        # 2. Eskakizuna: Input hutsa
        if not search_term:
            flash("Errorea: Mesedez, idatzi Pokemon baten izena.", "danger")
        else:
            # Bilaketa egin (6. Eskakizuna: Espazioak baditu, ez du aurkituko)
            pokemon = model.get_pokemon_by_name(search_term)
            
            # 3. eta 6. Eskakizunak: Ez bada aurkitzen
            if not pokemon:
                flash(f"Ez da Pokemon hori aurkitu: '{search_term}'", "danger")
            else:
                # Pokemon aurkitu da! Orain datuak kalkulatu:
                pid = pokemon['PokemonID']
                types = model.get_pokemon_types(pid)         # Motak
                weaknesses = model.get_weaknesses(types)     # Ahuleziak
                strengths = model.get_strengths(types)       # Indarguneak

    return render_template('chatbot/matchups.html', 
                         pokemon=pokemon,
                         types=types,
                         weaknesses=weaknesses,
                         strengths=strengths,
                         all_names=all_names)

@chatbot_bp.route('/chatbot/evolution', methods=['GET', 'POST'])
def evolution():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    db = DatabaseConnection()
    model = ChatbotModel(db)
    
    all_names = model.get_all_pokemon_names()
    
    current_pokemon = None
    evolution_chain = []  # <--- HEMEN GORDETZEN DIRA HURRENGO GUZTIAK
    no_evolution_msg = False
    
    if request.method == 'POST':
        search_term = request.form.get('pokemon_name')
        
        if not search_term:
            flash("Errorea: Mesedez, idatzi Pokemon baten izena.", "danger")
        else:
            current_pokemon = model.get_pokemon_by_name(search_term)
            
            if not current_pokemon:
                flash(f"Ez da Pokemon hori aurkitu: '{search_term}'", "danger")
            else:
                # --- (WHILE LOOP) ---
                # 1. Begiratu ea lehenengoak eboluziorik duen
                next_id = current_pokemon['EboluzioaID']
                
                # 2. Eboluzioa duen bitartean, jarraitu bilatzen
                while next_id:
                    # Hurrengoaren datuak lortu
                    next_poke = model.get_pokemon_by_id(next_id)
                    
                    if next_poke:
                        # Zerrendara gehitu
                        evolution_chain.append(next_poke)
                        # Hurrengoaren IDa prestatu hurrengo itzulirako
                        next_id = next_poke['EboluzioaID']
                    else:
                        # Datu-basean ez badago hurrengoa (segurtasuna), gelditu
                        break
                
                # 3. Zerrenda hutsik badago, esan nahi du ez daukala eboluziorik
                if not evolution_chain:
                    no_evolution_msg = True

    return render_template('chatbot/evolution.html', 
                         current_pokemon=current_pokemon,
                         evolution_chain=evolution_chain, # <--- Zerrenda osoa pasatu
                         no_evolution_msg=no_evolution_msg,
                         all_names=all_names)
