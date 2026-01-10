import pytest

@pytest.fixture(autouse=True)
def print_test_description(request):
    """
    Fixture automatikoa: Test bakoitzaren 'Docstring'-a (azalpena)
    hartzen du eta kontsolan inprimatzen du.
    Horrela, pytest-html txostenean 'Captured stdout' atalean agertuko da.
    """
    # Testaren izena eta dokumentazioa lortu
    test_name = request.node.name
    test_doc = request.function.__doc__

    if test_doc:
        # Formateatu eta inprimatu
        print(f"\n{'='*60}")
        print(f"TESTA: {test_name}")
        print(f"{'-'*60}")
        print("AZALPENA (DESCRIPCIÓN DEL CASO):")
        print(test_doc.strip()) # Espazio zuriak garbitu
        print(f"{'='*60}\n")
    else:
        print(f"\nTest honek ez dauka deskribapenik: {test_name}")