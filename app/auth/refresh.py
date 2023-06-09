from flask import make_response, request
from flask_restx import Namespace, Resource
from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer

from logic.user.application.AuthService import JwtAuthService

refresh_ns = Namespace('refresh', description='토큰 갱신')

parser = refresh_ns.parser()
parser.add_argument('Authorization', type=str, location='headers', help='Refresh Token')


@refresh_ns.route('')
class Refresh(Resource):
    @refresh_ns.doc(parser=parser, description="refresh 토큰으로 새로운 access token을 발급합니다 ")
    @refresh_ns.response(code=200, description='갱신 성공', headers={'Authentication': 'access_token'})
    @inject
    def get(self, jwt_auth_service: JwtAuthService = Provide[UserContainer.auth_service]):
        """토큰 갱신"""
        refresh_token = request.headers['Authorization']

        access_token = jwt_auth_service.refresh(refresh_token)

        res = make_response()
        res.headers['Authentication'] = f'{access_token}'

        return res
