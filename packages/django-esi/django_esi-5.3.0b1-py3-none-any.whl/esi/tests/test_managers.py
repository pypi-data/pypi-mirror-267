from datetime import timedelta
from unittest.mock import Mock, patch

import requests_mock
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.utils.timezone import now

from ..errors import IncompleteResponseError, TokenError
from ..managers import _process_scopes
from ..models import Token
from . import _generate_token, _store_as_Token
from .jwt_factory import generate_jwk, generate_token


class TestProcessScopes(TestCase):

    def test_none(self):
        self.assertSetEqual(
            _process_scopes(None), set()
        )

    def test_empty_list(self):
        self.assertSetEqual(
            _process_scopes([]), set()
        )

    def test_single_string_1(self):
        self.assertSetEqual(
            _process_scopes(['one']),
            {'one'}
        )

    def test_single_string_2(self):
        self.assertSetEqual(
            _process_scopes(['one two three']),
            {'one', 'two', 'three'}
        )

    def test_list(self):
        self.assertSetEqual(
            _process_scopes(['one', 'two', 'three']),
            {'one', 'two', 'three'}
        )

    def test_tuple(self):
        self.assertSetEqual(
            _process_scopes(('one', 'two', 'three')),
            {'one', 'two', 'three'}
        )


class TestTokenQuerySet(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            'Bruce Wayne',
            'abc@example.com',
            'password'
        )
        self.user2 = User.objects.create_user(
            'Peter Parker',
            'abc@example.com',
            'password'
        )
        Token.objects.all().delete()

    @patch('esi.models.app_settings.ESI_TOKEN_VALID_DURATION', 120)
    def test_get_expired(self):
        _store_as_Token(
            _generate_token(
                character_id=101,
                character_name=self.user1.username,
                scopes=['abc']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=102,
                character_name=self.user2.username,
                scopes=['xyz']
            ),
            self.user2
        )
        self.assertEqual(list(Token.objects.get_queryset().get_expired()), [])

        t2.created -= timedelta(121)
        t2.save()
        self.assertEqual(list(Token.objects.get_queryset().get_expired()), [t2])

    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_ID', 'abc')
    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_SECRET', 'xyz')
    @patch('esi.models.Token.delete', autospec=True)
    @patch('esi.models.Token.refresh', autospec=True)
    @patch('esi.managers.requests.auth.HTTPBasicAuth', autospec=True)
    @patch('esi.managers.OAuth2Session', autospec=True)
    def test_bulk_refresh_normal(
        self,
        mock_OAuth2Session,
        mock_HTTPBasicAuth,
        mock_Token_refresh,
        mock_Token_delete
    ):
        character_id = 99
        character_name = 'Bruce Wayne'
        t1 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['xyz']
            ),
            self.user1
        )
        incomplete_qs = Token.objects.get_queryset().bulk_refresh()
        self.assertEqual(mock_Token_refresh.call_count, 2)
        self.assertEqual(mock_Token_delete.call_count, 0)
        self.assertSetEqual(
            set(incomplete_qs),
            {t1, t2}
        )

        # Note
        # looks like a bug in bulk_refresh():
        # this filter can never find anything, because refresh_token
        # can not be null:
        #   self.filter(refresh_token__isnull=True).get_expired().delete()

    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_ID', 'abc')
    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_SECRET', 'xyz')
    @patch('esi.models.Token.delete', autospec=True)
    @patch('esi.models.Token.refresh', autospec=True)
    @patch('esi.managers.requests.auth.HTTPBasicAuth', autospec=True)
    @patch('esi.managers.OAuth2Session', autospec=True)
    def test_bulk_refresh_token_error(
        self,
        mock_OAuth2Session,
        mock_HTTPBasicAuth,
        mock_Token_refresh,
        mock_Token_delete
    ):
        mock_Token_refresh.side_effect = TokenError

        character_id = 99
        character_name = 'Bruce Wayne'
        t1 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['xyz']
            ),
            self.user1
        )
        incomplete_qs = Token.objects.get_queryset().bulk_refresh()
        self.assertEqual(mock_Token_refresh.call_count, 2)
        self.assertEqual(mock_Token_delete.call_count, 2)
        self.assertSetEqual(
            set(incomplete_qs),
            {t1, t2}
        )

    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_ID', 'abc')
    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_SECRET', 'xyz')
    @patch('esi.models.Token.delete', autospec=True)
    @patch('esi.models.Token.refresh', autospec=True)
    @patch('esi.managers.requests.auth.HTTPBasicAuth', autospec=True)
    @patch('esi.managers.OAuth2Session', autospec=True)
    def test_bulk_refresh_incomplete_response_error(
        self,
        mock_OAuth2Session,
        mock_HTTPBasicAuth,
        mock_Token_refresh,
        mock_Token_delete
    ):
        mock_Token_refresh.side_effect = IncompleteResponseError

        character_id = 99
        character_name = 'Bruce Wayne'
        _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc']
            ),
            self.user1
        )
        _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['xyz']
            ),
            self.user1
        )
        incomplete_qs = Token.objects.get_queryset().bulk_refresh()
        self.assertEqual(mock_Token_refresh.call_count, 2)
        self.assertEqual(mock_Token_delete.call_count, 0)
        self.assertSetEqual(
            set(incomplete_qs),
            set()
        )

    @patch('esi.models.app_settings.ESI_TOKEN_VALID_DURATION', 120)
    @patch('esi.managers.TokenQueryset.bulk_refresh', autospec=True)
    def test_require_valid_none_expired(
        self,
        mock_bulk_refresh
    ):
        character_id = 99
        character_name = 'Bruce Wayne'
        t1 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['xyz']
            ),
            self.user1
        )
        mock_bulk_refresh.return_value = Token.objects.none()

        self.assertSetEqual(
            set(Token.objects.get_queryset().require_valid()),
            {t1, t2}
        )

    @patch('esi.models.app_settings.ESI_TOKEN_VALID_DURATION', 120)
    @patch('esi.managers.TokenQueryset.bulk_refresh', autospec=True)
    def test_require_valid_some_expired(
        self,
        mock_bulk_refresh
    ):
        character_id = 99
        character_name = 'Bruce Wayne'
        t1 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['xyz']
            ),
            self.user1
        )
        t2.created -= timedelta(121)
        t2.save()
        mock_bulk_refresh.return_value = Token.objects.filter(pk__in=[t2.pk])

        self.assertSetEqual(
            set(Token.objects.get_queryset().require_valid()),
            {t1, t2}
        )

    @patch('esi.models.app_settings.ESI_TOKEN_VALID_DURATION', 120)
    @patch('esi.managers.TokenQueryset.bulk_refresh', autospec=True)
    def test_require_valid_one_refresh_error(
        self,
        mock_bulk_refresh
    ):
        character_id = 99
        character_name = 'Bruce Wayne'
        t1 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['xyz']
            ),
            self.user1
        )
        t2.created -= timedelta(121)
        t2.save()
        mock_bulk_refresh.return_value = Token.objects.none()

        self.assertSetEqual(
            set(Token.objects.get_queryset().require_valid()),
            {t1}
        )

    def test_require_scopes_normal(self):
        character_id = 99
        character_name = 'Bruce Wayne'
        t1 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', 'xyz', '123']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', 'xyz']
            ),
            self.user1
        )
        t3 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', '123']
            ),
            self.user1
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().require_scopes('abc')), {t1, t2, t3}
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().require_scopes('xyz')), {t1, t2}
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().require_scopes('123')), {t1, t3}
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().require_scopes('555')), set()
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().require_scopes('abc xyz 123')), {t1}
        )

    def test_require_scopes_empty(self):
        character_id = 99
        character_name = 'Bruce Wayne'
        _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', 'xyz', '123']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name
            ),
            self.user1
        )
        t2.scopes.all().delete()
        _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', '123']
            ),
            self.user1
        )
        self.assertSetEqual(set(Token.objects.get_queryset().require_scopes('')), {t2})

    def test_require_scopes_exact(self):
        character_id = 99
        character_name = 'Bruce Wayne'
        _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', 'xyz', '123']
            ),
            self.user1
        )
        t2 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', 'xyz']
            ),
            self.user1
        )
        t3 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', '123']
            ),
            self.user1
        )
        t4 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', '123']
            ),
            self.user1
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().require_scopes_exact('abc')), set()
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().require_scopes_exact('abc xyz')), {t2}
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().require_scopes_exact('abc 123')), {t3, t4}
        )

    def test_require_scopes_exact_2(self):
        character_id = 99
        character_name = 'Bruce Wayne'
        _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', 'xyz', '123']
            ),
            self.user1
        )
        _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['abc', 'xyz']
            ),
            self.user1
        )
        t3 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['xyz', '123']
            ),
            self.user1
        )
        t4 = _store_as_Token(
            _generate_token(
                character_id=character_id,
                character_name=character_name,
                scopes=['xyz', '123']
            ),
            self.user1
        )
        self.assertSetEqual(
            set(Token.objects.get_queryset().equivalent_to(t3)), {t4}
        )


