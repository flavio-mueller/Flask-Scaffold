#!/usr/bin/python
# coding=utf-8
import yaml

yaml_file = "scaffold/structure.yaml"


def generate_files(module, html, fields):
    # Generate Template Files
    try:
        new_file = open('templates/{}.html'.format(module), "w+")
        new_file.write("""
            {% extends "layout.html" %}
            {% block body %}""")
        new_file.write("""
            <fieldset>
            <form action={}_data method="post">""".format(module))
        for f in html:
            new_file.write(f)
        new_file.write("""

            <button type="submit" class="btn btn-success">Abschicken</button>
            <button type="reset" class="btn btn-danger">Reset</button>
            <small>Wichtig: Alle Felder mit * sind Pflichtfelder</small>
            </form>
            </fieldset>
            {% endblock %}
            """)
        new_file.close()

        f= open('templates/{}_data.html'.format(module), "w+")
        f.write("""
            {% extends "layout.html" %}
            {% block body %}""")
        f.write("""
            <p>Your data has been safed</p>
            {% endblock %}
            """)
        f.close()


        print "Wrote Html-files"
    except:
        print "An Error accured! Couldn't wirte Html-files"



    try:
        app = open('app.py', "a")
        app.write("@app.route('/{}')\n".format(module))
        app.write("def {}():\n".format(module))
        app.write("    return render_template('{}.html')\n\n\n".format(module))
        app.write("@app.route('/{}_data', methods=['POST'])\n".format(module))
        app.write("def {}_data():\n".format(module))
        app.write("    {}_formdata = {}_Model(request.form)\n".format(module, module))
        app.write("\n")
        app.write("    db.session.add({}_formdata)\n".format(module))
        app.write("    db.session.commit()\n")
        app.write("    return render_template('{}_data.html')\n\n".format(module))
        app.write("class {}_Model(db.Model):\n".format(module))
        app.write("    __tablename__ = '{}'\n".format(module))
        first = True
        for f in fields:
            field_name, field_type = f.split(':')
            field_type = field_type.title()
            if first:
                app.write("    {} = db.Column(db.{}, primary_key=True)\n".format(field_name, field_type))
                first = False
            else:
                app.write("    {} = db.Column(db.{}, unique=True)\n".format(field_name, field_type))
        app.write("\n\n")
        app.write("    def __init__(self, data):\n")
        app.write("        for key, value in data.iteritems():\n")
        first = True
        for f in fields:
            field_name, field_type = f.split(':')
            if first:
                app.write("            if key == '{}':\n".format(field_name))
                app.write("                self.{} = data['{}']\n".format(field_name, field_name))
                first = False
            else:
                app.write("            elif key == '{}':\n".format(field_name))
                app.write("                self.{} = data['{}']\n".format(field_name, field_name))

        app.write("\n\n")
        app.close()
        print "created Controller"
    except:
        print "couldnt write controller"


app = open("app.py", "w")
app.write("from flask import Flask, render_template, request\n")
app.write("from flask_sqlalchemy import SQLAlchemy\n")
app.write("app = Flask(__name__)\n")
app.write("app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flavio:flavio@localhost/flarecast'\n")
app.write("db = SQLAlchemy(app)\n")
app.write("db.init_app(app)\n\n\n")
app.close()

with open(yaml_file, "r") as file:
    yaml_data = yaml.load(file)


    for module, fields in yaml_data.items():

        # array for the html tags
        html = []
        #arry for the fields
        field_names = []

        for f in fields:
            field_name, field_type = f.split(':')

            if field_type == "string":
                html.append("""
                <div class="form-group">
                    <label for="{field}">{field}*</label>
                    <input type="text" class="form-control" id="{field}" name="{field}" placeholder="{field}">
                </div>""".format(field=field_name))

            elif field_type == "int":
                html.append("""
                <div class="form-group">
                    <label for="{field}">{field}*</label>
                    <input type="number" class="form-control" id="{field}" name="{field}" placeholder="{field}">
                </div>""".format(field=field_name))

            elif field_type == "double":
                html.append("""
                <div class="form-group">
                    <label for="{field}">{field}*</label>
                    <input type="number" class="form-control" id="{field}" name="{field}" placeholder="{field}">
                </div>""".format(field=field_name))

            elif field_type == "datetime":
                html.append("""
                <div class="form-group">
                    <label for="{field}">{field}*</label>
                    <input type="datetime" class="form-control" id="{field}" name="{field}" placeholder="{field}">
                </div>""".format(field=field_name))

            field_names.append(field_name)

        generate_files(module, html, fields)


app = open("app.py", "a")
app.write("if __name__ == '__main__':\n")
app.write("     app.run()")