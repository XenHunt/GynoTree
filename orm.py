from typing_extensions import Annotated
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String

db = SQLAlchemy()


class Persons(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    lastname: Mapped[str] = mapped_column(String(30), nullable=False)  # Фамилия
    firstname: Mapped[str] = mapped_column(String(30), nullable=False)  # Имя
    middlename: Mapped[str] = mapped_column(String(30))  # Отчество


persons_id = Annotated[int, mapped_column(primary_key=True)]


class ParentChildRelationships(db.Model):
    parent_id: Mapped[persons_id] = mapped_column(ForeignKey("persons.id"))
    child_id: Mapped[persons_id] = mapped_column(ForeignKey("persons.id"))
