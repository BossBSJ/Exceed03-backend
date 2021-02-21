import time
from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_user:1q2w3e4r@158.108.182.0:2277/exceed_backend'

mongo = PyMongo(app)

myCollection = mongo.db.g3

@app.route('/create', methods=['POST'])
def insert_one():
    data = request.json
    ts = time.time()
    if (data["avaiable"]):
        # update last record
        query = { 
            "parkid": data["parkid"],
            "end_ts": None
        }
        update = {
            "$set": {
                "end_ts": time.time()
            }
        }
        myCollection.update_one(query, update)
    else:
        # insert new
        del data["avaiable"]
        data["start_ts"] = time.time()
        myCollection.insert_one(data)
    return {'result': 'successfully'}

@app.route('/call', methods=['GET'])
def search():
    parkid = request.args.get("parkid")
    filt = {"parkid": int(parkid)}
    query = myCollection.find(filt)
    res=[]
    for ele in query:
        if ("end_ts" not in ele):
            continue
        res.append({
            "parkid": ele["parkid"],
            "start_ts": ele["start_ts"],
            "end_ts": ele["end_ts"]
        })
    return {"result": res }

@app.route('/currentstatus', methods=['GET'])
def showCurrent():
    output = []
    
    for i in range(4):
        parkid = i+1
        flit = {"parkid": parkid, "end_ts": None}
        query = myCollection.find_one(flit)
    
        if (query != None):
            # park is not free
            output.append({
                "parkid": parkid,
                "available": False,
                "start_ts": query["start_ts"]
            })
        else:
            #Free
            output.append({
                "parkid": parkid,
                "available": True,
            })

    return {"result": output}


@app.route('/test', methods=['GET'])
def test():
    return {'ok': 1}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000',debug=True)
