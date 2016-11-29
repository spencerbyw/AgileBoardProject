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
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
# auth = HTTPBasicAuth()

try:
    conn = psycopg2.connect(database='postgres',
                            user='postgres',
                            host='127.0.0.1',
                            port='5432')
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=RealDictCursor)
except Exception as e:
    print("DB connection failed, exiting with Exception:")
    print(e)
    exit(1)

'''
*create a new team with a new user as team leader

*create a new user

Pass employee username and password, if it's valid, return the entire team that employee is on, with all of the boards/categories/cards etc. that are under that team object

create a new board with title/description

create a new category with title and description

create a new card with title, description, due date etc. and an employee to assign it to

move a card from one category to another

delete a card

delete a category
'''


class CardAPI(Resource):
    # Example: GET <host>/card/33
    def get(self, id):
        # Use comma, not % to avoid sql injection
        cur.execute('SELECT * FROM card WHERE id = %s;', [id])
        card = cur.fetchone()
        return jsonify(card)

    # Create new card in backlog of board_title (due_date is MM-DD-YYYY)
    # Example: POST <host>/newcard/board_title=Ameliorated&priority=MED&description=Freaking%20cool&title=Great%20Card&due_date=09-15-2017
    def post(self, board_title, priority, description, title, due_date):
        # Make sure board exists and priority is right
        query = 'select * from board where title = %s;'
        cur.execute(query, [cln(board_title)])
        if not cur.fetchone() and cln(priority) in ['LOW', 'MED', 'HIGH']:
            return {'error': 'Board does not exist.'}

        query = 'insert into card (due_date, priority, description, title) values (%s, %s, %s, %s) ' \
                'returning id, due_date, priority, description, title;'
        cur.execute(query, [cln(due_date), cln(priority), cln(description), cln(title)])
        card = cur.fetchone()
        card_id = card['id']

        query = 'insert into isbackloggedon (board_title, card_id) values (%s, %s);'
        cur.execute(query, [cln(board_title), card_id])
        # conn.commit()
        return jsonify(card)

    # Example: DELETE <host>/card/33
    def delete(self, id):
        cur.execute('delete from categorizedAs where card_id = %s;', [id])
        cur.execute('delete from assignedTo where card_id = %s;', [id])
        cur.execute('delete from isBackloggedOn where card_id = %s;', [id])
        cur.execute('delete from card where id = %s;', [id])
        # conn.commit()
        return True


class MoveCardAPI(Resource):
    # Move a card from backlog/category to new category
    # card_id is the card you want to move.
    # category_id is the target category. The server handles the idiosyncrasies.
    # Example: PUT <host>/movecard/card_id=1&category_id=2
    def put(self, card_id, category_id):
        # Check card and category exist
        query = 'select * from card where id = %s;'
        cur.execute(query, [card_id])
        c = cur.fetchone()
        query = 'select * from category where id = %s;'
        cur.execute(query, [category_id])
        if not c and not cur.fetchone():
            return {'error': 'Invalid category or card id'}

        # Delete any old categorizedAs's or isBackloggedOn's
        query = 'delete from categorizedAs where card_id = %s;'
        cur.execute(query, [card_id])
        query = 'delete from isbackloggedon where card_id = %s;'  # Assume you have access to board for now
        cur.execute(query, [card_id])

        # Create new categorizedAs
        query = 'insert into categorizedAs (category_id, card_id) values (%s, %s);'
        cur.execute(query, [category_id, card_id])

        return True


class AssignCardAPI(Resource):
    # Assign card to a specific user
    # Example: PUT <host>/assigncard/email=sgarcia0%40wordpress.org&card_id=49
    def put(self, email, card_id):
        # Check user and card exist
        query = 'select * from teammember where email = %s;'
        cur.execute(query, [cln(email)])
        tm = cur.fetchone()
        query = 'select * from card where id = %s;'
        cur.execute(query, [card_id])
        if not tm and not cur.fetchone():
            return {'error': 'Card and/or TeamMember does/do not exist.'}

        # Delete previous assignments to that card
        query = 'delete from assignedTo where card_id = %s;'
        cur.execute(query, [card_id])

        # Create new assignedTo
        query = 'insert into assignedTo(member_email, card_id) values (%s, %s);'
        cur.execute(query, [cln(email), card_id])

        # conn.commmit()
        return True


class FilteredCardsAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('priority', location='args', choices=['LOW', 'MED', 'HIGH'])
    parser.add_argument('past_due', type=bool, location='args')
    parser.add_argument('assignee', location='args')
    parser.add_argument('board_title', required=True, location='args')

    # Get list of cards based on argument filters
    # Argument order DOES NOT MATTER FOR THIS ENDPOINT
    # The only required argument is board_title
    # Examples: GET <host>/filteredcards?board_title=Ameliorated    -> All cards in board
    #               <host>/filteredcards?board_title=Ameliorated&priority=LOW    -> LOW priority cards in board
    #               <host>/filteredcards?board_title=Ameliorated&assignee=cstonef%40sciencedaily.com&priority=MED
    #               <host>/filteredcards?board_title=Ameliorated&past_due=true
    def get(self):
        args = self.parser.parse_args()
        query = 'select * from (' \
                'select c.* from card c, category cat, boardContains bc, categorizedAs ca where ' \
                'bc.board_title = %s and ' \
                'bc.category_id = cat.id and ' \
                'cat.id = ca.category_id and ' \
                'ca.card_id = c.id ' \
                'UNION ' \
                'select c.* from card c, isbackloggedon ibo where ' \
                'ibo.board_title = %s and ' \
                'ibo.card_id = c.id' \
                ') all_cards ' \
                'where ' \
                '1 = 1'
        if args['priority']:
            query += ' and all_cards.priority = \'%s\'' % args['priority']
        if args['past_due']:
            query += ' and all_cards.due_date < now()'
        query += ';'
        cur.execute(query, [cln(args['board_title']), cln(args['board_title'])])
        cards = cur.fetchall()

        # Add assignedTo field
        for c in cards:
            query = 'select tm.name, tm.email from assignedTo at, TeamMember tm where ' \
                    'at.member_email = tm.email and ' \
                    'at.card_id = %s;'
            cur.execute(query, [c['id']])
            c['assignedto'] = cur.fetchone()
        if args['assignee']:
            cards = [c for c in cards if c['assignedto']]  # Filter by exists
            cards = [c for c in cards if c['assignedto']['email'] == cln(args['assignee'])]  # Filter by assignee
        return jsonify(cards)


class TeamMemberAPI(Resource):
    # Example: GET <host>/users/sgarcia0%40wordpress.org
    def get(self, email):
        cur.execute('SELECT email, hiredate, name, role FROM TeamMember WHERE email = %s;',
                    [cln(email)])
        tm = cur.fetchone()
        return jsonify(tm)

    # Example: POST <host>/adduser/name=Bob&email=bob%40bob.com&role=Ninja&pwd=afWIOJf&ent_type=SeniorDev
    def post(self, name, email, role, pwd, ent_type):
        if cln(ent_type).lower() not in ['seniordev', 'intern', 'juniordev']:
            return {'error': 'Invalid type. Must be seniordev, intern, or juniordev.'}

        query = "insert into teammember(name, email, role, password, hiredate) values (%s, %s, %s, %s, now());"
        cur.execute(query, [cln(name), cln(email), cln(role), cln(pwd)])
        query = "insert into {} (email) values (%s);".format(ent_type)
        cur.execute(query, [cln(email)])

        # conn.commit()
        return True


class BoardAPI(Resource):
    # Example: <host>/board/Ameliorated
    # NOTE: The title needs to be url_encoded
    def get(self, title):
        title_clean = cln(title)
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
        # TODO: return backlog
        return jsonify(board)

    # Create a new Board run by specified Team
    # Example: POST <host>/board/team_name=Flexidy&board_title=Wowza&board_desc=So%20cool
    def post(self, team_name, board_title, board_desc):
        # Make sure Team exists
        cur.execute('select * from team where name = %s;', [cln(team_name)])
        if not cur.fetchone():
            return {'error': 'Team does not exist'}
        # Make sure Board DNE
        cur.execute('select * from board where title = %s;', [cln(board_title)])
        if cur.fetchone():
            return {'error': 'Board already exists.'}

        # Create the Board and runBy
        query = 'insert into Board (title, description) values (%s, %s);'
        cur.execute(query, [cln(board_title), cln(board_desc)])
        query = 'insert into runBy (board_title, team_name) values (%s, %s);'
        cur.execute(query, [cln(board_title), cln(team_name)])
        return True


