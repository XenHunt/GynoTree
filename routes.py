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


@app.route("/person/<int:id>", methods=["GET", "POST", "DELETE"])
def up_get_person(id: int):
    if request.method == "GET":
        per = Persons.query.where(Persons.id == id).first()
        if isinstance(per, Persons):

            return ic(
                {
                    "person": ic(per.toJson()),
                    "parents": ic(Persons.getCurrentParents(per.id)),
                    "family": ic(Families_Persons.getFamilyByPersonId(per.id)),
                }
            )
        else:
            return {}
    elif request.method == "POST":
        if not request.json:
            return
        person = request.json["person"]
        family = request.json["family"]
        parents = request.json["parents"]

        per = Persons.query.where(Persons.id == id).first()

        if not isinstance(per, Persons):
            return
        if Persons.updatePerson(id, person):
            if Families_Persons.movePersonToNewFamily(id, family["id"]):
                if Persons.update_parents(id, parents):
                    return "All updated", 200
                return "Bad parents", 400
            return "Bad family", 400
        return "Bad payload", 400
    else:
        if Persons.deletePerson(id):
            return "Deleted", 200
        return "Bad id", 400
        


@app.route("/person", methods=["PUT"])
def put_person():
    if not request.json:
        return 404
    ic(request.json)
    person = request.json["person"]
    familyId = int(request.json["familyId"])

    res, person = Persons.putPerson(person)
    if res:  # Человек добавился успешнок
        if Families_Persons.putNewMember(
            person.id, familyId
        ):  # Связь между человеком и семье налажена
            return "Success", 200
        return "Bad family id", 400
    return "Bad person", 400


@app.route("/women", methods=["GET"])
def get_women():
    return Persons.getAllWomen()


@app.route("/men", methods=["GET"])
def get_men():
    return Persons.getAllMen()


@app.route("/person/<int:id>/parents", methods=["GET"])
def get_parents(id: int):
    return Persons.getCurrentParents(id)
