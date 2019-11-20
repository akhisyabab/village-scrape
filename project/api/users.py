from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)

from project.models.models import User, RevokedToken
from project import db
from project.utils.decorator import admin_required


class UserRegistration(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if User.find_by_username(username):
            return {'message': 'User already exists: {}'.format(username)}

        username = username
        password = User.generate_hash(password)

        try:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'message': 'User created: {}'.format(username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            return {'message': e}, 500


class UserLogin(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        current_user = User.find_by_username(username)
        if not current_user:
            return {'message': 'User doesn\'t exist: {}'.format(username)}

        if User.verify_hash(password, current_user.password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=password)
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except Exception:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    @admin_required
    def get(self):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password,
            }

        return {'users': list(map(lambda x: to_json(x), User.query.all()))}


class SecretResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        jti = get_raw_jwt()
        return {
            'current': current_user,
            'jti': jti,
        }


class UserProfile(Resource):
    @jwt_required
    def get(self):
        username = get_jwt_identity()
        current_user = User.find_by_username(username)
        if not current_user:
            return {'message': 'User doesn\'t exist: {}'.format(username)}

        detail = {}
        for column in current_user.__table__.columns:
            detail[column.name] = str(getattr(current_user, column.name))
        return detail


class UserEdit(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()
        current_user = User.find_by_username(username)
        if not current_user:
            return {'message': 'User doesn\'t exist: {}'.format(username)}

        try:
            current_user.phone = request.json.get('phone', None)
            current_user.address = request.json.get('address', None)

            db.session.commit()

            return {'message': 'Data updated: {}'.format(current_user.username)}

        except Exception as e:
            return {'message': e}, 500


class AddAdmin(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        secret = request.json.get('secret', None)
        role = 'admin'
        if secret != 'iniSECret':
            return {'message': 'Permission denied'}, 500

        if User.find_by_username(username):
            return {'message': 'Admin already exists: {}'.format(username)}

        username = username
        password = User.generate_hash(password)

        try:
            new_user = User(username, password, role)
            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'message': 'Admin created: {}'.format(username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            return {'message': e}, 500
