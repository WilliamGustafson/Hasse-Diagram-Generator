from sys import argv
from posets import transClose
from math import log
from diagram import *

class loi:
	def __init__(this,vars):
		#read input file and make a Diagram object
		this.vars=vars
		f=open(this.vars.argv[1],"rb")
		the_input=f.read().decode('ascii')
		f.close()
		this.diagram=Diagram(scale=vars.nodetikzscale)
		err=this.diagram.parse(the_input)
		if err!=None:
			print("Error while parsing input file ",this.vars.argv[1])
			print(err)
			exit()
		this.P=this.diagram.M
		transClose(this.P)
		this.inverse_names={v: k for k,v in this.diagram.names.items()} #inverse of dictionary this.diagam.names, takes indices to names used in the diagram
		#make lower order ideals
		irr=[]
		for i in range(0,len(this.P)):
			x=1<<i
			for j in range(0,len(this.P[i])):
				if this.P[i][j]==-1: x|=1<<j
			irr.append(x)
		#add all unions to make distr lattice
		this.loi_P=[0]+[i for i in irr]
		new=[i for i in irr]
		while len(new)>0:
			last=new
			new=[]
			for l in last:
				for i in irr:
					x=l|i
					if x not in this.loi_P:
						this.loi_P.append(x)
						new.append(x)
		this.lengths=[[] for i in range(0,len(this.P)+1)]
		for l in this.loi_P:
			this.lengths[len([c for c in bin(l) if c=='1'])].append(l)
		for r in this.lengths: r.sort()
		this.maxrksize=max([len(l) for l in this.lengths])

		this.vars = vars
		this.ranked=True

	def loc_x(this,i):
		rk=len([c for c in bin(i) if c=='1'])
		if len(this.lengths[rk])==1: return '0'
		rkwidth=log(float(len(this.lengths[rk])))/log(this.maxrksize)*float(this.vars.width)
		index=this.lengths[rk].index(i)
		return str((float(index)/float(len(this.lengths[rk])-1))*rkwidth - (rkwidth/2.0))

	def loc_y(this,i):
		if i==0: return '0'
		if i==(1<<len(this.P))-1: return str(this.vars.height)
		delta=float(this.vars.height)/float(len(this.lengths)-2)
		return str(len([c for c in bin(i) if c=='1'])*delta-delta/2.0)

	def less(this,i,j):
		return i&j==i


	def nodeLabel(this,i):
		if i==0: return "$\\emptyset$"
		return this.diagram.draw([this.inverse_names[j] for j in range(0,len(this.P)) if i&(1<<j)!=0])

	def nodeName(this,i):
		return str(this.loi_P.index(i))

	def extra_packages(this):
		return ""



