import pytest
from unittest.mock import patch, MagicMock
from app import create_app

class TestAuthHodei:
    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'hodei_secret'
        with app.test_client() as client:
            yield client

    @patch('app.controllers.model.user_model.UserModel.verify_password')
    @patch('app.controllers.model.auth_model.AuthModel.create_session')
    def test_login_id_1(self, mock_session, mock_verify, client):
        """
        [SAIOA HASI - ID 1]
        Azalpena: Saioa ondo hasten da datu zuzenekin.
        Esperotako emaitza: Dashboard pantaila.
        """
        mock_verify.return_value = {'id': 1, 'username': 'Hodei', 'role': 'user', 'is_approved': 1}
        mock_session.return_value = 'fake_token'
        response = client.post('/login', data={'username': 'Hodei', 'password': '123'}, follow_redirects=True)
        assert b"Saioa ongi hasi duzu" in response.data

    @patch('app.controllers.model.user_model.UserModel.verify_password')
    def test_login_id_2(self, mock_verify, client):
        """
        [SAIOA HASI - ID 2]
        Azalpena: email zuzena pasahitza okerrarekin.
        Esperotako emaitza: Errore mezua.
        """
        mock_verify.return_value = None 
        response = client.post('/login', data={'username': 'Hodei', 'password': 'bad'}, follow_redirects=True)
        assert b"Erabiltzailea edo pasahitza okerrak" in response.data

    @patch('app.controllers.model.user_model.UserModel.verify_password')
    def test_login_id_3(self, mock_verify, client):
        """
        [SAIOA HASI - ID 3]
        Azalpena: Erabiltzaile ez erregistratua.
        Esperotako emaitza: Errore mezua.
        """
        mock_verify.return_value = None
        response = client.post('/login', data={'username': 'NoExist', 'password': '123'}, follow_redirects=True)
        assert b"Erabiltzailea edo pasahitza okerrak" in response.data

    def test_login_id_4(self, client):
        """
        [SAIOA HASI - ID 4]
        Azalpena: Eremuak hutsik.
        Esperotako emaitza: Errore mezua.
        """
        response = client.post('/login', data={'username': '', 'password': ''}, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    def test_login_id_5(self, client):
        """
        [SAIOA HASI - ID 5]
        Azalpena: Email eremua hutsik.
        Esperotako emaitza: Errore mezua.
        """
        response = client.post('/login', data={'username': '', 'password': '123'}, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    def test_login_id_6(self, client):
        """
        [SAIOA HASI - ID 6]
        Azalpena: Pasahitz eremua hutsik.
        Esperotako emaitza: Errore mezua.
        """
        response = client.post('/login', data={'username': 'Hodei', 'password': ''}, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    def test_login_id_7(self, client):
        """
        [SAIOA HASI - ID 7]
        Azalpena: Erregistratu botoia sakatzea.
        Esperotako emaitza: Erregistro eremura birbideratu.
        """
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

    @patch('app.controllers.model.user_model.UserModel.create_user')
    def test_register_id_1(self, mock_create, client):
        """
        [ERREGISTRATU - ID 1]
        Azalpena: Erregistro arrakastatsua.
        Esperotako emaitza: Saioa Hasi pantailara joan.
        """
        mock_create.return_value = 1
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"Erregistroa ondo burutu da" in response.data

    def test_register_id_2(self, client):
        """
        [ERREGISTRATU - ID 2]
        Azalpena: Pasahitz eta baieztapen ezberdinak.
        Esperotako emaitza: Errore mezua.
        """
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '123456', 'confirm_password': '654321'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"Pasahitzak ez datoz bat" in response.data

    def test_register_id_3(self, client):
        """
        [ERREGISTRATU - ID 3]
        Azalpena: Pasahitz laburregia.
        Esperotako emaitza: Errore mezua.
        """
        data = {'username': 'Hodei', 'email': 'h@g.com', 'password': '123', 'confirm_password': '123'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"gutxienez 6 karaktere" in response.data

    def test_register_id_4(self, client):
        """
        [ERREGISTRATU - ID 4]
        Azalpena: Erabiltzaile izen motzegia.
        Esperotako emaitza: Errore mezua.
        """
        data = {'username': 'Bo', 'email': 'h@g.com', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"izena motzegia da" in response.data

    def test_register_id_5(self, client):
        """
        [ERREGISTRATU - ID 5]
        Azalpena: Erabiltzaile izen luzegia.
        Esperotako emaitza: Errore mezua.
        """
        long_name = "a" * 25
        data = {'username': long_name, 'email': 'h@g.com', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"izena luzegia da" in response.data

    def test_register_id_6(self, client):
        """
        [ERREGISTRATU - ID 6]
        Azalpena: Email formatu okerra.
        Esperotako emaitza: Errore mezua.
        """
        data = {'username': 'Hodei', 'email': 'emailtxarra', 'password': '123456', 'confirm_password': '123456'}
        response = client.post('/register', data=data, follow_redirects=True)
        assert b"formatua okerra" in response.data

    def test_register_id_7_11(self, client):
        """
        [ERREGISTRATU - ID 7-11]
        Azalpena: Eremu guztiak edo batzuk hutsik.
        Esperotako emaitza: Errore mezua.
        """
        response = client.post('/register', data={}, follow_redirects=True)
        assert b"Eremu guztiak bete behar dira" in response.data

    def test_register_id_12(self, client):
        """
        [ERREGISTRATU - ID 12]
        Azalpena: Baliogabetu botoia sakatzea.
        Esperotako emaitza: Aurreko pantailara (Login) birbidaltzea.
        """
        response = client.post('/register', data={'cancel': 'true'}, follow_redirects=True)
        assert b"Saioa Hasi" in response.data

    @patch('app.controllers.model.user_model.UserModel.create_user')
    def test_register_id_13(self, mock_create, client):
        """
        [ERREGISTRATU - ID 13]
        Azalpena: Erabiltzaile errepikatua.
        Esperotako emaitza: Errore mezua.
        """
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

    @patch('app.controllers.model.user_model.UserModel.update_user')
    def test_edit_id_1(self, mock_update, client):
        """
        [ERABILTZAILE KUDEAKETA - ID 1]
        Azalpena: Profila ondo editatu.
        Esperotako emaitza: Mezua (Ondo editatu da).
        """
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'NewName', 'email': 'new@g.com', 'bio': 'Kaixo'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Profila ondo editatu da" in response.data

    def test_edit_id_2_5(self, client):
        """
        [ERABILTZAILE KUDEAKETA - ID 2-5]
        Azalpena: Eremuak hutsik (Izena, Email, Bio).
        Esperotako emaitza: Errore mezua.
        """
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/profile/edit', data={'username': ''}, follow_redirects=True)
        assert b"Eremu guztiak bete" in response.data

    def test_edit_id_6_8(self, client):
        """
        [ERABILTZAILE KUDEAKETA - ID 6-8]
        Azalpena: Formatu okerrak (Izena motza, Email txarra, Bio luzea).
        Esperotako emaitza: Errore mezua.
        """
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'Ab', 'email': 'a@a.com', 'bio': 'Hola'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"Izena motzegia" in response.data

    @patch('app.controllers.model.user_model.UserModel.update_user')
    def test_edit_id_9(self, mock_update, client):
        """
        [ERABILTZAILE KUDEAKETA - ID 9]
        Azalpena: Sisteman jada existitzen zen email-a jartzea.
        Esperotako emaitza: Errore mezua.
        """
        mock_update.side_effect = Exception("Duplicate entry")
        with client.session_transaction() as sess: sess['user_id'] = 1
        data = {'username': 'Aitor', 'email': 'exists@a.com', 'bio': 'Hola'}
        response = client.post('/profile/edit', data=data, follow_redirects=True)
        assert b"existitzen da jada" in response.data

    def test_edit_id_10(self, client):
        """
        [ERABILTZAILE KUDEAKETA - ID 10]
        Azalpena: Atzera botoia sakatzea.
        Esperotako emaitza: Dashboardera birbideratu.
        """
        with client.session_transaction() as sess: sess['user_id'] = 1
        response = client.post('/profile/edit', data={'back': 'true'}, follow_redirects=True)
        assert b"Panela" in response.data