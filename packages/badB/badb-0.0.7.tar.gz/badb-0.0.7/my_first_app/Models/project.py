class Project:
	def __init__(self, id, title, content, start_date, end_date, isCurrentlyWorking, category):
		self._id = id
		self._title = title
		self._content = content
		self._start_date = start_date
		self._end_date = end_date
		self._isCurrentlyWorking = isCurrentlyWorking
		self._category = category

	def get_id(self):
		return self._id

	def get_title(self):
		return self._title

	def get_content(self):
		return self._content

	def get_start_date(self):
		return self._start_date

	def get_end_date(self):
		return self._end_date

	def get_isCurrentlyWorking(self):
		return self._isCurrentlyWorking

	def get_category(self):
		return self._category

	def set_id(self, id):
		self._id = id

	def set_title(self, title):
		self._title = title

	def set_content(self, content):
		self._content = content

	def set_start_date(self, start_date):
		self._start_date = start_date

	def set_end_date(self, end_date):
		self._end_date = end_date

	def set_isCurrentlyWorking(self, isCurrentlyWorking):
		self._isCurrentlyWorking = isCurrentlyWorking

	def set_category(self, category):
		self._category = category

