import pytest
from unittest.mock import patch, MagicMock
from app import create_app

class TestAuth:
    
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'hodei_secret'
        with app.test_client() as client:
            yield client

    # ==========================================================
    # TABLA 1: SAIOA HASI (LOGIN) - 7 CASOS
    # ==========================================================
    
    # CASO 1: Saioa ondo hasten da datu zuzenekin -> 3c (Dashboard)
    @patch('app.controllers.model.user_model.UserModel.verify_password')
    @patch('app.controllers.model.auth_model.AuthModel.create_session')
    def test_login_id_1(self, mock_session, mock_verify, client):
        mock_verify.return_value = {'id': 1, 'username': 'Hodei', 'role': 'user', 'is_approved': 1}
        mock_session.return_value = 'fake_token'
        
        response = client.post('/login', data={'username': 'Hodei', 'password': '123'}, follow_redirects=True)
        assert b"Saioa ongi hasi duzu" in response.data
        assert b"Panela" in response.data # Confirma dashboard

    # CASO 2: Email zuzena pasahitza okerrarekin -> 3b (Error)
    @patch('app.controllers.model.user_model.UserModel.verify_password')
    def test_login_id_2(self, mock_verify, client):
        mock_verify.return_value = None # Fallo auth
        response = client.post('/login', data={'username': 'Hodei', 'password': 'bad'}, follow_redirects=True)
        assert b"Erabiltzailea edo pasahitza okerrak" in response.data

    # CASO 3: Erabiltzaile ez erregistratua -> 3b (Error)
    @patch('app.controllers.model.user_model.UserModel.verify_password')
    def test_login_id_3(self, mock_verify, client):
        mock_verify.return_value = None
        response = client.post('/login', data={'username': 'NoExist', 'password': '123'}, follow_redirects=True)
        assert b"Erabiltzailea edo pasahitza okerrak" in response.data

    # CASO 4: Eremuak hutsik -> 3b (Error)
    def test_login_id_4(self, client):
        response = client.post('/login', data={'username': '', 'password': ''}, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    # CASO 5: Email eremua hutsik -> 3b
    def test_login_id_5(self, client):
        response = client.post('/login', data={'username': '', 'password': '123'}, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    # CASO 6: Pasahitz eremua hutsik -> 3b
    def test_login_id_6(self, client):
        response = client.post('/login', data={'username': 'Hodei', 'password': ''}, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    # CASO 7: Erregistratu botoia sakatzea -> Redirigir register
    def test_login_id_7(self, client):
        # Simulamos que el botón de registro envía el usuario a /register
        response = client.get('/register') 
        assert response.status_code == 200
        assert b"Erregistratu" in response.data


class TestRegisterHodei:
    
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'hodei_secret'
        with app.test_client() as client:
            yield client

    # ==========================================================
    # TABLA 2: ERREGISTRATU - 13 CASOS
    # ==========================================================

    # CASO 1: Erregistro arrakastatsua -> 3a
    @patch('app.controllers.model.user_model.UserModel.create_user')
    def test_register_id_1(self, mock_create, client):
        mock_create.return_value = 1
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"Erregistroa ondo burutu da" in response.data

    # CASO 2: Pasahitz eta baieztapen ezberdinak
    def test_register_id_2(self, client):
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '123456', 'confirm_password': '654321'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"Pasahitzak ez datoz bat" in response.data

    # CASO 3: Pasahitz laburregia
    def test_register_id_3(self, client):
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '123', 'confirm_password': '123'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"gutxienez 6 karaktere" in response.data

    # CASO 4: Izen motzegia
    def test_register_id_4(self, client):
        data = {'username': 'Bo', 'email': 'h@g.com', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"izena motzegia da" in response.data

    # CASO 5: Izen luzegia
    def test_register_id_5(self, client):
        long_name = "a" * 25
        data = {'username': long_name, 'email': 'h@g.com', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"izena luzegia da" in response.data

    # CASO 6: Email formatu okerra
    def test_register_id_6(self, client):
        data = {'username': 'Hodei', 'email': 'emailtxarra', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"formatua okerra" in response.data

    # CASO 7: Eremu guztiak hutsik
    def test_register_id_7(self, client):
        response = client.post('/register', data={}, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    # CASO 8: Id hutsik (En web el ID es autogenerado, probamos username vacio como proxy)
    def test_register_id_8(self, client):
        data = {'username': '', 'email': 'h@g.com', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    # CASO 9: Email hutsik
    def test_register_id_9(self, client):
        data = {'username': 'Hodei', 'email': '', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    # CASO 10: Pasahitza hutsik
    def test_register_id_10(self, client):
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    # CASO 11: Baieztapena hutsik
    def test_register_id_11(self, client):
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '123456', 'confirm_password': ''}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    # CASO 12: Baliogabetu botoia (Simulamos botón con name='cancel')
    def test_register_id_12(self, client):
        response = client.post('/register', data={'cancel': 'true'}, follow_redirects=True)
        assert b"Saioa Hasi" in response.data

    # CASO 13: Erabiltzaile errepikatua
    @patch('app.controllers.model.user_model.UserModel.create_user')
    def test_register_id_13(self, mock_create, client):
        # Simulamos que el modelo lanza error de valor (duplicate)
        mock_create.side_effect = ValueError("Erabiltzaile izena dagoeneko existitzen da")
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"dagoeneko existitzen da" in response.data


class TestProfileEditHodei:
    
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'hodei_secret'
        with app.test_client() as client:
            yield client

    # ==========================================================
    # TABLA 3: ERABILTZAILE KUDEAKETA (EDIT) - 10 CASOS
    # ==========================================================

    # CASO 1: Profila ondo editatu
    @patch('app.controllers.model.user_model.UserModel.update_user')
    def test_edit_id_1(self, mock_update, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'NewName', 'email': 'new@g.com', 'bio': 'Kaixo'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Profila ondo editatu da" in response.data

    # CASO 2: Dena hutsik
    def test_edit_id_2(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/profile/edit', data={}, follow_redirects=True)
        assert b"Eremu guztiak bete" in response.data

    # CASO 3: Izena hutsik
    def test_edit_id_3(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': '', 'email': 'a@a.com', 'bio': 'a'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Eremu guztiak bete" in response.data

    # CASO 4: Email hutsik
    def test_edit_id_4(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'A', 'email': '', 'bio': 'a'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Eremu guztiak bete" in response.data

    # CASO 5: Bio hutsik
    def test_edit_id_5(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'A', 'email': 'a@a.com', 'bio': ''}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Eremu guztiak bete" in response.data

    # CASO 6: Izena formatu okerra (Motzegia)
    def test_edit_id_6(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'Ab', 'email': 'a@a.com', 'bio': 'Hola'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Izena motzegia" in response.data

    # CASO 7: Email formatu okerra
    def test_edit_id_7(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'Aitor', 'email': 'bademali', 'bio': 'Hola'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Email formatua okerra" in response.data

    # CASO 8: Bio formatu okerra (Luzegia)
    def test_edit_id_8(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        long_bio = "a" * 101
        data = {'username': 'Aitor', 'email': 'a@a.com', 'bio': long_bio}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Biografia luzegia" in response.data

    # CASO 9: Sisteman jada existitzen den emaila
    @patch('app.controllers.model.user_model.UserModel.update_user')
    def test_edit_id_9(self, mock_update, client):
        mock_update.side_effect = Exception("Duplicate entry")
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'Aitor', 'email': 'exists@a.com', 'bio': 'Hola'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"existitzen da jada" in response.data

    # CASO 10: Atzera botoia
    def test_edit_id_10(self, client):
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/profile/edit', data={'back': 'true'}, follow_redirects=True)
        assert b"Panela" in response.data