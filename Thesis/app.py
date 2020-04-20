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

        return jsonify(Access="Access denied")


class Palindrome(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        value = json_data['value']
        if isinstance(value, float):
            return {'Error': "Only String or Int Accepted"}

        conn = connection()
        c = conn.cursor()
        c.execute("""SELECT * FROM palindromes WHERE value = ?""", (value,))
        rows = c.fetchall()

        if rows is not None:
            for row in rows:
                return {'is_palindrome': row[3]}

        if not isinstance(value, str):
            temp = value
            n = value
            rev = 0
            while n > 0:
                dig = n % 10
                rev = rev * 10 + dig
                n = n // 10

            if temp == rev:
                DatabaseRequest(value, True)
                return {'is_palindrome': True}
            else:
                DatabaseRequest( value, False)
                return {'is_palindrome': False}

        ans = isPalindrome(value)
        if ans == 1:
            DatabaseRequest(value, True)
            return {'is_palindrome': True}
        else:
            DatabaseRequest(value, False)
            return {'is_palindrome': False}



def connection():
    return lite.connect('Palindrome.db')


def DatabaseRequest(value, is_palindrome):
    conn = connection()
    c = conn.cursor()
    c.execute("INSERT INTO palindromes(id, date, value, is_palindrome) VALUES(?,?,?,?)",
            (str(uuid.uuid4()), str(time.asctime(time.localtime(time.time()))), str(value), str(is_palindrome)))
    conn.commit()
    conn.close()


def reverse(s):
    return s[::-1]


def isPalindrome(s):
    rev = reverse(s)
    if s == rev:
        return True
    return False


def getSession():
    if 'user' in session:
        return True
    return False


class History(Resource):
    def get(self):
        conn = connection()
        c = conn.cursor()
        c.execute("SELECT * FROM palindromes")
        rows = c.fetchall()

        result = []
        i = 0
        for row in reversed(rows):
            if i == 10:
                break
            send = {'id': row[0], 'date': row[1], 'value': row[2], 'is_palindrome': row[3]}
            result.append(send)
            i = i + 1
        return jsonify(result)


class Delete(Resource):
    def delete(self, id):

        if getSession():
            conn = connection()
            c = conn.cursor()
            with conn:
                c.execute("""SELECT * FROM palindromes WHERE id = ?""", (id,))
                rows = c.fetchone()

                if rows is not None:
                    c.execute("""DELETE FROM palindromes WHERE id = ?""", (id,))
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
    c = connection()
    c.execute('CREATE TABLE IF NOT EXISTS palindromes(id TEXT,date TEXT,value TEXT,is_palindrome TEXT)')
    app.run(debug=True)
