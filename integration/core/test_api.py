import pytest
import cattle
import requests
from wait_for import wait_for


@pytest.fixture
def client():
    url = 'http://localhost:8088/v1-catalog/schemas'
    catalogs = cattle.from_env(url=url).list_catalog()
    wait_for(
        lambda: len(catalogs) > 0
    )
    return cattle.from_env(url=url)


def test_catalog_list(client):
    catalogs = client.list_catalog()
    assert len(catalogs) > 0


def test_template_list(client):
    templates = client.list_template()
    assert len(templates) > 0


def test_template_basics(client):
    url = 'http://localhost:8088/v1-catalog/templates/library:k8s:0'
    response = requests.get(url)
    assert response.status_code == 200
    resp = response.json()
    assert resp['template'] == 'k8s'


def test_template_bindings(client):
    url = 'http://localhost:8088/v1-catalog/templates/library:k8s:0'
    response = requests.get(url)
    assert response.status_code == 200
    resp = response.json()
    bindings = resp['bindings']
    assert bindings is not None


def test_v2_syntax(client):
    for revision in [0, 1, 2, 3]:
        url = 'http://localhost:8088/v1-catalog/templates/library:v2:' + \
                str(revision)
        response = requests.get(url)
        assert response.status_code == 200
        resp = response.json()
        assert resp['description'] is not None
