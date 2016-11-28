import psycopg2
import settings
import urllib

from flask import Flask, jsonify, abort, make_response
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from lib.helpers import cln
from psycopg2.extras import RealDictCursor

app = Flask(__name__, static_url_path=None)
cors = CORS(app, resources={r"/*": {"origins": "alexsrhodes.webfactional.com"}})
api = Api(app)
# auth = HTTPBasicAuth()

try:
    conn = psycopg2.connect(database='postgres',
                            user='postgres',
                            host='127.0.0.1',
                            port='5432')
    cur = conn.cursor(cursor_factory=RealDictCursor)
except Exception as e:
    print("DB connection failed, exiting with Exception:")
    print(e)
    exit(1)

'''
*create a new team with a new user as team leader

create a new user

Pass employee username and password, if it's valid, return the entire team that employee is on, with all of the boards/categories/cards etc. that are under that team object

create a new board with title/description

create a new category with title and description

create a new card with title, description, due date etc. and an employee to assign it to

move a card from one category to another

delete a card

delete a category
'''


class CardAPI(Resource):
    # Example: <host>/cards/33
    def get(self, id):
        # Use comma, not % to avoid sql injection
        cur.execute('SELECT * FROM card WHERE id = %s;', [id])
        card = cur.fetchone()
        return jsonify(card)

    def delete(self, id):
        cur.execute('delete from card where id = %s;', [id])
        conn.commit()
        return True


class TeamMemberAPI(Resource):
    # Example: <host>/users/sgarcia0%40wordpress.org
    # NOTE: the email needs to be url_encoded
    def get(self, email):
        cur.execute('SELECT email, hiredate, name, role FROM TeamMember WHERE email = %s;',
                    [cln(email)])
        tm = cur.fetchone()
        return jsonify(tm)

    # def post(self, name, email, role, pwd, type):
    #     if cln(type).lower() not in ['seniordev', 'intern', 'juniordev']:
    #         return {'error': 'Invalid type. Must be seniordev, intern, or juniordev.'}
    #
    #     query = "insert into teammember(name, email, role, password, hiredate) values (%s, %s, %s, %s, now());"
    #     cur.execute(query, [cln(name), cln(email), cln(role), cln(pwd)])
    #
    #     conn.commit()



class BoardAPI(Resource):
    # Example: <host>/boards/Ameliorated
    # NOTE: The title needs to be url_encoded
    def get(self, title):
        title_clean = urllib.unquote(title).decode('utf8')
        cur.execute('select * from board where title = %s;',
                    [title_clean])
        board = cur.fetchone()

        query = '''select c.id, c.title, c.description
                   from boardContains bc, Category c
                   where bc.board_title = %s and
                         bc.category_id = c.id;'''
        cur.execute(query, [title_clean])
        categories = cur.fetchall()

        for c in categories:
            query = '''select *
                       from categorizedAs ca, Card c
                       where ca.category_id = %s and
                             ca.category_id = c.id;'''
            cur.execute(query, [c['id']])
            cards = cur.fetchall()
            c['cards'] = cards

        board['categories'] = categories
        return jsonify(board)

class TeamAPI(Resource):
    # Create a Team with TeamMember as leader
    # Example: <host>/addteam/name=CoolTeam&email=sgarcia0%40wordpress.org
    def post(self, name, email):
        query = 'select * from teammember tm, seniordev sd where tm.email = %s and sd.email = %s;'
        cur.execute(query, [cln(email), cln(email)])
        teammember = cur.fetchone()
        if not teammember:
            return {'error': 'No team member with that email.'}

        # Create team
        query = '''insert into Team(name) values (%s);'''
        cur.execute(query, [cln(name)])

        # Create composedOf
        query = "insert into composedOf(team_name, member_email) values (%s, %s);"
        cur.execute(query, [cln(name), cln(email)])

        # Create hasLeader
        query = "insert into hasLeader(team_name, dev_email) values (%s, %s);"
        cur.execute(query, [cln(name), cln(email)])

        conn.commit()
        return True




api.add_resource(CardAPI, '/cards/<int:id>', endpoint='card')
api.add_resource(TeamMemberAPI, '/users/<string:email>', endpoint='user')
api.add_resource(BoardAPI, '/boards/<string:title>', endpoint='board')
api.add_resource(TeamAPI, '/addteam/name=<string:name>&email=<string:email>')


if __name__ == '__main__':
    app.run(debug=settings.ENABLE_DEBUG)
