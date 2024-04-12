class Post:
	def __init__(self, id, title, content, author_name, author_id, keywords):
		self._id = id
		self._title = title
		self._content = content
		self._author_name = author_name
		self._author_id = author_id
		self._keywords = keywords

	def get_id(self):
		return self._id

	def get_title(self):
		return self._title

	def get_content(self):
		return self._content

	def get_author_name(self):
		return self._author_name

	def get_author_id(self):
		return self._author_id

	def get_keywords(self):
		return self._keywords

	def set_id(self, id):
		self._id = id

	def set_title(self, title):
		self._title = title

	def set_content(self, content):
		self._content = content

	def set_author_name(self, author_name):
		self._author_name = author_name

	def set_author_id(self, author_id):
		self._author_id = author_id

	def set_keywords(self, keywords):
		self._keywords = keywords

