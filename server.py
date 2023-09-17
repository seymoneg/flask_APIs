from flask import Flask, make_response, request
app = Flask(__name__)

# hard coded data generated with Mockaroo
data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]


@app.route("/")
def index():
    return "hello world"

# create a new method named no_content
@app.route('/no_content')
def no_content():
    return ({"message": "No content found"}, 204)

# send custom HTTP response code using make_response()
@app.route('/exp')
def index_explicit():
    resp = make_response({"message": "hello world"})
    resp.status_code = 200
    return resp

# confirm that data has been copied to the file
@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

# search for the first name of a client
@app.route('/name_search')
def name_search():
    # look for the first name of the client
    query = request.args.get("q")

    if not query:
        return {"error message": "input parameter missing"}, 422

    # fetch resource from database
    for person in data:
        if query.lower() in person["first_name"].lower():
            return person

    return {"error message": "Person not found"}, 404

# create GET /count endpoint that returns total numer of people in data list
@app.route('/count')
def count():
    try:
        count = 0
        for i in data:
            count += 1
        
        return {"data count": count}, 200
    except NameError:
            return {"message": "data not defined"}, 500

# create GET /person/id endpoint to ask for a person by id
@app.route("/person/<uuid:id>")
def find_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            return person
    return {"message": "person not found"}, 404

# create DELETE /person/id endpoint to delete a person from the database
@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            data.remove(person)
            return {"message":"id of person deleted"}, 200
    return {"message": "person not found"}, 404

# create POST /person/id endpoint to create a new person and add to the database
@app.route('/person', methods=['POST'])
def add_by_uuid():
    new_person = request.json

    if not new_person:
        return {"message":"Invalid input parameter"}, 422
        try:
            data.append(new_person)
        except NameError:
            return {"message": "data not defined"}, 500

    return {"message": f"{new_person['id']}"}, 200

# create custom resource not found
@app.errorhandler(404)
def api_not_found(error):
    return {"message": "API not found"}, 404
