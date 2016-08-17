from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flavio:flavio@localhost/flarecast'
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def homepage():
    return render_template('layout.html')

@app.route('/property_group')
def property_group():
    return render_template('property_group.html')


@app.route('/property_group_data', methods=['POST'])
def property_group_data():
    property_group_formdata = property_group_Model(request.form)

    db.session.add(property_group_formdata)
    db.session.commit()
    return render_template('property_group_data.html')

class property_group_Model(db.Model):
    __tablename__ = 'property_group'
    fc_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)
    nar = db.Column(db.BIGINT, unique=True)
    time_start = db.Column(db.DATETIME, unique=True)
    lat_hg = db.Column(db.FLOAT, unique=True)
    long_hg = db.Column(db.FLOAT, unique=True)
    long_carr = db.Column(db.FLOAT, unique=True)


    def __init__(self, data):
        for key, value in data.iteritems():
            if key == 'fc_id':
                self.fc_id = data['fc_id']
            elif key == 'name':
                self.name = data['name']
            elif key == 'nar':
                self.nar = data['nar']
            elif key == 'time_start':
                self.time_start = data['time_start']
            elif key == 'lat_hg':
                self.lat_hg = data['lat_hg']
            elif key == 'long_hg':
                self.long_hg = data['long_hg']
            elif key == 'long_carr':
                self.long_carr = data['long_carr']


@app.route('/property_type')
def property_type():
    return render_template('property_type.html')


@app.route('/property_type_data', methods=['POST'])
def property_type_data():
    property_type_formdata = property_type_Model(request.form)

    db.session.add(property_type_formdata)
    db.session.commit()
    return render_template('property_type_data.html')

class property_type_Model(db.Model):
    __tablename__ = 'property_type'
    name = db.Column(db.String, primary_key=True)
    version = db.Column(db.String, unique=True)
    type = db.Column(db.String, unique=True)
    json_schema = db.Column(db.String, unique=True)
    utype = db.Column(db.String, unique=True)
    ucd = db.Column(db.String, unique=True)
    unit = db.Column(db.String, unique=True)
    description = db.Column(db.String, unique=True)


    def __init__(self, data):
        for key, value in data.iteritems():
            if key == 'name':
                self.name = data['name']
            elif key == 'version':
                self.version = data['version']
            elif key == 'type':
                self.type = data['type']
            elif key == 'json_schema':
                self.json_schema = data['json_schema']
            elif key == 'utype':
                self.utype = data['utype']
            elif key == 'ucd':
                self.ucd = data['ucd']
            elif key == 'unit':
                self.unit = data['unit']
            elif key == 'description':
                self.description = data['description']

if __name__ == "__main__":
    app.run()


