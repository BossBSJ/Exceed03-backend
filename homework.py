from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_user:1q2w3e4r@158.108.182.0:2277/exceed_backend'
mongo = PyMongo(app)

myCollection = mongo.db.twitter

@app.route('/store', methods=['POST'])
def insert_one():
    data = request.json
    myInsert ={
            "Brand":data["Brand"],
            "Product_name":data["Product_name"],
            "Product_description":data["Product_description"]
    }
    myCollection.insert_one(data)
    return {'result': "Created successfully"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='50002', debug=True)
