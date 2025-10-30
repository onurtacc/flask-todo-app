from domain_contracts import normalize_title

def test_contract_smoke():
    assert normalize_title("  Hello  ") == "Hello"
