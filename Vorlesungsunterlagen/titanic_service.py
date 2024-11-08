from fastapi import FastAPI, HTTPException
import csv

app = FastAPI()


with open('../data/titanic.csv', 'r') as ifile:
    reader = csv.DictReader(ifile)
    data = [row for row in reader if int(row['PassengerId']) < 10]


@app.get('/passenger/{row}')
def get_passengers(row: int):
    try:
        return data[row]
    except IndexError:
        raise HTTPException(404)
