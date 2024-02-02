from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://sanachouhan26:QJ29Buu9TglZ8186@cluster0stard.dfynme3.mongodb.net/')
db = client.dbhomework

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0,
        'thumbs_up': 0,  # New field for upvotes
        'thumbs_down': 0  # New field for downvotes
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/delete", methods=["POST"])
def delete_bucket():
    num_receive = request.form['num_give']
    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'Delete done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

@app.route("/thumbs/up", methods=["POST"])
def thumbs_up():
    num_receive = request.form['num_give']
    print(request.form)
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$inc': {'thumbs_up': 1}}
    )
    return jsonify({'msg': f'Thumbs up received for bucket {num_receive}'})

@app.route("/thumbs/down", methods=["POST"])
def thumbs_down():
    num_receive = request.form['num_give']
    print(request.form)
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$inc': {'thumbs_down': 1}}
    )
    return jsonify({'msg': f'Thumbs down received for bucket {num_receive}'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
