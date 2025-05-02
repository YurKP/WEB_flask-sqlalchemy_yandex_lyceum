from flask_restful import abort, Resource
from flask import jsonify

from data import db_session
from data.users import User
from data.parser_users import parser


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)

        session = db_session.create_session()
        user = session.query(User).get(user_id)

        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'email'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)

        session = db_session.create_session()
        user = session.query(User).get(user_id)

        session.delete(user)
        session.commit()

        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()

        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'surname')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email']
        )

        session.add(user)
        session.commit()

        return jsonify({'id': user.id})