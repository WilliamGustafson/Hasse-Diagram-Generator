#This module provides a class for use with hasse.py to produce tikz code for the
#lattice of subspaces of a finite dimensional vector space over a finite prime field $\F_p^n$
#
#In the hasse diagram the subspaces are reresented as the row space of a matrix
#
#Throughout vectors in \F_p^n are represented as the numbers 0,\dots,p^n-1 the components of the vector are the digits when the number is represented in base p.
#In other words, the ith component of v is (v%p**i - v%p**(i-1))/p**(i-1)
from sys import argv
from math import log

class FpSubspaces:
	#does dot product
	def dot(this,v,w):
		vmodpi=v%this.p
		wmodpi=w%this.p
		ret=(vmodpi*wmodpi)
		pj=this.p
		pi=1
		vmodpj=vmodpi
		wmodpj=wmodpi
		for i in range(1,this.n):
			pj*=this.p
			pi*=this.p
			vmodpi=vmodpj
			wmodpi=wmodpj
			vmodpj=v%pj
			wmodpj=w%pj
			ret+=((vmodpj-vmodpi)*(wmodpj-wmodpi))/(pi*pi)
		return ret%this.p

	#turns a number into a list
	def vec(this,v):
		ret=[v%this.p]
		pi=1
		pj=this.p
		for i in range(1,this.n):
			pi*=this.p
			pj*=this.p
			ret.append(int((v%pj-v%pi)/pi))
		return ret

	def __init__(this,vars):
		this.vars=vars
		try:
			this.n=int(this.vars.get_arg('n',2))
		except:
			print("Argument n must be an integer")
			exit()
		try:
			this.p=int(this.vars.get_arg('p',2))
		except:
			print("Argument p must be a prime intger")
			exit()
		this.pn=this.p**this.n
		#compute all hyperplanes
		#hyperplanes are represented as numbers in range(0,2**(p**n)-1)
		#the 1-bits set indicate the elements
		this.hyperplanes=[]
		for v in range(1,this.pn):
			H=0
			for w in range(0,this.pn):
				if this.dot(v,w)==0: H|=(1<<w)
			this.hyperplanes.append(H)

		#Do intersection of hyperplanes to fill out spaces
		this.spaces=set([(1<<(this.pn))-1]+this.hyperplanes) #first term is whole space
		newspaces=this.hyperplanes
		while len(newspaces)>0:
			newnewspaces=set([])
			for S in newspaces:
				for H in this.hyperplanes:
					if S&H!=S: newnewspaces.add(S&H)
			this.spaces=this.spaces.union(newnewspaces)
			newspaces=newnewspaces
		this.lengths=[[]for i in range(0,this.n+1)]
		for S in this.spaces: this.lengths[int(log(len([j for j in range(this.pn) if (1<<j)&S!=0]),this.p))].append(S)

		this.spaces=sorted(list(this.spaces))
		for i in range(0,len(this.lengths)): this.lengths[i]=sorted(list(this.lengths[i]))
		this.ranked=True

	def loc_x(this,i):
		#zero space or whole space
		if i==1 or i==(1<<this.pn)-1: return '0'
		rk=int(log(len([j for j in range(0,this.pn) if (1<<j)&i!=0]),this.p))
		ranks=this.lengths
		rkwidth=log(float(len(this.lengths[rk])))/log(float(len(this.lengths[this.n>>1])))*float(this.vars.width)
		index=this.lengths[rk].index(i)
		return str((float(index)/float(len(this.lengths[rk])-1))*rkwidth - (rkwidth/2.0))

	def loc_y(this,i):
		if i==1: return '0'
		if i==(1<<this.pn)-1: return str(this.vars.height)
		delta=float(this.vars.height)/float(len(this.lengths)-2)
		rk=int(log(len([j for j in range(0,this.pn) if (1<<j)&i!=0]),this.p))
		return str(rk*delta-delta/2.0)

	def less(this,i,j):
		return i&j==i

	def nodeLabel(this,i):
		if i==1: return "\\scalebox{2}{$\\widehat{0}$}"
		#find a basis recursively by finding any nonzero vector
		#then intersecting with any hyperplane not containing said vector
		#and repeating until the intersection is zero
		basis=[]
		while i!=1:
			for j in range(1,this.pn):
				if (1<<j)&i!=0:
					basis.append(j)
					break
			for H in this.hyperplanes:
				if H&(1<<j)==0:
					i&=H
					break
		basis=[[str(x) for x in this.vec(b)] for b in basis]
		return "$\\left(\\begin{matrix}"+"\\\\".join(["&".join(b) for b in basis])+"\\end{matrix}\\right)$"
		return str(i)

	def nodeName(this,i):
		return str(this.spaces.index(i))

	def extra_packages(this):
		return "\\usepackage{amsmath}"


