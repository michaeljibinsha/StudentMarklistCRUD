from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb+srv://michaeljibinsha:aaR2B10KJmdk3RIi@cluster0.tak3gnx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["StudentDB"]
collection = db["marks"]

# Homepage - List
@app.route('/')
def index():
    students = collection.find()
    return render_template('index.html', students=students)

# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        student = {
            "name": request.form['name'],
            "roll": request.form['roll'],
            "mark": request.form['mark']
        }
        collection.insert_one(student)
        return redirect('/')
    return render_template('add.html')

# Update Student
@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    student = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        updated_data = {
            "name": request.form['name'],
            "roll": request.form['roll'],
            "mark": request.form['mark']
        }
        collection.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
        return redirect('/')
    return render_template('update.html', student=student)

# Delete Student
@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
