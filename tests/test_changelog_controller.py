import pytest
from unittest.mock import patch
from app import create_app

class TestChangelogMenu:
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'test_secret'
        with app.test_client() as client:
            yield client

    # ==========================================
    # TABLA 1: FILTRATU (Pruebas de Filtrado)
    # ==========================================

    @patch('app.controllers.notifications_controller.MessageModel')
    def test_filtratu_ui_elements(self, MockModel, client):
        """[FILTRATU - ID 1 & 2] Interfazearen elementuak (UI check)."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: 
            sess['user_id'] = 1
            sess['username'] = 'admin'
            
        response = client.get('/notifications/filter')
        assert response.status_code == 200
        assert b'user-checkbox' in response.data 

    @patch('app.controllers.notifications_controller.MessageModel')
    def test_filtratu_id_3(self, MockModel, client):
        """[FILTRATU - ID 3] Eguneratu (Guztiak aukeratuta)."""
        mock = MockModel.return_value
        # CORRECCION: Usamos get_all_messages porque el controlador llama a este metodo
        # cuando el filtro es 'all'.
        mock.get_all_messages.return_value = [{'Mezua': 'Update 1', 'Data': '2023', 'username': 'User1'}]
        
        with client.session_transaction() as sess: 
            sess['user_id'] = 1
            sess['username'] = 'admin'

        response = client.post('/notifications/filter', data={'filter_users': 'all'}, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Update 1' in response.data
        assert b'Jakinarazpenak' in response.data or b'Changelog' in response.data

    @patch('app.controllers.notifications_controller.MessageModel')
    def test_filtratu_id_4(self, MockModel, client):
        """[FILTRATU - ID 4] Eguneratu (Bat ere ez aukeratuta)."""
        mock = MockModel.return_value
        mock.get_messages_by_users.return_value = []
        
        with client.session_transaction() as sess: 
            sess['user_id'] = 1
            sess['username'] = 'admin'

        response = client.post('/notifications/filter', data={'filter_users': []}, follow_redirects=True)
        
        assert response.status_code == 200
        # No deberían aparecer mensajes
        assert b'Update 1' not in response.data

    @patch('app.controllers.notifications_controller.MessageModel')
    def test_filtratu_id_5(self, MockModel, client):
        """[FILTRATU - ID 5] Eguneratu (Batzuk aukeratuta)."""
        mock = MockModel.return_value
        mock.get_messages_by_users.return_value = [{'Mezua': 'User 2 Update', 'Data': '2023', 'username': 'User2'}]
        
        with client.session_transaction() as sess: 
            sess['user_id'] = 1
            sess['username'] = 'admin'

        response = client.post('/notifications/filter', data={'user_ids': [2, 3]}, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'User 2 Update' in response.data

    @patch('app.controllers.notifications_controller.MessageModel')
    def test_filtratu_id_6_7_8(self, MockModel, client):
        """[FILTRATU - ID 6, 7, 8] Itzuli (Aldaketarik gabe)."""
        mock = MockModel.return_value
        with client.session_transaction() as sess: 
            sess['user_id'] = 1