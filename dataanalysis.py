import numpy as np
import random
from scipy import stats
from sklearn import linear_model


n = 5 # number of features
N = 100 # number of observations

###############
# Generate data
###############

dispersions= [1 for i in xrange(n)]

covariance = np.zeros((n,n)) # create n x n matrix of zeros
for i in xrange(n):
	for j in xrange(n):
		# generate covariation matrix: c[i,j] = DX_i if we're on diagonal, random number from U[-1;1] otherwise
		covariance[i,j] = dispersions[i] if i == j else covariance[j, i] if covariance[j, i] != 0 else 2*random.random()-1
# make covariation matrix positive definite
covariance = np.dot(covariance, np.matrix.transpose(covariance))
print "covariance:\n{cov}\n".format(cov=covariance) # show covariance matrix

eig = np.linalg.eig(covariance)
eigvals, eigvectors = eig
# for (i, val) in zip(eigvals, eigvectors):
# 	print i, val
# print np.linalg.cholesky(covariance)

def random_vector(R, N=1):
	k = len(R[0]) # get number of features from covariance matrix because relying on global variables is a bad idea
	x = np.empty((N, k)) # create empty array of given shape
	# fill this array with random observations of normal distribution with given covariance matrix R
	for i in xrange(N):
		s = np.random.normal(size=len(R[0])) 
		x[i] = np.dot(np.linalg.cholesky(R), s)
	return x

# get random sample
X = random_vector(covariance, N)

beta = np.array([3,2,0,1,1]) # regression coefficients
sigma = 0.01 # noise variance

Y = np.add(np.dot(X, beta), np.random.normal(scale=sigma, size=N)) # get Y that we will try to predict by X

############################################
# Do regression analysis and analyze results
############################################

clf = linear_model.LinearRegression()
clf.fit(X, Y) # now object clf has all the information about predicting Y by X

print "estimated regression:"
print clf.coef_
print "real regression:"
print beta


######################################
# Check significance of the regression
######################################

# L -- matrix of the second centered sample moments
L = np.empty((n, n))
mean_x = np.mean(X, axis=1)
for i in xrange(n):
	for j in xrange(n):
		L[i][j] = np.average(map(lambda t: (X[t][i] - mean_x[i])*(X[t][j] - mean_x[j]), xrange(N)))
# L0 -- second centered sample "moments" between X and Y
L0 = np.empty((n, ))
mean_y = np.mean(Y)
L0 = map(lambda j: np.average(map(lambda t: (Y[t] - mean_y)*(X[t][j] - mean_x[j]), xrange(N))), xrange(n))

# nobody does really care about cofactors in scipy, so we'll compute them by ourselves
def matrix_cofactor(matrix, row, col):
    nrows, ncols = matrix.shape
    minor = np.zeros([nrows-1, ncols-1])
    minor[:row,:col] = matrix[:row,:col]
    minor[row:,:col] = matrix[row+1:,:col]
    minor[:row,col:] = matrix[:row,col+1:]
    minor[row:,col:] = matrix[row+1:,col+1:]
    C = (-1)**(row+col) * np.linalg.det(minor)
    return C

LSM_expected_alpha = mean_y
LSM_expected_beta = map(lambda i: 
	np.sum(map(lambda j: L0[j]*matrix_cofactor(L,i,j), xrange(n)))/np.linalg.det(L), xrange(n))
print "regression estimates, calculated using cofactors:"
print LSM_expected_beta, LSM_expected_alpha




