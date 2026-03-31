from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import os

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI", "mongodb://database:27017/")
client = MongoClient(mongo_uri)
db = client.test_db
collection = db.items

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        collection.insert_one({'content': content})
        return redirect('/')
    
    items = collection.find()
    return render_template('index.html', items=items)

@app.route('/update/<id>', methods=['POST'])
def update_item(id):
    from bson.objectid import ObjectId
    new_content = request.form['content']
    collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': {'content': new_content}}
    )
    return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def delete_item(id):
    from bson.objectid import ObjectId
    collection.delete_one({'_id': ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

