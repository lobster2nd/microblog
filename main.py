import json

from flask import Flask, jsonify, request

from model.twit import Twit
from model.user import User
from model.comment import Comment


twits = []

app = Flask(__name__)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return {'uid': obj.uid, 'body': obj.body, 'author': obj.author, 'comments': obj.comments}
        if isinstance(obj, User):
            return {'_username': obj._username}
        if isinstance(obj, Comment):
            return {'uid': obj.uid, 'author': obj.author, 'twit_id': obj.twit_id, 'message': obj.message}
        else:
            return super().default(obj)


app.json_encoder = CustomJSONEncoder


@app.route('/ping')
def ping():
    return jsonify({'response': 'pong'})


@app.route('/twit', methods=['POST'])
def create_twit():
    try:
        twit_json = request.get_json()
        twit_obj = Twit(twit_json['uid'], twit_json['body'], twit_json['author'], twit_json['comments'])
        twit = json.dumps(twit_obj, cls=CustomJSONEncoder)
        twits.append(json.loads(twit))
        return jsonify({'status': 'success'}), 200
    except Exception:
        return jsonify({'status': 'error'}), 400


@app.route('/twit', methods=['GET'])
def read_twits():
    return jsonify({'twits': twits})


@app.route('/twit/<uid>', methods=['GET'])
def read_twit(uid: str):
    for twit in twits:
        if twit['uid'] == uid:
            return jsonify(twit)

    return jsonify({'status': 'error'}), 400


@app.route('/twit/<uid>/comment', methods=['POST'])
def add_comment(uid: str):
    try:
        comment_json = request.get_json()
        for twit in twits:
            if twit['uid'] == uid:
                # Create a new Comment object
                comment_obj = Comment(comment_json['uid'], comment_json['author'], comment_json['message'], uid)
                # Add the comment to the twit's comments list
                twit['comments'].append(json.loads(json.dumps(comment_obj, cls=CustomJSONEncoder)))
                return jsonify({'status': 'success'}), 200

        return jsonify({'status': 'error', 'message': 'Twit not found'}), 400
    except Exception:
        return jsonify({'status': 'error', 'message': 'Failed to add comment'}), 400


@app.route('/twit/<uid>/<comment_id>', methods=['DELETE'])
def delete_comment(uid: int, comment_id: str):
    for twit in twits:
        if twit['uid'] == uid:
            for comment in twit['comments']:
                if comment['uid'] == comment_id:
                    twit['comments'].remove(comment)
                    return jsonify({'status': 'success'}), 200

    return jsonify({'status': 'error'}), 400


@app.route('/twit/<uid>', methods=['PUT'])
def update_twit(uid: str):
    comment_json = request.get_json()
    for twit in twits:
        if twit['uid'] == uid:
            twit['body'] = comment_json['body']
            twit['author'] = comment_json['author']
            return jsonify({'status': 'success'}), 200

    return jsonify({'status': 'error'}), 400


@app.route('/twit/<uid>', methods=['DELETE'])
def delete_twit(uid: str):
    for twit in twits:
        if twit['uid'] == uid:
            twits.remove(twit)
            return jsonify({'status': 'success'}), 200

    return jsonify({'status': 'error'}), 400


if __name__ == '__main__':
    app.run(debug=True)
