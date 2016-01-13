from math import log

__author__ = 'demidovs'

def read_series(fileName):
	res = []
	with open(fileName,"r") as f:
		for val in f.readlines():
			res.append(int(val.strip()))
	return res


def create_vectors(N, m,u_list):
	res_vectors = []
	for i in range(N-m+2):
		res_vectors.append(u_list[i:i+m])
	return res_vectors


def calculate_distance(x1, x2):
	assert len(x1) == len(x2), "Vectors should be of equal sizes"
	res = []
	for i in range(len(x1)):
		res.append(abs(x1[i] - x2[i]))
	return max(res)


def calculate_c(N,m,r,x_list):
	c_vector = []
	for i in range(0,N-m+1):
		similar_vectors = 0
		for j in range(0,N-m+1):
			res = calculate_distance(x_list[i],x_list[j])
			if (res < r):
				similar_vectors += 1
		c_vector.append(similar_vectors/(N-m+1))
	return c_vector


def calculate_final(N, m, c_list):
	return sum([log(c_list[i]) for i in range(N-m+1)])*((N-m+1)**(-1))


if __name__ == "__main__":
	# 1. Read values: u(1), u(2),...,u(N)
	u_list = read_series("data/sample.dat")
	assert u_list, "File is either missed or corrupted"
	assert len(u_list)>=300, "Sample length is too small. Need more than 300"

	# 2. Fix m and r
	# TODO: compute r later as the value from the deviation
	m = 2 # m is 2 in our case
	r = 500 # r is now random, not sure which are real values
	N = len(u_list)

	# 3. Form a sequence of vectors so that
	# x[i] = [u[i],u[i+1],...,u[i+m-1]]
	# i ~ 0:N-m because indexes start from 0
	x_list = create_vectors(N=N,m=m,u_list=u_list)

	# 4. Construct the C(i,m) - portion of vectors "similar" to i-th
	# similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
	# this is just the respective values subtraction
	c_list =  calculate_c(N=N,m=m,r=r,x_list=x_list)

	res1 = calculate_final(N=N,m=m,c_list=c_list)
	print(res1)