import pytest

# 1

def test_vazio(client):

    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []

# 2

def test_criar(client):

    response = client.post("/produtos",
        json={
            "nome": "Booster Box Escarlate e Violeta",
            "preco": 380.00,
            "estoque": 15,
            "ativo": True
        }
    )

    assert response.status_code == 201
    dados = response.json()
    assert dados["id"] > 0
    assert dados["nome"] == "Booster Box Escarlate e Violeta"

# 3

def test_listagem(client):

    client.post("/produtos",
        json={
            "nome": "Triple Pack Astúcia Fulgurante",
            "preco": 45.90,
            "estoque": 40
        }
    )

    response = client.get("/produtos")
    assert len(response.json()) == 1

# 4

def test_id(client, existe):

    response = client.get(f"/produtos/{existe['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == existe["id"]

# 5

def test_inexistente(client):

    response = client.get("/produtos/999")
    assert response.status_code == 404

# 6

def test_deletar(client, existe):

    response = client.delete(f"/produtos/{existe['id']}")
    assert response.status_code == 204

# 7

def test_deletar_confirmar(client,existe):

    client.delete(f"/produtos/{existe['id']}")
    response = client.get(f"/produtos/{existe['id']}")
    assert response.status_code == 404

# 8

def test_deletar_inexistente(client):
    response = client.delete("/produtos/999")
    assert response.status_code == 404

# 9

@pytest.mark.parametrize(
    "payload",
    [
        {
            "nome": "",
            "preco": 7.00
        },
        {
            "nome": "Deck Inicial Charizard ex",
            "preco": -120.00
        },
        {
            "nome": "Blister Unitário Pikachu"
        },
        {
            "preco": 19.90
        }
    ]
)
def test_payloads_invalidos(client, payload):

    response = client.post("/produtos",json=payload)
    assert response.status_code == 422

# 10

def test_banco_isolado(client):

    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []