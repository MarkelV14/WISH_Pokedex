import pytest
from unittest.mock import patch, MagicMock
from app import create_app

class TestTeamTables:
    """
    CLASE 1: Pruebas para SORTU TALDEA y EDITATU TALDEA.
    """

    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'test_secret'
        with app.test_client() as client:
            yield client

    # --- SORTU TALDEA ---

    @patch('app.controllers.team_controller.TeamModel')
    @patch('app.controllers.team_controller.MessageModel')
    def test_sortu_taldea_id_1(self, MockMessage, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = []
        mock.get_pokemon_by_name.return_value = {'PokemonID': 25, 'Izena': 'Pikachu'}
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'pokemon_name': 'Pikachu'}, follow_redirects=True)
        
        mock.add_pokemon_to_team.assert_called_with(1, 25, 'Pikachu')
        assert b"Pikachu gehituta!" in response.data

    @patch('app.controllers.team_controller.TeamModel')
    def test_sortu_taldea_id_2(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = []
        mock.get_pokemon_by_name.return_value = None
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'pokemon_name': 'Digimon'}, follow_redirects=True)
        
        mock.add_pokemon_to_team.assert_not_called()
        assert b"Ez da aurkitu" in response.data

    def test_sortu_taldea_id_3(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'finish_team': 'true'})
        assert response.status_code == 302
        assert '/dashboard' in response.location

    @patch('app.controllers.team_controller.TeamModel')
    def test_sortu_taldea_id_4(self, MockTeam, client):
        mock = MockTeam.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/dashboard')
        mock.add_pokemon_to_team.assert_not_called()

    # --- EDITATU TALDEA ---

    @patch('app.controllers.team_controller.TeamModel')
    @patch('app.controllers.team_controller.MessageModel')
    def test_editatu_taldea_id_1(self, MockMessage, MockTeam, client):
        mock = MockTeam.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/team/delete/5', follow_redirects=True)
        mock.delete_pokemon_from_team.assert_called_with(1, 5)
        assert b"taldetik ezabatu da" in response.data

    @patch('app.controllers.team_controller.TeamModel')
    @patch('app.controllers.team_controller.MessageModel')
    def test_editatu_taldea_id_2(self, MockMessage, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [{'Izena': 'Charmander'}]
        mock.get_pokemon_by_name.return_value = {'PokemonID': 7, 'Izena': 'Squirtle'}
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        client.post('/team/create', data={'pokemon_name': 'Squirtle'})
        mock.add_pokemon_to_team.assert_called_with(1, 7, 'Squirtle')

    @patch('app.controllers.team_controller.TeamModel')
    def test_editatu_taldea_id_3(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [{'Izena': 'Pikachu'}]
        mock.get_pokemon_by_name.return_value = {'PokemonID': 25, 'Izena': 'Pikachu'}
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'pokemon_name': 'Pikachu'}, follow_redirects=True)
        
        mock.add_pokemon_to_team.assert_not_called()
        assert b"jadanik zure taldean dago" in response.data

    @patch('app.controllers.team_controller.TeamModel')
    def test_editatu_taldea_id_4(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = []
        mock.get_pokemon_by_name.return_value = None
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'pokemon_name': 'MewThree'}, follow_redirects=True)
        mock.add_pokemon_to_team.assert_not_called()
        assert b"Ez da aurkitu" in response.data


class TestTeamManagementMarkel:
    """
    CLASE 2: Pruebas para la tabla 'Pokemon talde kudeaketa (Markel)'.
    CORREGIDA: Usa diccionarios para evitar el error de 'int is not subscriptable'.
    """

    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'markel_secret'
        with app.test_client() as client:
            yield client

    # CASO 1: Equipo lleno (Simulamos lista de 6 elementos simples porque aquí solo cuenta la longitud)
    @patch('app.controllers.team_controller.TeamModel')
    def test_markel_id_1(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [1, 2, 3, 4, 5, 6] 
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'pokemon_name': 'New'}, follow_redirects=True)
        assert b"Taldea beteta dago" in response.data

    # CASO 2: Corrección del texto esperado
    @patch('app.controllers.team_controller.TeamModel')
    def test_markel_id_2(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [] 
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/team/create')
        assert response.status_code == 200
        # CAMBIO: Buscamos "Taldea Sortu" que aparece en el <title> y no da problemas de tildes
        assert b"Taldea Sortu" in response.data

    # CASO 3
    @patch('app.controllers.team_controller.TeamModel')
    def test_markel_id_3(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [] 
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/team/manage')
        assert b"taldea hutsik dago" in response.data

    # CASO 4
    @patch('app.controllers.team_controller.TeamModel')
    def test_markel_id_4(self, MockTeam, client):
        mock = MockTeam.return_value
        # Aquí sí usamos diccionario por si acaso se renderiza el nombre
        mock.get_user_team.return_value = [{'Izena': 'Pikachu', 'id': 1}] 
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/team/manage')
        assert response.status_code == 200
        assert b"Pikachu" in response.data

    # CASO 5
    @patch('app.controllers.team_controller.TeamModel')
    def test_markel_id_5(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [] 
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'finish_team': 'true'}, follow_redirects=True)
        assert b"izan behar ditu gordetzeko" in response.data

    # CASO 6
    @patch('app.controllers.team_controller.TeamModel')
    def test_markel_id_6(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [1, 2, 3, 4, 5, 6]
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'finish_team': 'true'}, follow_redirects=True)
        assert b"Aldaketak gordeta" in response.data

    # CASO 7
    @patch('app.controllers.team_controller.TeamModel')
    def test_markel_id_7(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [1, 2, 3, 4, 5] # 5 elementos
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'finish_team': 'true'}, follow_redirects=True)
        assert b"izan behar ditu gordetzeko" in response.data

    # CASO 8
    @patch('app.controllers.team_controller.TeamModel')
    def test_markel_id_8(self, MockTeam, client):
        mock = MockTeam.return_value
        mock.get_user_team.return_value = [1, 2, 3, 4, 5, 6]
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/team/create', data={'finish_team': 'true'}, follow_redirects=True)
        assert response.status_code == 200

    # CASO 9: CORREGIDO EL TYPE ERROR
    @patch('app.controllers.team_controller.TeamModel')
    @patch('app.controllers.team_controller.MessageModel')
    def test_markel_id_9(self, MockMessage, MockTeam, client):
        mock = MockTeam.return_value
        
        # CAMBIO IMPORTANTE: Usamos diccionarios [{'Izena': 'X'}] en lugar de números [1].
        # Esto permite que tu código haga `member['Izena']` sin fallar.
        mock.get_user_team.side_effect = [
            [{'Izena': 'Poke1'}, {'Izena': 'Poke2'}, {'Izena': 'Poke3'}, {'Izena': 'Poke4'}, {'Izena': 'Poke5'}], # Carga inicial (5)
            [{'Izena': 'Poke1'}, {'Izena': 'Poke2'}, {'Izena': 'Poke3'}, {'Izena': 'Poke4'}, {'Izena': 'Poke5'}, {'Izena': 'Mew'}] # Al guardar (6)
        ]
        mock.get_pokemon_by_name.return_value = {'PokemonID': 99, 'Izena': 'Mew'}
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        # 1. Añadimos el Pokemon (aquí es donde fallaba antes)
        client.post('/team/create', data={'pokemon_name': 'Mew'})
        
        # 2. Guardamos
        response = client.post('/team/create', data={'finish_team': 'true'}, follow_redirects=True)
        
        assert b"Aldaketak gordeta" in response.data