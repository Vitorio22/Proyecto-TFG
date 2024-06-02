from flask import Flask, request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_restful import Api

# Setup flask y MongoDB
app = Flask(__name__)
api = Api(app)
app.config['MONGO_URI'] = 'mongodb+srv://Victor:Erpele654321@cluster0.oixxsof.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(app.config['MONGO_URI'])
db = client['NostalgiaZone']
scores_blockAttack = db['scores_blockAttack']
scores_asteroids = db['scores_asteroids']
scores_tetris = db['scores_tetris']
mongo = PyMongo(app)

# Endpoint para guardar la puntuación Block Attack
@app.route('/save_score_blockAttack', methods=['POST'])
def save_score_blockAttack():
    player_name = request.json['nombre']
    score = request.json['puntuacion']
    
    # Guarda el nombre del jugador y la puntuación en la base de datos
    scores_blockAttack.insert_one({'nombre': player_name, 'puntuacion': score})
    
    return 'Puntuación guardada exitosamente'

# Endpoint para guardar la puntuación Asteroids
@app.route('/save_score_asteroids', methods=['POST'])
def save_score_asteroids():
    player_name = request.json['nombre']
    score = request.json['puntuacion']
    
    # Guarda el nombre del jugador y la puntuación en la base de datos
    scores_asteroids.insert_one({'nombre': player_name, 'puntuacion': score})
    
    return 'Puntuación guardada exitosamente'

# Endpoint para guardar la puntuación Tetris
@app.route('/save_score_tetris', methods=['POST'])
def save_score_tetris():
    player_name = request.json['nombre']
    score = request.json['puntuacion']
    
    # Guarda el nombre del jugador y la puntuación en la base de datos
    scores_tetris.insert_one({'nombre': player_name, 'puntuacion': score})
    
    return 'Puntuación guardada exitosamente'

# Endpoint para obtener las puntuaciones de Block Attack
@app.route('/get_score_blockAttack', methods=['GET'])
def get_score_blockAttack():
    # Obtiene las puntuaciones de la base de datos
    scores_blockAttack.find().sort('puntuacion', -1)
    
    score_list = []
    
    for score in scores_blockAttack.find():
        score_data = {
            'Nombre': score['nombre'],
            'Puntuacion': score['puntuacion']
        }
        score_list.append(score_data)
    
    response = {'scores': score_list}
    
    return response

# Endpoint para obtener las puntuaciones de Asteroids
@app.route('/get_score_asteroids', methods=['GET'])
def get_score_asteroids():
    # Obtiene las puntuaciones de la base de datos
    scores_asteroids.find().sort('puntuacion', -1)
    
    score_list = []
    
    for score in scores_asteroids.find():
        score_data = {
            'Nombre': score['nombre'],
            'Puntuacion': score['puntuacion']
        }
        score_list.append(score_data)
    
    response = {'scores': score_list}
    
    return response

# Endpoint para obtener las puntuaciones de Tetris
@app.route('/get_score_tetris', methods=['GET'])
def get_score_tetris():
    # Obtiene las puntuaciones de la base de datos
    scores_tetris.find().sort('puntuacion', -1)
    
    score_list = []
    
    for score in scores_tetris.find():
        score_data = {
            'Nombre': score['nombre'],
            'Puntuacion': score['puntuacion']
        }
        score_list.append(score_data)
    
    response = {'scores': score_list}
    
    return response