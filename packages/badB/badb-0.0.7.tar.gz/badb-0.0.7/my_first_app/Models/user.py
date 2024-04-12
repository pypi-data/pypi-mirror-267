class User:
	def __init__(self, id, name, email, age, gender, password):
		self._id = id
		self._name = name
		self._email = email
		self._age = age
		self._gender = gender
		self._password = password

	def get_id(self):
		return self._id

	def get_name(self):
		return self._name

	def get_email(self):
		return self._email

	def get_age(self):
		return self._age

	def get_gender(self):
		return self._gender

	def get_password(self):
		return self._password

	def set_id(self, id):
		self._id = id

	def set_name(self, name):
		self._name = name

	def set_email(self, email):
		self._email = email

	def set_age(self, age):
		self._age = age

	def set_gender(self, gender):
		self._gender = gender

	def set_password(self, password):
		self._password = password

