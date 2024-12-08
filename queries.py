from os import listdir, path
from orm import db
from main import app


def _load_sql_file(file_path: str):
    with open(file_path, "r") as f:
        sql = f.read()

    with app.app_context():
        with db.engine.connect() as cn:
            cn.execute(sql)
            cn.commit()


queries_folder = path.join(path.curdir, "queries")

for file in listdir(queries_folder):
    if file.endswith(".sql"):
        file_path = path.join(queries_folder, file)
        _load_sql_file(file_path)
