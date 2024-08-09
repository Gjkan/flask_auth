from flask import Blueprint, request, make_response, jsonify, current_app
from flask.views import MethodView

from project.models import User, BlacklistToken, decode_auth_token

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    API для регистрации пользователя
    """

    @staticmethod
    def post():
        """Endpoint для обработки post запросов"""
        post_data = request.get_json()
        user_id = User.get_user_id_or_none(email=post_data.get('email'))

        if not user_id:
            try:
                User.save(email=post_data.get('email'),
                          password=post_data.get('password'))
                user_dict = User.get_user_dict_by_email(email=post_data.get('email'))
                auth_token = User.encode_auth_token(user_id=user_dict['id'])
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully registered.',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(response_object)), 201
            except Exception as e:
                print(e)
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(response_object)), 202


class LoginAPI(MethodView):
    """
    API для авторизации пользователя по email и password. Возвращает ответ c json с auth_token и status 'success' и
    message 'Successfully logged in', если авторизация прошла успешно, в противном случае возвращает json без
    auth_token и с другими осмысленными status и message
    """

    @staticmethod
    def post():
        """Endpoint для обработки post запросов"""
        post_data = request.get_json()
        try:
            user_dict = User.get_user_dict_by_email(email=post_data.get('email'))
            if user_dict:
                bcrypt = current_app.config['BCRYPT']
                if bcrypt.check_password_hash(
                        user_dict['password'], post_data.get('password')):
                    auth_token = User.encode_auth_token(user_id=user_dict['id'])
                    if auth_token:
                        response_object = {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token
                        }
                        return make_response(jsonify(response_object)), 200
                    else:
                        raise Exception('Ошибка при получении токена пользователя')
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'Try again.',
                    }
                    return make_response(jsonify(response_object)), 500

            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response_object)), 404
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again.'
            }
            return make_response(jsonify(response_object)), 500


class UserAPI(MethodView):
    """
    API для аутентификации пользователя по заголовку Authorization.
    Возвращает ответ с json со словарём с данными пользователя и status 'success', если авторизация прошла успешно.
    В противном случае возвращает status 'fail' и осмысленные message
    """

    @staticmethod
    def get():
        """Endpoint для обработки get запросов"""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_object = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user_dict = User.get_user_dict_by_id(user_id=resp)
                response_object = {
                    'status': 'success',
                    'data': user_dict
                }
                return make_response(jsonify(response_object)), 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 401


class LogoutAPI(MethodView):
    """
    API для выхода пользователя по заголовку Authorization.
    Возвращает ответ с json со словарём с данными пользователя и status 'success', если выход прошла успешно.
    В противном случае возвращает status 'fail' и осмысленные message
    """

    @staticmethod
    def post():
        """Endpoint для обработки post запросов"""
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_object = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(response_object)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                try:
                    BlacklistToken.save(token=auth_token)
                    if BlacklistToken.is_token_in_blacklist(token=auth_token):
                        response_object = {
                            'status': 'success',
                            'message': 'Successfully logged out.'
                        }
                        return make_response(jsonify(response_object)), 200
                    else:
                        response_object = {
                            'status': 'fail',
                            'message': 'logout is fail'
                        }
                        return make_response(jsonify(response_object)), 401
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object)), 403


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
