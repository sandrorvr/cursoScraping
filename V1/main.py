import json
from ExtactPages import ExtractPages
from DataBaseConection import DB

with open('departments.json') as file:
    DEPARTMENTSJSON = json.load(file)
    
extrator = ExtractPages()
db = DB()
db.createDB()

for key in DEPARTMENTSJSON.keys():
    for pg in range(1,2):
        books = extrator.getBooksByDepartmentByPage(DEPARTMENTSJSON[key], pag=pg)
        for bk in books:
          data =(
                  bk.getIdBook(),
                  bk.extractTitle(),
                  ','.join(bk.extractAuthors()),
                  bk.extractPrice(),
                 )
          try:
            db.insertData(data)
            print({
                "status":"ok",
                "department":DEPARTMENTSJSON[key],
                "pag":pg,
                "data":data
                })
          except Exception as e:
            print({
                "status":e.args,
                "department":DEPARTMENTSJSON[key],
                "pag":pg,
                "data":data
                })