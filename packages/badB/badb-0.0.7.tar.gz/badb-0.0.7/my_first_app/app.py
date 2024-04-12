from flask import Flask, jsonify, request, session, redirect, url_for, render_template 
from werkzeug.security import generate_password_hash, check_password_hash 
import sqlite3 
import json
from Models.user import User
from Models.post import Post
from Models.project import Project

app = Flask(__name__) 
app.secret_key = 'my_secret' 
DB_NAME = 'my_first_app.db' 

#Initialize database 
def init_db():
	conn = sqlite3.connect(DB_NAME) 
	c = conn.cursor() 
	c.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, age INT, gender TEXT, password TEXT NOT NULL)''') 
	c.execute('''CREATE TABLE IF NOT EXISTS post (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, author_name TEXT, author_id INT, keywords TEXT)''') 
	c.execute('''CREATE TABLE IF NOT EXISTS project (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, start_date TEXT, end_date TEXT, isCurrentlyWorking BOOLEAN, category TEXT)''') 
	conn.commit() 
	conn.close() 

#Authentication decorator 
def login_required(f): 
	def decorated_function(*args, **kwargs):
		if 'email' not in session:
			return jsonify({'message': 'Access denied to this route'})
		return f(*args, **kwargs)
	decorated_function.__name__ = f.__name__
	return decorated_function 

#Login a User
@app.route("/login", methods=["POST"])
def login():
	data = request.get_json()
	email = data.get('email')
	password = data.get('password')

	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	c.execute('SELECT email, password FROM user WHERE email = ?', (email,))
	user = c.fetchone()
	conn.close()

	if user and check_password_hash(user[1], password):
		session['email'] = user[0]
		return jsonify({'message': 'Login successful'}), 200
	else:
		return jsonify({'message': 'Invalid username or password'}), 401

#Route for GET user
@app.route('/user', methods=['GET'])
def get_user():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	c.execute('SELECT * FROM user')
	user= [User(*row) for row in c.fetchall()]
	conn.close()
	user_json = []
	for i in user:
		user_json.append({
			'id': i._id,
			'id': i._id,
			'name': i._name,
			'email': i._email,
			'age': i._age,
			'gender': i._gender,
			'password': i._password
		})
	return jsonify(user_json)

#Route for POST user
@app.route('/user', methods=['POST'])
def add_user():
	data = request.get_json()
	id = data.get('id')
	name = data.get('name')
	email = data.get('email')
	age = data.get('age')
	gender = data.get('gender')
	password = data.get('password')
	password = generate_password_hash(data.get('password'))
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		c.execute('INSERT INTO user (id, name, email, age, gender, password) VALUES (?, ?, ?, ?, ?, ?)', (id, name, email, age, gender, password))
		conn.commit()
		response = jsonify({'message': 'user added successfully'}), 201
	except sqlite3.IntegrityError as e:
		print('Invalid Data entry', e)
		response = jsonify({'message': 'Invalid Data Entry or Data already exists.'}), 400
	finally:
		conn.close()

	return response

# Route for PUT user
@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
	data = request.get_json()
	id = data.get('id')
	name = data.get('name')
	email = data.get('email')
	age = data.get('age')
	gender = data.get('gender')
	password = data.get('password')

	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		c.execute('UPDATE user SET id = ?, name = ?, email = ?, age = ?, gender = ?, password = ? WHERE id = ?', (id, name, email, age, gender, password, user_id))
		conn.commit()
		response = jsonify({'message': 'user updated successfully'}), 201
	except sqlite3.IntegrityError as e:
		print('Invalid Data entry', e)
		response = jsonify({'message': 'Invalid Data Entry or Data already exists.'}), 400
	finally:
		conn.close()

	return response

# Route for DELETE user
@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	c.execute('DELETE FROM user WHERE id = ?', (user_id,))
	conn.commit()
	conn.close()

	return jsonify({'message': 'user deleted successfully'}), 201

#Route for GET post
@app.route('/post', methods=['GET'])
def get_post():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	c.execute('SELECT * FROM post')
	post= [Post(*row) for row in c.fetchall()]
	conn.close()
	post_json = []
	for i in post:
		post_json.append({
			'id': i._id,
			'id': i._id,
			'title': i._title,
			'content': i._content,
			'author_name': i._author_name,
			'author_id': i._author_id,
			'keywords': i._keywords
		})
	return jsonify(post_json)

#Route for POST post
@app.route('/post', methods=['POST'])
@login_required
def add_post():
	data = request.get_json()
	id = data.get('id')
	title = data.get('title')
	content = data.get('content')
	author_name = data.get('author_name')
	author_id = data.get('author_id')
	keywords = data.get('keywords')
	password = generate_password_hash(data.get('password'))
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		c.execute('INSERT INTO post (id, title, content, author_name, author_id, keywords) VALUES (?, ?, ?, ?, ?, ?)', (id, title, content, author_name, author_id, keywords))
		conn.commit()
		response = jsonify({'message': 'post added successfully'}), 201
	except sqlite3.IntegrityError as e:
		print('Invalid Data entry', e)
		response = jsonify({'message': 'Invalid Data Entry or Data already exists.'}), 400
	finally:
		conn.close()

	return response

# Route for PUT post
@app.route('/post/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
	data = request.get_json()
	id = data.get('id')
	title = data.get('title')
	content = data.get('content')
	author_name = data.get('author_name')
	author_id = data.get('author_id')
	keywords = data.get('keywords')

	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		c.execute('UPDATE post SET id = ?, title = ?, content = ?, author_name = ?, author_id = ?, keywords = ? WHERE id = ?', (id, title, content, author_name, author_id, keywords, post_id))
		conn.commit()
		response = jsonify({'message': 'post updated successfully'}), 201
	except sqlite3.IntegrityError as e:
		print('Invalid Data entry', e)
		response = jsonify({'message': 'Invalid Data Entry or Data already exists.'}), 400
	finally:
		conn.close()

	return response

# Route for DELETE post
@app.route('/post/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	c.execute('DELETE FROM post WHERE id = ?', (post_id,))
	conn.commit()
	conn.close()

	return jsonify({'message': 'post deleted successfully'}), 201

#Route for GET project
@app.route('/project', methods=['GET'])
def get_project():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	c.execute('SELECT * FROM project')
	project= [Project(*row) for row in c.fetchall()]
	conn.close()
	project_json = []
	for i in project:
		project_json.append({
			'id': i._id,
			'id': i._id,
			'title': i._title,
			'content': i._content,
			'start_date': i._start_date,
			'end_date': i._end_date,
			'isCurrentlyWorking': i._isCurrentlyWorking,
			'category': i._category
		})
	return jsonify(project_json)

#Route for POST project
@app.route('/project', methods=['POST'])
@login_required
def add_project():
	data = request.get_json()
	id = data.get('id')
	title = data.get('title')
	content = data.get('content')
	start_date = data.get('start_date')
	end_date = data.get('end_date')
	isCurrentlyWorking = data.get('isCurrentlyWorking')
	category = data.get('category')
	password = generate_password_hash(data.get('password'))
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		c.execute('INSERT INTO project (id, title, content, start_date, end_date, isCurrentlyWorking, category) VALUES (?, ?, ?, ?, ?, ?, ?)', (id, title, content, start_date, end_date, isCurrentlyWorking, category))
		conn.commit()
		response = jsonify({'message': 'project added successfully'}), 201
	except sqlite3.IntegrityError as e:
		print('Invalid Data entry', e)
		response = jsonify({'message': 'Invalid Data Entry or Data already exists.'}), 400
	finally:
		conn.close()

	return response

# Route for PUT project
@app.route('/project/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
	data = request.get_json()
	id = data.get('id')
	title = data.get('title')
	content = data.get('content')
	start_date = data.get('start_date')
	end_date = data.get('end_date')
	isCurrentlyWorking = data.get('isCurrentlyWorking')
	category = data.get('category')

	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	try:
		c.execute('UPDATE project SET id = ?, title = ?, content = ?, start_date = ?, end_date = ?, isCurrentlyWorking = ?, category = ? WHERE id = ?', (id, title, content, start_date, end_date, isCurrentlyWorking, category, project_id))
		conn.commit()
		response = jsonify({'message': 'project updated successfully'}), 201
	except sqlite3.IntegrityError as e:
		print('Invalid Data entry', e)
		response = jsonify({'message': 'Invalid Data Entry or Data already exists.'}), 400
	finally:
		conn.close()

	return response

# Route for DELETE project
@app.route('/project/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	c.execute('DELETE FROM project WHERE id = ?', (project_id,))
	conn.commit()
	conn.close()

	return jsonify({'message': 'project deleted successfully'}), 201

# Custom routes GET getUserById
@app.route('/getUserById', methods=['GET'])
def getUserById():
	id = request.args.get('id')
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	getUserById = c.execute('SELECT name, age, gender FROM user WHERE id = ?', (id)).fetchall()
	conn.commit()
	conn.close()

	return jsonify(getUserById)

# Custom routes GET sortByEmail
@app.route('/sortByEmail', methods=['GET'])
def sortByEmail():
	conn = sqlite3.connect(DB_NAME)
	c = conn.cursor()
	sortByEmail = c.execute('SELECT * FROM user ORDER BY email ASC').fetchall()
	conn.commit()
	conn.close()

	return jsonify(sortByEmail)

if __name__ == '__main__':
	init_db()
	app.run(debug=True)