class EverythingAPI(Resource):
    # This is the cure-all, the origin. Returns mostly everything you need to render the page.
    # Example: <host>/userboard/user=sgarcia0%40wordpress.org&pwd=gWA61Du6h
    def get(self, email, pwd):
        uemail = cln(email)

        # Get pertinent user
        query = "select name, email, role, hiredate from teammember where email = %s and password = %s;"
        cur.execute(query, [uemail, cln(pwd)])
        uinfo = cur.fetchone()
        if not uinfo:
            return {'error': 'User not found with those credentials.'}

        # Get user's team
        query = "select t.name from team t, composedOf co where t.name = co.team_name and co.member_email = %s;"
        cur.execute(query, [uemail])
        tinfo = cur.fetchone()
        query = 'select tm.name, tm.email, tm.role, tm.hireDate from composedOf co, teammember tm ' \
                'where co.team_name = %s and co.member_email = tm.email;'
        cur.execute(query, [tinfo['name']])
        tinfo['members'] = cur.fetchall()

        # Get boards run by team
        query = "select b.title, b.description from board b, runby rb " \
                "where b.title = rb.board_title and rb.team_name = %s;"
        cur.execute(query, [tinfo['name']])
        board = cur.fetchone()

        # Get Categories in board
        btitle = board['title']
        cur.execute('select * from board where title = %s;',
                    [btitle])

        board = cur.fetchone()

        query = 'select c.id, c.title, c.description ' \
                'from boardContains bc, Category c ' \
                'where bc.board_title = %s and bc.category_id = c.id;'
        cur.execute(query, [btitle])
        categories = cur.fetchall()

        def get_assigned_to(cards):
            for card in cards:
                q = 'select member_email, name ' \
                    'from assignedTo, teammember ' \
                    'where card_id = %s and member_email = email;'
                cur.execute(q, [card['id']])
                cinfo = cur.fetchone()
                if cinfo:
                    card['assignedto'] = cinfo
                else:
                    card['assignedto'] = None

        # Get Cards for each Category
        for c in categories:
            query = 'select c.id, c.due_date, c.priority, c.description, c.title ' \
                    'from categorizedAs ca, Card c ' \
                    'where ca.category_id = %s and ca.card_id = c.id;'
            cur.execute(query, [c['id']])
            cards = cur.fetchall()
            get_assigned_to(cards)

            c['cards'] = cards

        board['categories'] = categories

        # Get Cards in board backlog
        query = 'select c.id, c.due_date, c.priority, c.description, c.title ' \
                'from card c, isbackloggedon ibo ' \
                'where ibo.board_title = %s and ibo.card_id = c.id;'
        cur.execute(query, [btitle])
        backlogged_cards = cur.fetchall()
        get_assigned_to(backlogged_cards)

        board['backlog'] = backlogged_cards

        # Put it all together
        tinfo['board'] = board
        uinfo['team'] = tinfo
        return jsonify(uinfo)


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

        # conn.commit()
        return True


class CategoryAPI(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('board_title', required=True, location='args')
    parser.add_argument('cat_title', required=True, location='args')
    parser.add_argument('cat_desc', required=True, location='args')

    # Create a new category in board
    # Example: POST <host>/category?board_title=Ameliorated&cat_title=New%20Category&cat_desc=Such%20category
    def post(self):
        args = self.parser.parse_args()
        # Ensure board exists
        cur.execute('select * from board where title = %s;', [cln(args['board_title'])])
        if not cur.fetchone():
            return {'error': 'Board does not exist'}

        query = 'insert into category (title, description) values (%s, %s) returning id, title, description;'
        cur.execute(query, [cln(args['cat_title']), cln(args['cat_desc'])])
        cat = cur.fetchone()
        query = 'insert into boardContains (board_title, category_id) values (%s, %s);'
        cur.execute(query, [cln(args['board_title']), cat['id']])
        return jsonify(cat)

    # Delete a category and all contained Cards
    # Example: DELETE <host>/category/3
    def delete(self, cat_id):
        # Get all categorizedAs's
        query = 'select * from categorizedas where category_id = %s;'
        cur.execute(query, [cat_id])
        cas = cur.fetchall()

        # Delete boardContains
        cur.execute('delete from boardcontains where category_id = %s;', [cat_id])
        # Delete all categorizedAs's
        cur.execute('delete from categorizedas where category_id = %s;', [cat_id])
        # Delete all Cards
        for ca in cas:
            cur.execute('delete from card where id = %s;', [ca['card_id']])

        # Delete the Category
        cur.execute('delete from category where id = %s;', [cat_id])

        return {'message': 'Deleted %s cards and category %s.' % (len(cas), cat_id)}


api.add_resource(CardAPI, '/card/<int:id>', endpoint='card')
api.add_resource(CardAPI, '/newcard/board_title=<string:board_title>&'
                          'priority=<string:priority>&description=<string:description>&'
                          'title=<string:title>&due_date=<string:due_date>',
                 endpoint='newcard')

api.add_resource(MoveCardAPI, '/movecard/card_id=<int:card_id>&category_id=<int:category_id>')

api.add_resource(AssignCardAPI, '/assigncard/email=<string:email>&card_id=<int:card_id>')

api.add_resource(FilteredCardsAPI, '/filteredcards')

api.add_resource(TeamMemberAPI, '/users/<string:email>', endpoint='user')
api.add_resource(TeamMemberAPI, '/adduser/name=<string:name>&email=<string:email>&role=<string:role>&'
                                'pwd=<string:pwd>&ent_type=<string:ent_type>',
                 endpoint='adduser')

api.add_resource(BoardAPI, '/board/<string:title>', '/board/team_name=<string:team_name>&'
                                                    'board_title=<string:board_title>&board_desc=<string:board_desc>',
                 endpoint='board')

api.add_resource(EverythingAPI, '/userboard/user=<string:email>&pwd=<string:pwd>', endpoint='userboard')
api.add_resource(TeamAPI, '/addteam/name=<string:name>&email=<string:email>', endpoint='addteam')

api.add_resource(CategoryAPI, '/category', '/category/<int:cat_id>', endpoint='category')


if __name__ == '__main__':
    app.run(debug=settings.ENABLE_DEBUG)
