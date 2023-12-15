from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Ruta para crear un usuario
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    new_user = User(username=data['username'], email=data['email'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to create user'}), 500
    finally:
        db.session.close()

# Ruta para obtener un usuario por su ID
@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'username': user.username, 'email': user.email}), 200
    return jsonify({'message': 'User not found'}), 404

# Ruta para actualizar un usuario por su ID
@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)

    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user'}), 500
    finally:
        db.session.close()

# Ruta para eliminar un usuario por su ID
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete user'}), 500
    finally:
        db.session.close()

# Ruta para obtener todos los usuarios
@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({'id': user.id, 'username': user.username, 'email': user.email})
    return jsonify({'users': user_list}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)