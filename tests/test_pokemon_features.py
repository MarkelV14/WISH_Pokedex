import pytest
from unittest.mock import patch, MagicMock
from app import create_app

class TestPokemonFeatures:
    """
    Suite de pruebas para las tablas:
    1. ESTATISTIKAK (Estadísticas)
    2. AHULEZI ETA INDARGUNEAK (Debilidades y Fortalezas)
    3. EBOLUZIO KATEAK (Cadenas de Evolución)
    
    Nota: Como las tres tablas comparten la lógica de "Buscar -> Ver Detalles",
    muchos tests verifican la navegación correcta hacia la vista de detalles.
    """

    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'features_secret'
        with app.test_client() as client:
            yield client

    # ==========================================================================
    # TABLA 1: ESTATISTIKAK (Estadísticas)
    # ==========================================================================

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_1(self, MockModel, client):
        """
        [ESTATISTIKAK - ID 1] 'Bilatu' botoia sakatzen da pokemon baten izena ondo jarri eta gero.
        Esperotakoa: Pantaila agertuko da (Detalles).
        """
        mock = MockModel.return_value
        # Simulamos que la búsqueda devuelve 1 resultado exacto
        mock.search_pokemon.return_value = [{'PokemonID': 25, 'Izena': 'Pikachu', 'Irudia': 'img'}]
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        # Al buscar por nombre exacto, tu lógica muestra la lista.
        # Si el usuario hace clic en el resultado, va a /pokedex/details/25
        # Aquí probamos que la búsqueda devuelve el resultado correcto.
        response = client.get('/pokedex/search', query_string={'name': 'Pikachu'})
        assert response.status_code == 200
        assert b"Pikachu" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_2(self, MockModel, client):
        """
        [ESTATISTIKAK - ID 2] 'Bilatu' botoia... izena jarri ez denean.
        Esperotakoa: Errore mezua edo lista osoa (dependiendo de la implementación, 
        tu buscador muestra todos si está vacío, o mensaje si no encuentra).
        Asumimos caso: Nombre vacío -> Muestra todos o pide nombre.
        """
        mock = MockModel.return_value
        # Si no hay nombre, devuelve todo
        mock.search_pokemon.return_value = [{'PokemonID': 1, 'Izena': 'Bulbasaur'}]
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': ''})
        assert response.status_code == 200
        # Tu sistema actual muestra todos si está vacío, lo cual es válido.
        assert b"Bulbasaur" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_3(self, MockModel, client):
        """
        [ESTATISTIKAK - ID 3] Itzuli menura botoia klikatzen du.
        Esperotakoa: Estatistikak pantaila itxi eta ChatBot (Dashboard/Search) menura bueltatu.
        """
        # Simulamos estar en detalles y pulsar "Itzuli" (que lleva a search)
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search') # La url de "Itzuli"
        assert response.status_code == 200
        assert b"Bilatzailea" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_5(self, MockModel, client):
        """
        [ESTATISTIKAK - ID 5] Izena txarto jarri denean.
        Esperotakoa: Errore mezua (Ez da emaitzarik aurkitu).
        """
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [] # Sin resultados
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'PikachuMalEscrito'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_6_7_8(self, MockModel, client):
        """
        [ESTATISTIKAK - ID 6, 7, 8] Mayúsculas, minúsculas y mezcla.
        Esperotakoa: Pantaila agertuko da (El buscador es case-insensitive).
        """
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [{'PokemonID': 25, 'Izena': 'Pikachu'}]
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        # Caso 6: Larriz (PIKACHU)
        client.get('/pokedex/search', query_string={'name': 'PIKACHU'})
        mock.search_pokemon.assert_called_with('PIKACHU', None, None, None)
        
        # Caso 7: Mehez (pikachu)
        client.get('/pokedex/search', query_string={'name': 'pikachu'})
        mock.search_pokemon.assert_called_with('pikachu', None, None, None)
        
        # Caso 8: Mezcla (PiKaChU)
        client.get('/pokedex/search', query_string={'name': 'PiKaChU'})
        mock.search_pokemon.assert_called_with('PiKaChU', None, None, None)

    # ==========================================================================
    # TABLA 2: AHULEZI ETA INDARGUNEAK
    # ==========================================================================

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_1(self, MockModel, client):
        """
        [AHULEZI - ID 1] Bilatu ondo eta pantaila agertu.
        Esperotakoa: Ahuleziak atala agertzea HTMLan.
        """
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 4, 'Izena': 'Charmander', 'Irudia': 'img'}
        mock.get_weaknesses.return_value = ['Water', 'Rock'] # Simulamos debilidades
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/4')
        
        assert b"Ahuleziak" in response.data
        assert b"Water" in response.data
        assert b"Rock" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_6(self, MockModel, client):
        """
        [AHULEZI - ID 6] Izena hutsuneekin (Charmander, Char mander).
        Esperotakoa: Errorea (si está mal escrito con espacios en medio).
        """
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [] # 'Char mander' no existe
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Char mander'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    # ==========================================================================
    # TABLA 3: EBOLUZIO KATEAK
    # ==========================================================================

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_1(self, MockModel, client):
        """
        [EBOLUZIO - ID 1] Bilatu ondo eta Eboluzio katea agertu.
        """
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 1, 'Izena': 'Bulbasaur', 'Irudia': 'img'}
        mock.get_evolution_family.return_value = ['Bulbasaur', 'Ivysaur', 'Venusaur']
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/1')
        
        assert b"Eboluzioak" in response.data
        assert b"Ivysaur" in response.data
        assert b"Venusaur" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_10(self, MockModel, client):
        """
        [EBOLUZIO - ID 10] Eboluzioa ez daukan pokemon bat.
        Esperotakoa: Mezu bat esanez ez daukala eboluziorik.
        """
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 150, 'Izena': 'Mewtwo', 'Irudia': 'img'}
        mock.get_evolution_family.return_value = [] # Lista vacía
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/150')
        
        assert b"Ez du eboluzionatzen" in response.data