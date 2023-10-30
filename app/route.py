from app import app, response
from app.controller import DosenContr
from app.controller import UserContr
from flask import request
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

@app.route("/")
def index():
    return 'hello flask app'

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return response.success(current_user, 'Sukses')

@app.route('/dosen', methods=['GET', 'POST'])
@jwt_required()
def dosens():
    if request.method == 'GET':
        return DosenContr.index()
    elif request.method == 'POST':
        return DosenContr.save()
    
@app.route('/createadmin', methods=['POST'])
def admins():
    if request.method == 'POST':
        return UserContr.createAdmin()

@app.route('/dosen/<id>', methods=['GET', 'PUT', 'DELETE'])
def dosenDetail(id):
    if request.method == 'GET':
        return DosenContr.detail(id)
    elif request.method == 'PUT':
        return DosenContr.ubah(id)
    elif request.method == 'DELETE':
        return DosenContr.hapus(id)

@app.route('/api/dosen/page', methods=['GET'])
def paginations():
    return DosenContr.paginate()

@app.route('/login', methods=['POST'])
def logins():
    return UserContr.login()

@app.route('/file-upload', methods=['POST'])
def uploads():
    return UserContr.upload()