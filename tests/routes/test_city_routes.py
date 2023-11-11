import json
from datetime import datetime, timedelta


def test_fetch_cities(client, mocker):
    mock_cities = [
        {"name": "Rio de Janeiro", "state_abbreviation": "RJ"},
        {"name": "São Paulo", "state_abbreviation": "SP"},
    ]
    mocker.patch("services.city_svc.fetch_cities", return_value=mock_cities)
    resp = client.get("/city/external-fetching")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp == mock_cities


def test_fetch_cities_and_save(client, mocker):
    created = 1
    updated = 2
    mock_fetch_and_save_cities = created, updated
    mocker.patch("services.city_svc.fetch_and_save_cities", return_value=mock_fetch_and_save_cities)
    resp = client.get("/city/external-fetching/save")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp["message"] == "Fetching and saving completed"
    assert json_resp["created"] == created
    assert json_resp["updated"] == updated


def test_list_cities(client, mocker):
    mock_cities = [
        {
            "id": 1,
            "name": "Rio de Janeiro",
            "state_abbreviation": "RJ",
            "created": datetime.utcnow(),
            "updated": None,
        },
        {
            "id": 2,
            "name": "São Paulo",
            "state_abbreviation": "SP",
            "created": datetime.utcnow() - timedelta(hours=2),
            "updated": datetime.utcnow(),
        },
    ]
    mocker.patch("services.city_svc.get_cities", return_value=mock_cities)
    resp = client.get("/city")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp[0]["name"] == mock_cities[0]["name"]
    assert json_resp[1]["name"] == mock_cities[1]["name"]


def test_get_city_by_id(client, mocker):
    city_id = 1
    mock_city = {
        "id": city_id,
        "name": "Rio de Janeiro",
        "state_abbreviation": "RJ",
        "created": datetime.utcnow().isoformat(),
        "updated": None,
    }
    mocker.patch("services.city_svc.get_city_by_id", return_value=mock_city)
    resp = client.get(f"/city/{city_id}")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp == mock_city