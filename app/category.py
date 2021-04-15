from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sebastiang1103.@localhost:3306/prueba_api'
app.config['SQALALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

class Categoria(db.Model):
    cat_id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
        
    def __init__(self,nombre,descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

db.create_all()            

class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'nombre', 'descripcion')    
        
categoria_schema = CategoriaSchema()

categorias_schema = CategoriaSchema(many=True)

@app.route('/categoria',methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)



@app.route('/categoria/<id>',methods=['GET'])
def get_categorias_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)


@app.route('/categoria',methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    
    nombre = data['nombre']
    descripcion = data['descripcion']

    nuevocategoria = Categoria(nombre,descripcion)
    
    db.session.add(nuevocategoria)
    db.session.commit()
    return categoria_schema.jsonify(nuevocategoria)

@app.route('/',methods=['GET'])
def index():
    return jsonify({'Mensaje': 'Bienvenido'})

if __name__=="__main__":
    app.run(debug=True)
