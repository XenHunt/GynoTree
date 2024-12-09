from flask import render_template, request
from main import app
from orm import Families, Families_Persons, Persons
from icecream import ic


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
        ic()
        # ic(request.json)
        if not request.json:
            return
        id = int(request.json["id"])

        return Families_Persons.getFamilyPersonsAndRoots(id)


@app.route("/person/<int:id>", methods=["GET", "UPDATE"])
def up_get_person(id: int):
    if request.method == "GET":
        per = Persons.query.where(Persons.id == id).first()
        if isinstance(per, Persons):
            return per.toJson()
        else:
            return {}
    else:
        if not request.json:
            return
        person = request.json["person"]

        per = Persons.query.where(Persons.id == id).first()

        if not isinstance(per, Persons):
            return
        if Persons.updatePerson(id, person):
            return "Update managed", 200
        return "Bad payload", 400


@app.route("/person", methods=["PUT"])
def put_person():
    if not request.json:
        return 404
    ic(request.json)
    person = request.json["person"]
    familyId = int(request.json["familyId"])

    res, person = Persons.putPerson(person)
    if res:
        if Families_Persons.putNewMember(person.id, familyId):
            return "Success", 200
        return "Bad family id", 400
    return "Bad person", 400
