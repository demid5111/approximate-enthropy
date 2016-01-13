__author__ = 'demidovs'
import random
with open("data/sample.dat","w") as f:
	for i in range(300):
		f.write(str(random.randint(300,1500)))
		f.write('\n')