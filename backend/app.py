#-*- encoding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import copy
import random
import base64
import pymongo

app = Flask(__name__)
CORS(app, supports_credentials=True)


client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['face']
figure_meta = db['figure']
#  path face times
score_col = db['score']
# id path score 0 error 1 up 2 down 3 left 4 right

path_dict = dict()
prev_dict = dict()

def generate_id():
	return ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 10))

def get_figure():
	for x in figure_meta.find().sort('times').limit(1):
		for y in figure_meta.aggregate([{ '$match': {'times': x['times']}}, { '$sample': {'size': 1}} ]):
			return y
	return None

def update(fid, score):
	for x in score_col.find({'id': fid}):
		score_col.update_one({'id': fid}, {"$set": {'score': score}})
		return
	path = path_dict[fid]
	for x in figure_meta.find({'path': path}):
		figure_meta.update_one({'path': path}, {"$set": {'times': int(x['times'] + 1)}})
	score_col.insert_one({'id': fid, 'path': path, 'score': score})


def get_image_stream(path):
	stream = ''
	with open(path, 'rb') as f:
		stream = base64.b64encode(f.read())
	return stream

@app.route('/image', methods = ['POST'])
def get_image():
	fid = request.json['id']
	return get_image_stream(path_dict[fid])

@app.route('/next', methods = ['POST'])
def get_next():
	fid = request.json['id']
	figure = get_figure()
	if figure is None:
		return jsonify({})

	new_id = generate_id()
	path_dict[new_id] = figure['path']
	prev_dict[new_id] = fid

	return jsonify({'id': new_id})

@app.route('/back', methods = ['POST'])
def go_back():
	fid = request.json['id']
	if prev_dict[fid] == 'null':
		return jsonify({'id': fid})
	return jsonify({'id': prev_dict[fid]})

@app.route('/score', methods = ['POST'])
def update_score():
	fid = request.json['id']
	score = int(request.json['score'])
	update(fid, score)
	return jsonify({})

if __name__ == '__main__':
	app.run(host='0.0.0.0')
