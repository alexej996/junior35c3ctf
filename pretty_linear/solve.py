from sympy import Matrix, pprint
import sympy
from Crypto.Util.number import *
import Crypto
import binascii
from hashlib import sha256
from Crypto.Cipher import AES
import sys
from progressbar import ProgressBar
pbar = ProgressBar()

p = 340282366920938463463374607431768211297
N = 40

def decrypt(key):
	cyphertext=binascii.unhexlify("923fa1835d8dbdcd9f9b0e6658b24fce54512fbba71d7a0012c37d2c9dd094a6278593d8d9f7a4aa9fecb66042")
	cipher = AES.new(sha256(' '.join(map(str, key)).encode('utf-8')).digest(), AES.MODE_CFB, b'\0'*16)
	return cipher.decrypt(cyphertext).decode('utf-8')

def solve(m):
	M=Matrix(m)
	M.col_del(N)

	M=M.applyfunc(lambda x : x % p)

	M_det=sympy.det(M)%p
	M_det_inv=Crypto.Util.number.inverse(M_det, p)

	X=list()

	for i in range(N):
		X.append(Matrix(m))

	for i in range(N):
		X[i].col_swap(i,N)
		X[i].col_del(N)
		X[i]=X[i].applyfunc(lambda x : x % p)

	X_det=list()

	print("Solving the matrix...")
	for i in pbar(range(N)):
		try:
			X_det.append(sympy.det(X[i])%p)
		except KeyboardInterrupt:
			exit()

	key=list()

	for i in range(N):
		key.append((X_det[i]*M_det_inv)%p)
	return key

if __name__ == '__main__':

	print("Loading the matrix...")
	matrixfile=open("matrix","r")
	m0=list()

	for i in range(N):
        	r = matrixfile.readline()
        	m0.append(list(map(int, r.split(' '))))
        	r = matrixfile.readline()
        	m0[i].append(int(r))

	print(decrypt(solve(m0)))
