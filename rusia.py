import os,sqlite3

class moscu:
	def __init__(self,name):
		self.con = sqlite3.connect(f'{name}.db')
		self.cur = self.con.cursor()
	def execute(self,code,add = (),commit = False):
		data = ""
		if add != ():
			data = self.cur.execute(code,add)
		elif add == ():
			data = self.cur.execute(code)
		if commit:
			self.commit()
		return list(data)
	def commit(self):
		self.con.commit()
	def close(self):
		self.con.close()
	def getid(self,table,idname = "id"):
		ids = self.execute(f"SELECT {idname} FROM {table} ORDER BY {idname}")
		return 1 if len(ids) == 0 else ids[-1][0] + 1

			