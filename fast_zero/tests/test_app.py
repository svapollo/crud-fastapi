from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_html_deve_retornar_ok_e_ola_mundo_html(client):
    response_html = client.get('/html')

    assert response_html.status_code == HTTPStatus.OK
    assert '<html>' in response_html.text


def test_create_user_deve_retonar_201(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_email_errado_deve_retornar_422(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'aliceexample.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_read_users_deve_retornar_vazio_e_200(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_deve_retornar_usuario_e_200(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user_deve_retornar_200(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_deve_retornar_404(client, user, token):
    response = client.put(
        '/users/10',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'joao',
            'email': 'joao@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_deve_retornar_200(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_deve_retornar_404(client, user, token):
    response = client.delete(
        '/users/100', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}


def test_read_user_deve_retornar_200(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Test',
        'email': 'test@test.com',
        'id': 1,
    }


def test_create_user_deve_retornar_400_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Test',
            'email': 'alice@example.com',
            'password': 'senha',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_deve_retornar_400_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Alice',
            'email': 'test@test.com',
            'password': 'senha',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_get_token_deve_retornar_200(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_update_user_none(client, user, token_none):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_none}'},
        json={
            'username': 'Bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
