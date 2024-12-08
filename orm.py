from icecream import ic
from typing import Dict

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Annotated

db = SQLAlchemy()


class Families(db.Model):  # Семьи
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )  # id семьи
    name: Mapped[str] = mapped_column(String(30), nullable=False)  # имя семьи

    @staticmethod
    def getFamilies():
        with db.session() as s:
            families = s.execute(select(Families)).scalars().all()
            return list([family.toJson() for family in families])

    def toJson(self):
        return {"id": self.id, "name": self.name}


class Families_Persons(db.Model):  # Связь между семьями и их членами
    id_family: Mapped[int] = mapped_column(primary_key=True)  # id семьи
    id_person: Mapped[int] = mapped_column(primary_key=True)  # id члена семьи

    @staticmethod
    def getFamilyPersons(id: int):
        with db.session() as s:
            persons = list(
                map(
                    lambda per: per.toJson(),
                    s.execute(
                        select(Persons)
                        .join(
                            Families_Persons, Families_Persons.id_person == Persons.id
                        )
                        .where(Families_Persons.id_family == id)
                    )
                    .scalars()
                    .all(),
                )
            )

            ids = set(int(person["id"]) for person in persons)

            roots = s.execute(select(Persons))
            relation = list(
                s.execute(
                    select(ParentsChildrenRelationships).filter(
                        ParentsChildrenRelationships.child_id.in_(ids)
                    )
                )
                .scalars()
                .all()
            )

            def findAllChildren(id: int):
                return [p.child_id for p in relation if p.parent_id == id]

            childrenIds = set(
                child.child_id for child in relation if child.child_id in ids
            )

            persons_without_parents = []

            persons_without_parents

            for i in range(len(persons)):
                persons[i]["childrenId"] = findAllChildren(persons[i].id)

            return persons


class Persons(db.Model):  # Член семьи
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    lastName: Mapped[str] = mapped_column(String(30), nullable=False)  # Фамилия
    firstName: Mapped[str] = mapped_column(String(30), nullable=False)  # Имя
    middleName: Mapped[str] = mapped_column(String(30))  # Отчество
    is_male: Mapped[bool] = mapped_column(Boolean)

    def toJson(self):
        return {
            "id": self.id,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "middleName": self.middleName,
            "is_male": self.is_male,
        }


persons_id = Annotated[int, mapped_column(primary_key=True)]


class ParentsChildrenRelationships(db.Model):  # Отношение между Родителями и Детьми
    parent_id: Mapped[persons_id] = mapped_column(
        ForeignKey("persons.id")
    )  # id - родителя
    child_id: Mapped[persons_id] = mapped_column(
        ForeignKey("persons.id")
    )  # id - ребенка


def get_persons_with_parents():
    relationships = ParentsChildrenRelationships.query.all()
    persons_dict: Dict[int, Dict] = {}

    for relationship in relationships:
        child_id = relationship.child_id
        parent_id = relationship.parent_id

        if child_id not in persons_dict:
            child = Persons.query.get(child_id)
            if child:
                persons_dict[child_id] = {
                    "id": child.id,
                    "firstname": child.firstname,
                    "lastname": child.lastname,
                    "middlename": child.middlename,
                    "parent_ids": [],
                }

        if parent_id not in persons_dict[child_id]["parent_ids"]:
            persons_dict[child_id]["parent_ids"].append(parent_id)

    return jsonify(list(persons_dict.values()))
