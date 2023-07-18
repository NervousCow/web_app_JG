#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para administrar la base de datos de registro
de pulsaciones de personas
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inovecode.com"
__version__ = "1.1"


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
db = SQLAlchemy()

class LiveWeight(db.Model):
    __tablename__ = "live_weight"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    id_number = db.Column(db.Integer)
    farm = db.Column(db.String)
    category = db.Column(db.String)
    weight = db.Column(db.Integer)
    
    def __repr__(self):
        return f"El animal con caravana {self.id_number} registra un peso de {self.weight}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(time, id_number, establecimiento, categoria, peso):
    # Crear un nuevo registro de pulsaciones
    peso = LiveWeight(time=time, id_number=id_number, farm=establecimiento, category=categoria, weight=peso)

    # Agregar el registro de pulsaciones a la DB
    db.session.add(peso)
    db.session.commit()


def report(limit=0, offset=0):
    json_result_list = []

    # Obtener el ultimo registor de cada paciente
    # y ademas la cantidad (count) de registros por paciente
    # Esta forma de realizar el count es más avanzada pero más óptima
    # porque de lo contrario debería realizar una query + count  por persona
    # with_entities --> especificamos qué queremos que devuelva la query,
    # por defecto retorna un objeto HeartRate, nosotros estamos solicitando
    # que además devuelva la cantidad de veces que se repite cada nombre
    query = db.session.query(LiveWeight).with_entities(LiveWeight, db.func.count(LiveWeight.id_number))

    # Agrupamos por paciente (name) para que solo devuelva
    # un valor por paciente
    query = query.group_by(LiveWeight.id_number)

    # Ordenamos por fecha para obtener el ultimo registro
    query = query.order_by(LiveWeight.time)

    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    for result in query:
        peso = result[0]
        cantidad = result[1]
        json_result = {}
        json_result['time'] = peso.time.strftime("%Y-%m-%d %H:%M:%S.%f")
        json_result['id_number'] = peso.id_number
        json_result['farm'] = peso.farm
        json_result['categoria'] = peso.category
        json_result['last_weight'] = peso.weight
        json_result['records'] = cantidad
        json_result_list.append(json_result)

    return json_result_list


def chart(id_number):
    # Obtener los últimos 250 registros del paciente
    # ordenado por fecha, obteniedo los últimos 250 registros
    query = db.session.query(LiveWeight).filter(LiveWeight.id_number == id_number).order_by(LiveWeight.time.desc())
    query = query.limit(25)
    query_results = query.all()

    if query_results is None or len(query_results) == 0:
        # No data register
        # Bug a proposito dejado para poner a prueba el traceback
        # ya que el sistema espera una tupla
        return []

    # De los resultados obtenidos tomamos el tiempo y las puslaciones pero
    # en el orden inverso, para tener del más viejo a la más nuevo registro
    time = [x.time.strftime("%Y-%m-%d %H:%M:%S.%f") for x in reversed(query_results)]
    peso = [x.weight for x in reversed(query_results)]

    return time, peso

def chart_1(categoria):
    # Obtener los ultimos pesos individuales por categoria
    # query = db.session.query(LiveWeight).filter(LiveWeight.category == categoria)
    # results = query.all()

    subquery = db.session.query(
        LiveWeight.id_number,
        func.max(LiveWeight.time).label('max_time')
    ).filter(LiveWeight.category == categoria).group_by(LiveWeight.id_number).subquery()

    query = db.session.query(LiveWeight).join(
        subquery,
        (LiveWeight.id_number == subquery.c.id_number) &
        (LiveWeight.time == subquery.c.max_time)
    )

    result = query.all()

    time = [x.time.strftime("%Y-%m-%d %H:%M:%S") for x in result]
    peso = [x.weight for x in result]

    return time, peso