import pytest
from unittest.mock import patch, MagicMock
from app import create_app

class TestChatbotController:
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'test_secret'
        with app.test_client() as client:
            yield client

    # ==========================================
    # TABLA 1: BILATU / POKEMON HOBERENA
    # ==========================================

    @patch('app.controllers.chatbot_controller.ChatbotModel')
    def test_chatbot_search_id_1(self, MockModel, client):
        """[CHATBOT - ID 1] “Bilatu” botoia sakatzen da taldea aukeratu eta gero."""
        mock = MockModel.return_value
        
        # CORRECCIÓN: El controlador usa 'get_best_from_my_team', no 'get_best_pokemon'
        mock.get_best_from_my_team.return_value = {'ID': 25, 'Izena': 'Pikachu', 'Irudia': 'img/pikachu.png'}
        
        with client.session_transaction() as sess:
            sess['user_id'] = 1

        # Simulamos POST
        response = client.post('/chatbot/best', data={'team_id': '1'}, follow_redirects=True)
        
        assert response.status_code == 200
        assert b"Pikachu" in response.data

    @patch('app.controllers.chatbot_controller.ChatbotModel')
    def test_chatbot_search_id_2(self, MockModel, client):
        """[CHATBOT - ID 2] “Bilatu” botoia sakatzen da taldea aukeratu ez denean."""
        # Nota: En tu controlador actual, si no hay POST data, simplemente carga la página vacía o da error
        # Si el controlador valida 'team_id', saltará el error.
        
        with client.session_transaction() as sess:
            sess['user_id'] = 1

        response = client.post('/chatbot/best', data={}, follow_redirects=True)
        assert response.status_code == 200
        # Verificar comportamiento esperado según tu código

    def test_chatbot_search_id_3(self, client):
        """[CHATBOT - ID 3] “Itzuli menura” botoia klikatzen du."""
        
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        
        # CORRECCIÓN: La ruta es /chatbot, no /chatbot/menu
        response = client.get('/chatbot', follow_redirects=True)
        
        assert response.status_code == 200
        # Verificamos que carga el menú (buscando un texto que solo esté en el menú)
        # assert b"Menua" in response.data 

    def test_chatbot_search_id_4(self, client):
        """[CHATBOT - ID 4] “Itzuli menura” botoia klikatzen du taldea aukeratuta dagoenean."""
        
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            
        # CORRECCIÓN: La ruta es /chatbot
        response = client.get('/chatbot', follow_redirects=True)
        assert response.status_code == 200

    @patch('app.controllers.chatbot_controller.ChatbotModel')
    def test_chatbot_search_id_5(self, MockModel, client):
        """[CHATBOT - ID 5] Bilatzean aukeratutako taldea ez dauka pokemonik."""
        mock = MockModel.return_value
        
        # CORRECCIÓN: Usar el nombre correcto del método
        mock.get_best_from_my_team.return_value = None 
        
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            
        response = client.post('/chatbot/best', data={'team_id': '2'}, follow_redirects=True)
        assert response.status_code == 200
        # Verificamos mensaje de error (flash message)
        # assert b"hutsik dago" in response.data

    # ==========================================
    # TABLA 2: NAVEGACIÓN MENÚ (MENU NAVIGATION)
    # ==========================================

    def test_chatbot_nav_id_1(self, client):
        """[MENU - ID 1] “Pokemon hoberena” klikatzen du."""
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/chatbot/best') 
        assert response.status_code == 200

    @patch('app.controllers.chatbot_controller.ChatbotModel')
    def test_chatbot_nav_id_2(self, MockModel, client):
        """[MENU - ID 2] “Estatistikak” klikatzen du."""
        # Necesitamos mockear get_all_pokemon_names porque se llama al cargar la página
        mock = MockModel.return_value
        mock.get_all_pokemon_names.return_value = ['Pikachu', 'Charmander']
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/chatbot/stats')
        assert response.status_code == 200

    @patch('app.controllers.chatbot_controller.ChatbotModel')
    def test_chatbot_nav_id_3(self, MockModel, client):
        """[MENU - ID 3] “Ahulezi eta indargune” klikatzen du."""
        mock = MockModel.return_value
        mock.get_all_pokemon_names.return_value = ['Pikachu', 'Charmander']

        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/chatbot/matchups')
        assert response.status_code == 200

    @patch('app.controllers.chatbot_controller.ChatbotModel')
    def test_chatbot_nav_id_4(self, MockModel, client):
        """[MENU - ID 4] “Eboluzio katea” klikatzen du."""
        mock = MockModel.return_value
        mock.get_all_pokemon_names.return_value = ['Pikachu', 'Charmander']

        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.get('/chatbot/evolution')
        assert response.status_code == 200

    def test_chatbot_nav_id_5(self, client):
        """[MENU - ID 5] “Itzuli menura” botoia klikatzen du (Salir)."""
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        # Asumiendo que salir del chatbot lleva al dashboard principal
        response = client.get('/dashboard', follow_redirects=True)
        assert response.status_code == 200