class TestTokenManager(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user1 = User.objects.create_user(
            'Bruce Wayne',
            'abc@example.com',
            'password'
        )

    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_ID', 'abc')
    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_SECRET', 'xyz')
    @patch('esi.managers.app_settings.ESI_SSO_CALLBACK_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_TOKEN_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_TOKEN_VERIFY_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_ALWAYS_CREATE_TOKEN', False)
    @patch('esi.managers.TokenManager._decode_jwt')
    @patch('esi.managers.OAuth2Session', autospec=True)
    def test_create_from_code_single_scope(self, mock_OAuth2Session, mock_decode_jwt):
        """Normal case with refresh token"""
        mock_oauth = Mock()
        mock_oauth.request.return_value.json.return_value = \
            _generate_token(
                99, 'Bruce Wayne', scopes='publicData'
            )
        mock_oauth.fetch_token.return_value = {
            'access_token': 'access_token',
            'refresh_token': 'refresh_token',
            'token_type': 'Bearer',
            'expires_in': 1200,
        }
        mock_OAuth2Session.return_value = mock_oauth
        mock_decode_jwt.return_value = \
            _generate_token(
                99, 'Bruce Wayne', scopes='publicData'
            )
        # create new token from code
        token1 = Token.objects.create_from_code('abc123xyz')
        self.assertEqual(
            token1.character_id,
            99
        )
        self.assertEqual(
            token1.character_name,
            'Bruce Wayne'
        )
        self.assertEqual(
            token1.scopes.all().count(),
            1
        )
        # should return existing token instead of creating a new one
        # since ESI_ALWAYS_CREATE_TOKEN is False
        token2 = Token.objects.create_from_code('11abc123xyz')
        self.assertEqual(token1, token2)

    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_ID', 'abc')
    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_SECRET', 'xyz')
    @patch('esi.managers.app_settings.ESI_SSO_CALLBACK_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_TOKEN_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_TOKEN_VERIFY_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_ALWAYS_CREATE_TOKEN', False)
    @patch('esi.managers.TokenManager._decode_jwt')
    @patch('esi.managers.OAuth2Session', autospec=True)
    def test_create_from_code_1(self, mock_OAuth2Session, mock_decode_jwt):
        """Normal case with refresh token"""
        mock_oauth = Mock()
        mock_oauth.request.return_value.json.return_value = \
            _generate_token(
                99, 'Bruce Wayne', scopes=[
                    'esi-calendar.read_calendar_events.v1',
                    'esi-location.read_location.v1',
                    'esi-location.read_ship_type.v1',
                    'esi-unknown-scope'
                ]
            )
        mock_oauth.fetch_token.return_value = {
            'access_token': 'access_token',
            'refresh_token': 'refresh_token',
            'token_type': 'Bearer',
            'expires_in': 1200,
        }
        mock_OAuth2Session.return_value = mock_oauth
        mock_decode_jwt.return_value = \
            _generate_token(
                99, 'Bruce Wayne', scopes=[
                    'esi-calendar.read_calendar_events.v1',
                    'esi-location.read_location.v1',
                    'esi-location.read_ship_type.v1',
                    'esi-unknown-scope'
                ]
            )
        # create new token from code
        token1 = Token.objects.create_from_code('abc123xyz')
        self.assertEqual(
            token1.character_id,
            99
        )
        self.assertEqual(
            token1.character_name,
            'Bruce Wayne'
        )
        self.assertEqual(
            token1.scopes.all().count(),
            4
        )

        # should return existing token instead of creating a new one
        # since ESI_ALWAYS_CREATE_TOKEN is False
        token2 = Token.objects.create_from_code('11abc123xyz')
        self.assertEqual(token1, token2)

    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_ID', 'abc')
    @patch('esi.managers.app_settings.ESI_SSO_CLIENT_SECRET', 'xyz')
    @patch('esi.managers.app_settings.ESI_SSO_CALLBACK_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_TOKEN_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_TOKEN_VERIFY_URL', 'localhost')
    @patch('esi.managers.app_settings.ESI_ALWAYS_CREATE_TOKEN', False)
    @patch('esi.managers.TokenManager._decode_jwt')
    @patch('esi.managers.OAuth2Session', autospec=True)
    def test_create_from_code_2(self, mock_OAuth2Session, mock_decode_jwt):
        """Special case w/o refresh token"""
        mock_oauth = Mock()
        mock_oauth.request.return_value.json.return_value = \
            _generate_token(
                99, 'Bruce Wayne', scopes=[
                    'esi-calendar.read_calendar_events.v1',
                    'esi-location.read_location.v1',
                    'esi-location.read_ship_type.v1',
                    'esi-unknown-scope'
                ]
            )
        mock_oauth.fetch_token.return_value = {
            'access_token': 'access_token',
            'refresh_token': None,
            'token_type': 'Bearer',
            'expires_in': 1200,
        }
        mock_OAuth2Session.return_value = mock_oauth
        mock_decode_jwt.return_value = \
            _generate_token(
                99, 'Bruce Wayne', scopes=[
                    'esi-calendar.read_calendar_events.v1',
                    'esi-location.read_location.v1',
                    'esi-location.read_ship_type.v1',
                    'esi-unknown-scope'
                ]
            )
        # create new token from code
        token1 = Token.objects.create_from_code('abc123xyz')
        self.assertEqual(
            token1.character_id,
            99
        )
        self.assertEqual(
            token1.character_name,
            'Bruce Wayne'
        )
        self.assertEqual(
            token1.scopes.all().count(),
            4
        )

        # should return existing token instead of creating a new one
        # since ESI_ALWAYS_CREATE_TOKEN is False
        token2 = Token.objects.create_from_code('11abc123xyz')
        self.assertEqual(token1, token2)

    @patch('esi.managers.TokenManager.create_from_code', autospec=True)
    def test_create_from_request(self, mock_create_from_code):
        mock_create_from_code.return_value = 'we got you'

        request = self.factory.get('https://www.example.com?code=abc123')
        request.user = self.user1

        middleware = SessionMiddleware(HttpResponse)
        middleware.process_request(request)
        request.session.save()

        x = Token.objects.create_from_request(request)
        self.assertEqual(x, 'we got you')
        self.assertEqual(mock_create_from_code.call_args[0][1], 'abc123')


@requests_mock.Mocker()
class TestTokenManagerValidateAccessToken(TestCase):
    def test_should_return_token_1(self, requests_mocker):
        # given
        jwks = {"keys": [generate_jwk()]}
        requests_mocker.register_uri(
            "GET", url="https://login.eveonline.com/oauth/jwks", json=jwks
        )
        access_token, _ = generate_token(1001, "Bruce Wayne")
        # when
        token = Token.objects.validate_access_token(access_token)
        # then
        self.assertEqual(token["character_id"], 1001)
        self.assertEqual(token["name"], "Bruce Wayne")
        self.assertEqual(token["token_type"], "character")

    def test_should_return_token_2(self, requests_mocker):
        # given
        jwks = {"keys": [generate_jwk()]}
        requests_mocker.register_uri(
            "GET", url="https://login.eveonline.com/oauth/jwks", json=jwks
        )
        access_token, _ = generate_token(
            1001, "Bruce Wayne", issuer="https://login.eveonline.com"
        )
        # when
        token = Token.objects.validate_access_token(access_token)
        # then
        self.assertEqual(token["character_id"], 1001)
        self.assertEqual(token["name"], "Bruce Wayne")
        self.assertEqual(token["token_type"], "character")

    def test_should_return_none_when_no_jwk(self, requests_mocker):
        # given
        jwks = dict()
        requests_mocker.register_uri(
            "GET", url="https://login.eveonline.com/oauth/jwks", json=jwks
        )
        access_token, _ = generate_token(1001, "Bruce Wayne", audience=False)
        # when
        result = Token.objects.validate_access_token(access_token)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_expired(self, requests_mocker):
        # given
        jwks = {"keys": [generate_jwk()]}
        requests_mocker.register_uri(
            "GET", url="https://login.eveonline.com/oauth/jwks", json=jwks
        )
        issued_at = now() - timedelta(hours=3)
        access_token, _ = generate_token(1001, "Bruce Wayne", issued_at=issued_at)
        # when
        result = Token.objects.validate_access_token(access_token)
        # then
        self.assertIsNone(result)

    def test_should_return_none_when_invalid(self, requests_mocker):
        # given
        jwks = {"keys": [generate_jwk()]}
        requests_mocker.register_uri(
            "GET", url="https://login.eveonline.com/oauth/jwks", json=jwks
        )
        access_token = "invalid"
        # when
        result = Token.objects.validate_access_token(access_token)
        # then
        self.assertIsNone(result)
