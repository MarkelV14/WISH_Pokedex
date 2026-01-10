import pytest
from unittest.mock import patch, MagicMock
from app import create_app

class TestPokedexSearch:
    """
    Suite de pruebas para:
    1. POKEMON LISTAREN MENU NAGUSIA (Lista Principal)
    2. BILATU POKEMON (Buscador)
    3. INFORMAZIOA ERAKUTSI (Detalles)
    """

    @pytest.fixture
    def client(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'test_secret'
        with app.test_client() as client:
            yield client

    # ==========================================================================
    # TABLA 1: POKEMON LISTAREN MENU NAGUSIA
    # ==========================================================================

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_list_id_1(self, MockModel, client):
        """
        [LISTA - ID 1] Pokemon lista kargatzea.
        Esperotakoa: Pokemon guztiak (harrapatuak eta falta direnak) agertzea.
        """
        mock = MockModel.return_value
        # Simulamos que tenemos 1 capturado y 1 faltante
        mock.get_captured_list.return_value = [{'PokemonID': 1, 'Izena': 'Bulbasaur', 'Irudia': 'img.png'}]
        mock.get_missing_list.return_value = [{'PokemonID': 4, 'Izena': 'Charmander', 'Irudia': 'img.png'}]

        with client.session_transaction() as sess: sess['user_id'] = 1
        
        response = client.get('/pokedex')
        
        assert response.status_code == 200
        assert b"Bulbasaur" in response.data # Está en capturados
        assert b"Charmander" in response.data # Está en faltantes
        # Verificamos que se llamaron a los métodos del modelo
        mock.get_captured_list.assert_called_with(1)
        mock.get_missing_list.assert_called_with(1)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_list_id_2(self, MockModel, client):
        """
        [LISTA - ID 2] Pokemon lista sistema kargatuta ez egotea (hutik).
        Esperotakoa: Lista hutsik.
        """
        mock = MockModel.return_value
        mock.get_captured_list.return_value = []
        mock.get_missing_list.return_value = []

        with client.session_transaction() as sess: sess['user_id'] = 1
        
        response = client.get('/pokedex')
        
        assert response.status_code == 200
        assert b"Oraindik ez duzu" in response.data # Mensaje de lista vacía en tu HTML

    # ==========================================================================
    # TABLA 2: BILATU POKEMON
    # ==========================================================================

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_1(self, MockModel, client):
        """
        [BILATU - ID 1] Pokemon baten motaren arabera bilatu.
        Esperotakoa: Mota zehatz bateko pokemonak bistaratu.
        """
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [{'PokemonID': 4, 'Izena': 'Charmander', 'Altuera': 0.6, 'Pisua': 8.5, 'Irudia': 'img'}]
        mock.get_all_types.return_value = [{'Izena': 'Fire'}, {'Izena': 'Water'}]
        mock.get_all_generations.return_value = [{'Zenbakia': 1}]

        with client.session_transaction() as sess: sess['user_id'] = 1
        
        # Simulamos GET con query param type=Fire
        client.get('/pokedex/search', query_string={'type': 'Fire'})
        
        # CAJA BLANCA: Verificamos que al modelo le llegó el filtro 'Fire'
        # search_pokemon(name, type, gen, evo)
        mock.search_pokemon.assert_called_with('', 'Fire', None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_2(self, MockModel, client):
        """
        [BILATU - ID 2] Pokemon baten generazioaren arabera bilatu.
        Esperotakoa: Generazio zehatz batekoak bistaratu.
        """
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        client.get('/pokedex/search', query_string={'gen': '1'})
        
        # Verificamos tercer argumento (Gen)
        mock.search_pokemon.assert_called_with('', None, '1', None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_3(self, MockModel, client):
        """
        [BILATU - ID 3] Pokemon baten izen osoaren arabera bilatu.
        """
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [{'PokemonID': 25, 'Izena': 'Pikachu', 'Altuera':0.4, 'Pisua':6.0, 'Irudia':'img'}]
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        response = client.get('/pokedex/search', query_string={'name': 'Pikachu'})
        
        assert b"Pikachu" in response.data
        mock.search_pokemon.assert_called_with('Pikachu', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_4(self, MockModel, client):
        """
        [BILATU - ID 4] Pokemon baten eboluzioaren arabera bilatu (Bai/Ez).
        """
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        client.get('/pokedex/search', query_string={'evo': 'Bai'})
        
        # Verificamos cuarto argumento (Evo)
        mock.search_pokemon.assert_called_with('', None, None, 'Bai')

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_5(self, MockModel, client):
        """
        [BILATU - ID 5] Iragazirik aplikatu barik bilatu (Guztiak).
        Esperotakoa: Pokemon lista osoa (filtros None).
        """
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        client.get('/pokedex/search') # Sin params
        
        mock.search_pokemon.assert_called_with('', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_6(self, MockModel, client):
        """
        [BILATU - ID 6] Pokemon bat agertzen ez den izen batekin bilatu.
        Esperotakoa: Lista hutsik.
        """
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [] # Retorna vacío
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        response = client.get('/pokedex/search', query_string={'name': 'InventoMon'})
        
        assert b"Ez da emaitzarik aurkitu" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_7(self, MockModel, client):
        """
        [BILATU - ID 7] Amankomunean ez dauden iragazkien artean bilatu (Mota: Altzairua, Gen: 1).
        Esperotakoa: Lista hutsik (o casi, según la DB).
        """
        mock = MockModel.return_value
        mock.search_pokemon.return_value = [] # Suponemos que no hay resultados
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        client.get('/pokedex/search', query_string={'type': 'Steel', 'gen': '1'})
        
        mock.search_pokemon.assert_called_with('', 'Steel', '1', None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_8(self, MockModel, client):
        """
        [BILATU - ID 8] Izenaren zati batekin bilatu (Adib: 'Pik').
        """
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        client.get('/pokedex/search', query_string={'name': 'Pik'})
        
        # El controlador pasa 'Pik' tal cual, el modelo hace el LIKE %Pik%
        mock.search_pokemon.assert_called_with('Pik', None, None, None)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_search_id_9(self, MockModel, client):
        """
        [BILATU - ID 9] Hainbat iragazki konbinatu.
        """
        mock = MockModel.return_value
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        # Combinación: Fire + Gen 1 + Evo Bai
        client.get('/pokedex/search', query_string={'type': 'Fire', 'gen': '1', 'evo': 'Bai'})
        
        mock.search_pokemon.assert_called_with('', 'Fire', '1', 'Bai')

    # ==========================================================================
    # TABLA 3: INFORMAZIOA ERAKUTSI
    # ==========================================================================

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_info_id_1(self, MockModel, client):
        """
        [INFO - ID 1] Pokemon baten informazioa ikusi.
        Esperotakoa: Leihoa agertzea infoarekin.
        """
        mock = MockModel.return_value
        # Mockeamos todos los datos que pide el controller
        mock.get_pokemon_by_id.return_value = {'PokemonID': 6, 'Izena': 'Charizard', 'Altuera': 1.7, 'Pisua': 90.5, 'Irudia': 'img'}
        mock.get_pokemon_types.return_value = ['Fire', 'Flying']
        mock.get_weaknesses.return_value = ['Water', 'Rock']
        mock.get_strengths.return_value = ['Grass']
        mock.get_evolution_family.return_value = ['Charmander', 'Charmeleon', 'Charizard']

        with client.session_transaction() as sess: sess['user_id'] = 1
        
        response = client.get('/pokedex/details/6')
        
        assert response.status_code == 200
        assert b"Charizard" in response.data
        assert b"Fire" in response.data
        # Verificamos que se llamó al ID correcto
        mock.get_pokemon_by_id.assert_called_with(6)

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_info_id_2(self, MockModel, client):
        """
        [INFO - ID 2] Ebolurik gabeko Pokemon baten informazioa.
        Esperotakoa: Eboluzio atala hutsik edo "Ez du eboluzionatzen".
        """
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 150, 'Izena': 'Mewtwo', 'Altuera': 2.0, 'Pisua': 122, 'Irudia': 'img'}
        mock.get_evolution_family.return_value = [] # Sin evolución
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        response = client.get('/pokedex/details/150')
        
        assert b"Ez du eboluzionatzen" in response.data

    @patch('app.controllers.pokedex_controller.PokedexModel')
    def test_info_id_3_and_4(self, MockModel, client):
        """
        [INFO - ID 3 y 4] Informazio leihotik itzuli (iragazkiak mantenduz).
        Esperotakoa: El botón de volver debe contener los parámetros de búsqueda anteriores.
        """
        mock = MockModel.return_value
        mock.get_pokemon_by_id.return_value = {'PokemonID': 6, 'Izena': 'Charizard', 'Irudia': 'img'}
        
        with client.session_transaction() as sess: sess['user_id'] = 1
        
        # Simulamos que venimos de una búsqueda filtrada: Type=Fire
        response = client.get('/pokedex/details/6', query_string={'type': 'Fire', 'gen': '1'})
        
        assert response.status_code == 200
        # Validamos que en el HTML existe un enlace que vuelve al buscador CON los filtros
        # Flask url_for genera los ampersands como &amp; en HTML
        assert b'type=Fire' in response.data
        assert b'gen=1' in response.data
        # Esto confirma que al pulsar "Itzuli", volverá a la búsqueda filtrada.