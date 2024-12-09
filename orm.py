import os
from icecream import ic
from typing import Dict

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, ForeignKey, String, select, update, insert
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
    __tablename__ = "families_persons"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_family: Mapped[int] = mapped_column(ForeignKey("families.id"))  # id семьи
    id_person: Mapped[int] = mapped_column(
        ForeignKey("persons.id"), name="id_person"
    )  # id члена семьи

    @staticmethod
    def getFamilyPersonsAndRoots(id: int):
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
            )  # Все люди семьи

            ids = set(int(person["id"]) for person in persons)  # Их id

            relation = list(
                s.execute(
                    select(Parents_Children_Relationships).filter(
                        Parents_Children_Relationships.child_id.in_(ids)
                    )
                )
                .scalars()
                .all()
            )  # Отношения между членами семьи

            def findAllChildren(id: int):
                return [p.child_id for p in relation if p.parent_id == id]

            childrenIds = set(
                child.child_id for child in relation if child.child_id in ids
            )  # Id детей

            persons_without_parents = [
                person["id"] for person in persons if person["id"] not in childrenIds
            ]  # Люди без родителей - корни

            for i in range(len(persons)):
                persons[i]["childrenId"] = findAllChildren(
                    persons[i]["id"]
                )  # Добавляем детей

            return {"persons": persons, "roots": persons_without_parents}

    def putNewMember(id_person, id_family):
        try:
            with db.engine.connect() as cn:
                cn.execute(
                    insert(Families_Persons),
                    [{"id_family": id_family, "id_person": id_person}],
                )
                cn.commit()
        except Exception as e:
            ic(e)
            return False
        return True


class Persons(db.Model):  # Член семьи
    # __tablename__ = "persons"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    firstName: Mapped[str] = mapped_column(
        String(30), nullable=False, name="firstname"
    )  # Имя
    lastName: Mapped[str] = mapped_column(
        String(30), nullable=False, name="lastname"
    )  # Фамилия
    middleName: Mapped[str] = mapped_column(String(30), name="middlename")  # Отчество
    is_male: Mapped[bool] = mapped_column(Boolean)

    @staticmethod
    def updatePerson(id, per):
        try:
            with db.engine.connect() as cn:
                ic(cn.execute(update(Persons).where(Persons.id == id).values(**per)))
                cn.commit()
        except Exception as e:
            ic(e)
            return False
        return True

    def putPerson(per):
        try:
            with db.engine.connect() as cn:
                person = cn.execute(
                    insert(Persons).values(**per).returning(Persons)
                ).first()
                ic(person)
                cn.commit()
        except Exception as e:
            ic(e)
            return False, None
        return True, person

    def toJson(self):
        return {
            "id": self.id,
            "lastName": self.lastName,
            "firstName": self.firstName,
            "middleName": self.middleName,
            "is_male": self.is_male,
        }


persons_id = Annotated[int, mapped_column(primary_key=True)]


class Parents_Children_Relationships(db.Model):  # Отношение между Родителями и Детьми
    __tablename__ = "parents_children_relationships"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    parent_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))  # id - родителя
    child_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id"), name="child_id"
    )  # id - ребенка


def get_persons_with_parents():
    relationships = Parents_Children_Relationships.query.all()
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
