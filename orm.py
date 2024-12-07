from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Annotated

db = SQLAlchemy()


class Persons(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    lastname: Mapped[str] = mapped_column(String(30), nullable=False)  # Фамилия
    firstname: Mapped[str] = mapped_column(String(30), nullable=False)  # Имя
    middlename: Mapped[str] = mapped_column(String(30))  # Отчество


persons_id = Annotated[int, mapped_column(primary_key=True)]


class ParentChildRelationships(db.Model):
    parent_id: Mapped[persons_id] = mapped_column(
        ForeignKey("persons.id")
    )  # id - родителя
    child_id: Mapped[persons_id] = mapped_column(
        ForeignKey("persons.id")
    )  # id - ребенка


from typing import Dict

from flask import jsonify


def get_persons_with_parents():
    relationships = ParentChildRelationships.query.all()
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
