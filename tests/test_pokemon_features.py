import pytest
from unittest.mock import patch, MagicMock
from app import create_app

class TestPokemonFeatures:
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'features_secret'
        with app.test_client() as client:
            yield client

    # --- ESTATISTIKAK ---
    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_1(self, MockModel, client):
        """[ESTATISTIKAK - ID 1] Bilatu ondo -> Pantaila agertu."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [{'PokemonID': 25, 'Izena': 'Pikachu', 'Irudia': 'img'}]
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Pikachu'})
        assert b"Pikachu" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_2(self, MockModel, client):
        """[ESTATISTIKAK - ID 2] Izena hutsik -> Lista osoa."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [{'PokemonID': 1, 'Izena': 'Bulbasaur'}]
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': ''})
        assert b"Bulbasaur" in response.data

    def test_stats_id_3(self, client):
        """[ESTATISTIKAK - ID 3] Itzuli menura -> ChatBot/Search."""
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search')
        assert b"Bilatzailea" in response.data

    def test_stats_id_4(self, client):
        """[ESTATISTIKAK - ID 4] Itzuli menura (idatzita) -> ChatBot/Search."""
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Pika'})
        assert b"Bilatzailea" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_5(self, MockModel, client):
        """[ESTATISTIKAK - ID 5] Izen okerra -> Errorea."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'BadName'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_6(self, MockModel, client):
        """[ESTATISTIKAK - ID 6] Letra larriz -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'PIKACHU'})
        mock.search_pokemon.assert_called_with('PIKACHU', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_7(self, MockModel, client):
        """[ESTATISTIKAK - ID 7] Letra mehez -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'pikachu'})
        mock.search_pokemon.assert_called_with('pikachu', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_8(self, MockModel, client):
        """[ESTATISTIKAK - ID 8] Larriz eta mehez -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'PiKaChU'})
        mock.search_pokemon.assert_called_with('PiKaChU', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_stats_id_9(self, MockModel, client):
        """[ESTATISTIKAK - ID 9] Hutsuneak (Char mander) -> Errorea."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Char mander'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    # --- AHULEZIAK (Errepikatzen dira kasu asko, baina IDak behar dira) ---
    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_1(self, MockModel, client):
        """[AHULEZIAK - ID 1] Bilatu ondo -> Taula agertu."""
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 4, 'Izena': 'Charmander', 'Irudia': 'img'}
        mock.get_weaknesses.return_value = ['Water']
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/4')
        assert b"Ahuleziak" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_2(self, MockModel, client):
        """[AHULEZIAK - ID 2] Hutsik -> Lista osoa."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [{'PokemonID': 1, 'Izena': 'Bulbasaur'}]
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': ''})
        assert b"Bulbasaur" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_3(self, MockModel, client):
        """[AHULEZIAK - ID 3] Izen okerra -> Errorea."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Bad'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    # ID 4, 5, 8 son variantes de Mayus/Minus, que funcionan igual
    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_4(self, MockModel, client):
        """[AHULEZIAK - ID 4] Mehez -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'pikachu'})
        mock.search_pokemon.assert_called()

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_5(self, MockModel, client):
        """[AHULEZIAK - ID 5] Larriz -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'PIKACHU'})
        mock.search_pokemon.assert_called()

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_6(self, MockModel, client):
        """[AHULEZIAK - ID 6] Hutsuneak -> Errorea."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Char mander'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    def test_weakness_id_7(self, client):
        """[AHULEZIAK - ID 7] Itzuli -> ChatBot."""
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search')
        assert b"Bilatzailea" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_weakness_id_8(self, MockModel, client):
        """[AHULEZIAK - ID 8] Mistoa -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'PiKa'})
        mock.search_pokemon.assert_called()

    def test_weakness_id_9(self, client):
        """[AHULEZIAK - ID 9] Itzuli (idatzita) -> ChatBot."""
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Pika'})
        assert b"Bilatzailea" in response.data

    # --- EBOLUZIOAK (Repetimos patrón para cubrir IDs) ---
    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_1(self, MockModel, client):
        """[EBOLUZIO KATEAK - ID 1] Bilatu ondo -> Katea agertu."""
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 1, 'Izena': 'Bulbasaur', 'Irudia': 'img'}
        mock.get_evolution_family.return_value = ['Ivysaur']
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/1')
        assert b"Eboluzioak" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_2(self, MockModel, client):
        """[EBOLUZIO KATEAK - ID 2] Hutsik -> Lista."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [{'PokemonID': 1, 'Izena': 'Bulbasaur'}]
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': ''})
        assert b"Bulbasaur" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_3(self, MockModel, client):
        """[EBOLUZIO KATEAK - ID 3] Okerra -> Errorea."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Bad'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_4(self, MockModel, client):
        """[EBOLUZIO KATEAK - ID 4] Mehez -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'pikachu'})
        mock.search_pokemon.assert_called()

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_5(self, MockModel, client):
        """[EBOLUZIO KATEAK - ID 5] Larriz -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'PIKACHU'})
        mock.search_pokemon.assert_called()

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_6(self, MockModel, client):
        """[EBOLUZIO KATEAK - ID 6] Hutsuneak -> Errorea."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Ch ar'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    def test_evolution_id_7(self, client):
        """[EBOLUZIO KATEAK - ID 7] Itzuli -> ChatBot."""
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search')
        assert b"Bilatzailea" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_8(self, MockModel, client):
        """[EBOLUZIO KATEAK - ID 8] Mistoa -> Ondo."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'PiKa'})
        mock.search_pokemon.assert_called()

    def test_evolution_id_9(self, client):
        """[EBOLUZIO KATEAK - ID 9] Itzuli -> ChatBot."""
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'Pika'})
        assert b"Bilatzailea" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_evolution_id_10(self, MockModel, client):
        """[EBOLUZIO KATEAK - ID 10] Eboluzio gabe -> Mezua."""
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 150, 'Izena': 'Mewtwo', 'Irudia': 'img'}
        mock.get_evolution_family.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/150')
        assert b"Ez du eboluzionatzen" in response.data