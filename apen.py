from math import log

__author__ = 'demidovs'

class ApEn:
	def __init__(self,m,r):
		self.N = -1
		self.m = m
		self.r = r
		self.u_list = []
		self.x_list = []
		self.c_list = []

	def read_series(self,fileName):
		self.u_list = []
		with open(fileName,"r") as f:
			for val in f.readlines():
				self.u_list.append(int(val.strip()))
		assert self.u_list, "File is either missed or corrupted"
		assert len(self.u_list)>=300, "Sample length is too small. Need more than 300"

	def create_vectors(self,m):
		self.x_list = []
		for i in range(self.N-m+1):
			self.x_list.append(self.u_list[i:i+m])

	def calculate_distance(self,x1, x2):
		assert len(x1) == len(x2), "Vectors should be of equal sizes: " + str(x1) + " : " + str(x2)
		res = []
		for i in range(len(x1)):
			res.append(abs(x1[i] - x2[i]))
		return max(res)


	def calculate_c(self,m):
		self.c_list = []
		for i in range(0,self.N-m+1):
			similar_vectors = 0
			for j in range(0,self.N-m+1):
				res = self.calculate_distance(self.x_list[i],self.x_list[j])
				if (res < r):
					similar_vectors += 1
			self.c_list.append(similar_vectors/(self.N-m+1))


	def _final(self,m):
		return sum([log(self.c_list[i]) for i in range(self.N-m+1)])\
		       *((self.N-m+1)**(-1))

	def calculate_final(self,m):
		self.N = len(self.u_list)
		# 3. Form a sequence of vectors so that
		# x[i] = [u[i],u[i+1],...,u[i+m-1]]
		# i ~ 0:N-m because indexes start from 0
		self.create_vectors(m=m)

		# 4. Construct the C(i,m) - portion of vectors "similar" to i-th
		# similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
		# this is just the respective values subtraction
		self.calculate_c(m=m)

		res1 = self._final(m=m)
		return res1

	def calculate_apen(self,m):
		return self.calculate_final(m) - self.calculate_final(m+1)

if __name__ == "__main__":
	# 2. Fix m and r
	# TODO: compute r later as the value from the deviation
	m = 2 # m is 2 in our case
	r = 500 # r is now random, not sure which are real values

	apEn = ApEn(m=2,r=500)
	# 1. Read values: u(1), u(2),...,u(N)
	apEn.read_series("data/sample.dat")

	apEn.calculate_apen(m=m)
	apEn.calculate_apen(m=m+1)


	res1 = apEn.calculate_apen(m=m)
	print(res1)