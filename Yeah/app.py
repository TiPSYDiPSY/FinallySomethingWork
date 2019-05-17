import sqlite3 as lite
import jwt
import os
import time
import uuid
from flask import Flask, request, jsonify, session
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
app.secret_key = os.urandom(24)


class Login(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        un = json_data['username']
        pw = json_data['password']
        if un == 'admin' and pw == ';--!s@fepassw0rd':
            encoded_jwt = jwt.encode({'username': un}, 'OH HI MARK', algorithm='HS256')
            session['user'] = 'admin'
            return jsonify(token=encoded_jwt.decode("utf-8"))
        else:
            return jsonify(Access="Access denied")


class Palindrome(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        value = json_data['value']
        if isinstance(value, float):
            return {'Error': "Only String or Int Accepted"}
        conn = lite.connect('Palindrome.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS palindromes(id TEXT,date TEXT,value TEXT,is_palindrome TEXT)')
        c.execute("""SELECT * FROM palindromes WHERE value = ?""", (value,))
        rows = c.fetchall()
        if rows is not None:
            for row in rows:
                return {'is_palindrome': row[3]}
        id = uuid.uuid4()
        localtime = time.asctime(time.localtime(time.time()))
        if not isinstance(value, str):
            temp = value
            n = value
            rev = 0
            while n > 0:
                dig = n % 10
                rev = rev * 10 + dig
                n = n // 10
            if temp == rev:

                c.execute("INSERT INTO palindromes(id, date, value, is_palindrome) VALUES(?,?,?,?)",
                          (str(id), str(localtime), str(value), "True"))
                conn.commit()
                return {'is_palindrome': True}
            else:

                c.execute("INSERT INTO palindromes(id, date, value, is_palindrome) VALUES(?,?,?,?)",
                          (str(id), str(localtime), str(value), "False"))
                conn.commit()
                return {'is_palindrome': False}

        else:
            ans = isPalindrome(value)

            if ans == 1:
                c.execute("INSERT INTO palindromes(id, date, value, is_palindrome) VALUES(?,?,?,?)",
                          (str(id), str(localtime), str(value), "True"))
                conn.commit()
                return {'is_palindrome': True}
            else:
                c.execute("INSERT INTO palindromes(id, date, value, is_palindrome) VALUES(?,?,?,?)",
                          (str(id), str(localtime), str(value), "False"))
                conn.commit()
                return {'is_palindrome': False}


def reverse(s):
    return s[::-1]


def isPalindrome(s):
    rev = reverse(s)
    if s == rev:
        return True
    return False


def getsession():
    if 'user' in session:
        return True
    return False


class History(Resource):

    def get(self):
        conn = lite.connect('Palindrome.db')
        c = conn.cursor()
        c.execute('SELECT * FROM palindromes ORDER BY id DESC LIMIT 10')
        rows = c.fetchall()

        result = []
        for row in rows:

            send = {'id': row[0], 'date': row[1], 'value': row[2], 'is_palindrome': row[3]}
            result.append(send)

        return jsonify(result)


class Delete(Resource):
    def delete(self, id):

        if getsession():
            con = lite.connect('Palindrome.db')
            with con:
                cur = con.cursor()
                cur.execute("""SELECT * FROM palindromes WHERE id = ?""", (id,))
                rows = cur.fetchone()
                if rows is not None:
                    cur.execute("""DELETE FROM palindromes WHERE id = ?""", (id,))
                    return {'status': "Success"}
                else:
                    return {'status': "Record does not exist"}
        else:
            return jsonify(Access="Access denied")


api.add_resource(History, '/palindrome/history')
api.add_resource(Delete, '/palindrome/<string:id>')
api.add_resource(Palindrome, '/palindrome/solve')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)
