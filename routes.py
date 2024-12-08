from flask import render_template, request
from main import app
from orm import Families, Families_Persons, db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/family", methods=["GET", "POST"])
def get_families():
    if request.method == "GET":
        # for name in ["Ильинов", "Бобов", "Тамарский"]:
        #     with db.session() as sn:
        #         sn.execute(insert(Families).values(name=name))
        #         sn.commit()
        return Families.getFamilies()
    else:
        id = int(request.form["id"])

        return Families_Persons.getFamilyPersons(id)
