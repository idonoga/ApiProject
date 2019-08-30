from flask import Flask, request, render_template
from flask import jsonify
from flask_restful import Resource, Api, reqparse
import pymysql


def connect():
    con = pymysql.connect('users-mysql', 'root', 'password', 'users')
    return (con)


app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    return render_template('Homepage.html')


class ListUsers(Resource):
    def get(self):
        con = connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tbl_user")
        rows = cursor.fetchall()
        con.close()
        return jsonify(rows)


api.add_resource(ListUsers, '/ListUsers')


class ListSpecificUser(Resource):
    def get(self, user_id):
        con = connect()
        cursor = con.cursor()
        sql = "SELECT * FROM tbl_user WHERE user_id = %s"
        values = user_id
        cursor.execute(sql, values)
        rows = cursor.fetchall()
        con.close()
        return jsonify(rows)


api.add_resource(ListSpecificUser, '/ListUsers/<user_id>')

class AddUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user-id', type=int, location='json')
        parser.add_argument('user-name', location='json')
        parser.add_argument('user-email', location='json')
        parser.add_argument('user-password', location='json')
        args = parser.parse_args()
        con = connect()
        cursor = con.cursor()
        sql = "INSERT INTO tbl_user (user_id, user_name, user_email, user_password) VALUES (%s, %s, %s, %s)"
        values = (args.get('user-id'), args.get('user-name'), args.get('user-email'), args.get('user-password'))
        cursor.execute(sql,values)
        con.commit()
        con.close()
        return args

    def get(self):
        return "Use Post Method"


api.add_resource(AddUser, '/AddUser')

class ModifyUser(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user-id', type=int, location='json')
        parser.add_argument('user-name',location='json')
        parser.add_argument('user-email', location='json')
        parser.add_argument('user-password', location='json')
        args = parser.parse_args()
        con = connect()
        cursor = con.cursor()
        sql = "UPDATE tbl_user SET user_name = %s, user_email = %s, user_password = %s WHERE user_id = %s"
        values = (args.get('user-name'), args.get('user-email'), args.get('user-password'), args.get('user-id'))
        cursor.execute(sql, values)
        con.commit()
        con.close()
        return "User Changed Successfully"


api.add_resource(ModifyUser, '/ModifyUser')

class DeleteUser(Resource):
    def delete(self, user_id):
        con = connect()
        cursor = con.cursor()
        sql = "DELETE FROM tbl_user WHERE user_id = %s"
        values = (user_id)
        cursor.execute(sql,values)
        deleted_count = cursor.rowcount
        print(deleted_count)
        if deleted_count == 0:
            return "There is no such user"
        else:
            con.commit()
            con.close()
            return "User Deleted Successfully"


api.add_resource(DeleteUser, '/DeleteUser/<user_id>')



if __name__ == '__main__':
    app.run(host="0.0.0.0")