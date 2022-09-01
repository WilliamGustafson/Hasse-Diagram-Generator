#computes the join of i and j in M, returns -1 if it does not exist
def join(i,j,M):
	if i==j: return i
	if M[i][j] == -1: return i
	if M[i][j] == 1: return j
	m = [x for x in range(0,len(M)) if M[i][x] == 1 and M[j][x] == 1]
	for x in range(0,len(m)):
		isJoin = True
		for y in range(0,len(m)):
			if x!=y and M[m[x]][m[y]] != 1:
				isJoin = False
				break
		if isJoin: return m[x]
	return None
#given a matrix encoding all the cover relations of a poset this function
#alters the input to compute the matrix representing the poset
def transClose(M):
	for i in range(0,len(M)):
		#uoi for upper order ideal
		uoi = [x for x in range(0,len(M)) if M[i][x] == 1]
		while True:
			next = [x for x in uoi]
			for x in uoi:
				for y in range(0,len(M)):
					if M[x][y] == 1 and y not in next: next.append(y)
			if uoi == next: break
			uoi = next

		for x in uoi:
			M[i][x] = 1
			M[x][i] = -1
