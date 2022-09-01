from math import log #rank widths fit to a log curve look nice
from posets import transClose

class ranked:
	def __init__(this,vars):
		if len(vars.argv) < 2:
			this.exception=Exception("You must include either a file name or your input as the second argument")
			return

		try:
			f = open(vars.argv[1], "rb")

			input = []
			#first strip down input
			for line in f:
				s = line[:line.find(b'#')] #if # in line cut out that and all after, if not cut off \n
				for c in s:
					if c in b';,0123456789': input.append(chr(c))
			input=''.join(input)
			f.close()

		except IOError:
			input = vars.argv[1]

		this.ranked=True
		this.M = [] #Incidence matrix, first read off just the covers from file then will build rest

		#turn input into a list of lists of numbers, ranks ended by an empty list
		input = input.split(';')[:-1] #slice to remove one extra empty string from the end
		for i in range(0,len(input)): input[i] = input[i].split(',')
		input=[[int(j)-1 for j in i if j!='']for i in input]

		#now find ranks
		this.n = 1 #1 less than number of elements
		this.lengths = [[0]]
		temp = []
		offset = 1
		for i in range(0,len(input)):
			if input[i] == []:
				this.lengths.append(temp)
				temp = []
				offset -= 1
				continue
			temp.append(i+offset)
			this.n += 1

		#get coatoms
		m = 0 #largest index of a coatom
		i = len(input)-2
		while i > 0 and input[i] != []:
			for x in input[i]:
				if x > m:
					m = x
			i -= 1

		this.n += m+1
		this.lengths.append(range(this.lengths[-1][-1]+1,this.lengths[-1][-1]+1+m+1))
		this.lengths.append([this.n])
		rank = len(this.lengths)
		#now make cover matrix from input
		#cover matrix
		this.M = [[0] + [1]*len(this.lengths[1]) + [0]*(this.n-len(this.lengths[1]))] #zero hat row
		r = 1 #current rank
		for i in range(0,len(input)):
			if input[i] == []:
				r += 1
				continue

			temp = [0]*(this.n+1)
			for x in input[i]:
				temp[x + this.lengths[r][-1]+1] = 1
			this.M.append(temp)
		#coatom rows
		for i in range(0, len(this.lengths[-2])):
			this.M.append([0]*(this.n)+[1])

		#onehat
		this.M.append([0]*(this.n+1))

		transClose(this.M)

		this.vars=vars
		this.maxrksize=max([len(r) for r in this.lengths])

	def loc_x(this,i):
		len_P=len(this.M)
		if i==0 or i==len_P-1: return '0' #top or bottom element
		for rk in range(0,len(this.lengths)):
			if i in this.lengths[rk]: break
		if len(this.lengths[rk])==1: return '0'
		rkwidth=log(float(len(this.lengths[rk])))/log(float(this.maxrksize))*float(this.vars.width)
		index=this.lengths[rk].index(i)
		return str((float(index)/float(len(this.lengths[rk])-1))*rkwidth - (rkwidth/2.0))

	def loc_y(this,i):
		if i==0: return '0'
		if i==len(this.M)-1: return str(this.vars.height)
		for rk in range(0,len(this.lengths)):
			if i in this.lengths[rk]: break
		delta=float(this.vars.height)/float(len(this.lengths)-2)
		return str(rk*delta-delta/2.0)


	def less(this,i,j):
		return this.M[i][j]==1

	def nodeLabel(this,i):
		return str(i)

	def nodeName(this,i):
		return str(i)

	def extra_packages(this):
		return ""



