#This module provides a class for use with hasse.py to produce tikz code for the Hasse diagram of a Boolean algebra,
#that is, the poset of subsets of {1,...,n}

from math import log #rank widths fit to a log curve looks nice

class booleanAlgebra:
	def __init__(this,vars):
		this.exception=None
		this.vars=vars
		try:
			this.n=int(this.vars.get_arg('n',1))
		except:
			this.exception=Exception('You must provide an integer length as argument n')
			return
		#we store subsets of {1,...,n} as integers 0 to 2^n-1, nonzero bits indicate elements
		this.P=range(0,1<<this.n)
		this.vars=vars
		this.ranked=True
		this.lengths=[[] for r in range(0,this.n+1)]
		for p in this.P: #append each p to its corresponding rank
			this.lengths[len([i for i in range(0,this.n) if (1<<i)&p!=0])].append(p)

		#default label is elements listed with no seperation (e.g. set {1,2,3} has label 123)
		temp=this.vars.get_arg('labels',None)
		if temp==None:
			this.label_code="ret=''.join([str(j+1) for j in range(0,this.n) if (1<<j)&i!=0])"
		#user provided label
		else:
			f=open(temp,"rb")
			this.label_code=f.read().decode('ascii')
			f.close()

	def loc_x(this,i):
		if i==0 or i==(1<<this.n)-1: return '0' #top and bottom elements
		absi=len([j for j in range(0,this.n) if (1<<j)&i!=0])
		rkwidth=log(float(len(this.lengths[absi])))/log(len(this.lengths[this.n>>1]))*float(this.vars.width)
		index=this.lengths[absi].index(i)
		return str((float(index)/float(len(this.lengths[absi])-1))*rkwidth - (rkwidth/2.0))

	def loc_y(this,i):
		if i==0: return '0'
		if i==(1<<this.n)-1: return str(this.vars.height)
		delta=float(this.vars.height)/float(this.n-1) #height distance between ranks
		#return value is rank(i)*delta - delta/2
		return str(len([j for j in range(0,this.n) if (1<<j)&i!=0])*delta-delta/2.0)
	#& is intersection
	def less(this,i,j):
		return i&j==i


	def nodeLabel(this,i):
		#label_code sets a variable ret to return
		#default is ''.join([str(j) for j in range(0,this.n) if (1<<j)&i!=0])
		scope={"this":this,"i":i}
		exec(this.label_code,scope)
		return scope['ret']


	def nodeName(this,i):
		return str(i)

	def extra_packages(this):
		return ""
