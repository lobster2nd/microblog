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
            return {'id': obj.id, 'body': obj.body, 'author': obj.author, 'comments': obj.comments}
        if isinstance(obj, User):
            return {'_username': obj._username}
        if isinstance(obj, Comment):
            return {'id': obj.id, 'author': obj.author, 'twit_id': obj.twit_id, 'message': obj.message}
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
        twit_obj = Twit(twit_json['id'], twit_json['body'], twit_json['author'], twit_json['comments'])
        twit = json.dumps(twit_obj, cls=CustomJSONEncoder)
        twits.append(json.loads(twit))
        return jsonify({'status': 'success'}), 200
    except Exception:
        return jsonify({'status': 'error'}), 400


@app.route('/twit', methods=['GET'])
def read_twits():
    return jsonify({'twits': twits})


@app.route('/twit/<id>', methods=['GET'])
def read_twit(id: str):
    for twit in twits:
        if twit['id'] == id:
            return jsonify(twit)

    return jsonify({'status': 'error'}), 400


@app.route('/twit/<id>/comment', methods=['POST'])
def add_comment(id: str):
    try:
        comment_json = request.get_json()
        for twit in twits:
            if twit['id'] == id:
                # Create a new Comment object
                comment_obj = Comment(comment_json['id'], comment_json['author'], comment_json['message'], id)
                # Add the comment to the twit's comments list
                twit['comments'].append(json.loads(json.dumps(comment_obj, cls=CustomJSONEncoder)))
                return jsonify({'status': 'success'}), 200

        return jsonify({'status': 'error', 'message': 'Twit not found'}), 400
    except Exception:
        return jsonify({'status': 'error', 'message': 'Failed to add comment'}), 400


@app.route('/twit/<id>/<comment_id>', methods=['DELETE'])
def delete_comment(id: int, comment_id: str):
    for twit in twits:
        if twit['id'] == id:
            for comment in twit['comments']:
                if comment['id'] == comment_id:
                    twit['comments'].remove(comment)
                    return jsonify({'status': 'success'}), 200

    return jsonify({'status': 'error'}), 400


@app.route('/twit/<id>', methods=['PUT'])
def update_twit(id: str):
    comment_json = request.get_json()
    for twit in twits:
        if twit['id'] == id:
            twit['body'] = comment_json['body']
            twit['author'] = comment_json['author']
            return jsonify({'status': 'success'}), 200

    return jsonify({'status': 'error'}), 400


@app.route('/twit/<id>', methods=['DELETE'])
def delete_twit(id: str):
    for twit in twits:
        if twit['id'] == id:
            twits.remove(twit)
            return jsonify({'status': 'success'}), 200

    return jsonify({'status': 'error'}), 400


if __name__ == '__main__':
    app.run(debug=True)
