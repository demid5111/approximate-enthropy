class S:
	def __init__(self,num):
		self.num = num
	def __add__(self, other):
		print ("in add")
		return S(self.num+other)
	def __radd__(self, other):
		print("in radd")
		return S(self.num+other)
	def __str__(self):
		return "[S:{}]".format(self.num)
a = S(10)
b = S(20)
print(a+b)