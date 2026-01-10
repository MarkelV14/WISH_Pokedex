import pytest
from unittest.mock import patch, MagicMock
from app import create_app

class TestPokedexSearch:
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'test_secret'
        with app.test_client() as client:
            yield client

    # --- LISTA ---
    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_list_id_1(self, MockModel, client):
        """[POKEMON LISTA - ID 1] Lista kargatzea."""
        mock = MockModel.return_value
        mock.get_captured_list.return_value = [{'PokemonID': 1, 'Izena': 'Bulbasaur', 'Irudia': 'img.png'}]
        mock.get_missing_list.return_value = [{'PokemonID': 4, 'Izena': 'Charmander', 'Irudia': 'img.png'}]
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex')
        assert response.status_code == 200
        assert b"Bulbasaur" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_list_id_2(self, MockModel, client):
        """[POKEMON LISTA - ID 2] Lista hutsik."""
        mock = MockModel.return_value
        mock.get_captured_list.return_value = []
        mock.get_missing_list.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex')
        assert b"Oraindik ez duzu" in response.data

    # --- BILATU ---
    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_1(self, MockModel, client):
        """[BILATU POKEMON - ID 1] Mota arabera."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [{'PokemonID': 4, 'Izena': 'Charmander', 'Irudia': 'img'}]
        mock.get_all_types.return_value = [{'Izena': 'Fire'}]
        mock.get_all_generations.return_value = [{'Zenbakia': 1}]
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'type': 'Fire'})
        mock.search_pokemon.assert_called_with('', 'Fire', None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_2(self, MockModel, client):
        """[BILATU POKEMON - ID 2] Generazio arabera."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'gen': '1'})
        mock.search_pokemon.assert_called_with('', None, '1', None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_3(self, MockModel, client):
        """[BILATU POKEMON - ID 3] Izen osoa."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'Pikachu'})
        mock.search_pokemon.assert_called_with('Pikachu', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_4(self, MockModel, client):
        """[BILATU POKEMON - ID 4] Eboluzio arabera."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'evo': 'Bai'})
        mock.search_pokemon.assert_called_with('', None, None, 'Bai')

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_5(self, MockModel, client):
        """[BILATU POKEMON - ID 5] Iragazki barik."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search')
        mock.search_pokemon.assert_called_with('', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_6(self, MockModel, client):
        """[BILATU POKEMON - ID 6] Ez da existitzen."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/search', query_string={'name': 'InventoMon'})
        assert b"Ez da emaitzarik aurkitu" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_7(self, MockModel, client):
        """[BILATU POKEMON - ID 7] Iragazki inkonpatibleak."""
        mock = MockModel.return_value
        mock.search_pokemon.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'type': 'Steel', 'gen': '1'})
        mock.search_pokemon.assert_called_with('', 'Steel', '1', None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_8(self, MockModel, client):
        """[BILATU POKEMON - ID 8] Izen zatia."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'name': 'Pik'})
        mock.search_pokemon.assert_called_with('Pik', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_9(self, MockModel, client):
        """[BILATU POKEMON - ID 9] Konbinatuak."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.get('/pokedex/search', query_string={'type': 'Fire', 'gen': '1', 'evo': 'Bai'})
        mock.search_pokemon.assert_called_with('', 'Fire', '1', 'Bai')

    # --- INFORMAZIOA ---
    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_info_id_1(self, MockModel, client):
        """[INFORMAZIOA ERAKUTSI - ID 1] Info ikusi."""
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 6, 'Izena': 'Charizard', 'Irudia': 'img'}
        mock.get_pokemon_types.return_value = ['Fire', 'Flying']
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/6')
        assert response.status_code == 200
        assert b"Charizard" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_info_id_2(self, MockModel, client):
        """[INFORMAZIOA ERAKUTSI - ID 2] Eboluzio gabe."""
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 150, 'Izena': 'Mewtwo', 'Irudia': 'img'}
        mock.get_evolution_family.return_value = []
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/150')
        assert b"Ez du eboluzionatzen" in response.data

    # --- DESAGRUPADOS 3-4 ---
    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_info_id_3(self, MockModel, client):
        """[INFORMAZIOA ERAKUTSI - ID 3] Itzuli (iragazkiekin)."""
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 6, 'Izena': 'Charizard', 'Irudia': 'img'}
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/6', query_string={'type': 'Fire'})
        assert response.status_code == 200
        assert b'type=Fire' in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_info_id_4(self, MockModel, client):
        """[INFORMAZIOA ERAKUTSI - ID 4] Itzuli (normal)."""
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 6, 'Izena': 'Charizard', 'Irudia': 'img'}
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/pokedex/details/6')
        assert response.status_code == 200
        # Verificar que el botón existe sin parámetros extra
        assert b'Itzuli' in response.data