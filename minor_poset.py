from sys import argv
from posets import transClose, join
from math import log
from diagram import Diagram
class minor_poset:
	def in_minor(this,i,m):
		j=m[0]
		for k in [x for x in  m[1] if this.joins[i][x]==i]: #i in m iff i is equal to the join of all generators in m below j and the minimum of m
			j=this.joins[j][k]
		return i==j
	#nodes is a minor and item_args is from coord_default_stick or draw_default_stick
	def stuck(this,minor,item_args):
		if len(item_args)==0: return True
		if type(item_args[0])==list: #draw command
			for e in item_args[0]:
				if not this.in_minor(this.diagram.names[e],minor): return False
			joins_row=this.joins[this.diagram.names[item_args[0][0]]]
			for g in minor[1]:
				if joins_row[g]==this.diagram.names[item_args[0][1]]: return True
			return False

		else: #coord command or other
			for e in item_args:
				if not this.in_minor(this.diagram.names[e],minor): return False
			return True

	def coord_default_stick(this,line,elems):
		return elems[0:1]
	def draw_default_stick(this,line,elems):
		return [elems[0:2]]

	def __init__(this,vars):
		#read off diagram code and make Diagram objects
		this.vars=vars
		f=open(vars.argv[1],"r")
		the_input=f.read()
		f.close()

		this.diagram=Diagram()
		#overwrite stuck and default sticks
		this.diagram.stuck=lambda nodes,item_args: this.stuck(nodes,item_args)
		this.diagram.coord_default_stick=lambda line,elems: this.coord_default_stick(line,elems)
		this.diagram.node_default_stick=lambda line,elems: this.coord_default_stick(line,elems)
		this.diagram.draw_default_stick=lambda line,elems: this.draw_default_stick(line,elems)
		err=this.diagram.parse(the_input)
		if err!=None:
			print("Error while parsing input file ",vars.argv[1])
			print(err)
			exit()

		#get the lattice from the diagram make join table
		this.L=[[x for x in row] for row in this.diagram.M] #diagram of lattice L
		transClose(this.L)
		this.joins=[[join(i,j,this.L) for j in range(0,i)]for i in range(0,len(this.L))]
		for i in range(0,len(this.L)): this.joins[i]+=[i]+[this.joins[j][i] for j in range(i+1,len(this.L))]
		#check that all joins exist
		for i in range(0,len(this.L)):
			for j in range(0,i):
				if this.joins[i][j]==None:
					print("The join of",i,"and",j," does not exist")
					exit()
		#find zerohat
		this.zerohat=-1
		zerohat_row=tuple(range(0,len(this.L)))
		for i in range(0,len(this.L)):
			if tuple(this.joins[i])==zerohat_row:
				this.zerohat=i
				break
		if this.zerohat==-1:
			print("Could not find the zerohat element from your diagram")
			exit()
		this.genL=[i for i in range(0,len(this.L)) if this.diagram.M[this.zerohat][i]==1]

		#make the minor poset
		this.minors = [[this.zerohat,this.genL]]
		this.minors_M = [[0]]
		this.minors_ranks = [[] for i in range(0,len(this.genL)+1)]
		this.minors_ranks[len(this.genL)].append(1) #will add a zerohat later
		new = [[this.zerohat,this.genL]]
		while len(new)>0:
			old = new
			new = []
			for l in old:
				r = this.minors.index(l)
				for i in range(0,len(l[1])): #delete i from l
					minor=[l[0],l[1][:i]+l[1][i+1:]]
					if minor in this.minors:
						s = this.minors.index(minor)
					else:
						s = len(this.minors_M)
						this.minors_ranks[len(minor[1])].append(s+1)
						this.minors.append(minor)
						for x in this.minors_M: x.append(0)
						this.minors_M.append([0 for x in range(-1,s)])
					this.minors_M[r][s] = -1
					this.minors_M[s][r] = 1
					if minor not in new: new.append(minor)

					#contract l by i
					temp = set([this.joins[l[1][i]][j] for j in l[1]])
					temp.remove(l[1][i])
					minor=[l[1][i],sorted(list(temp))]
					if minor in this.minors:
						s = this.minors.index(minor)
					else:
						s = len(this.minors_M)
						this.minors_ranks[len(minor[1])].append(s+1)
						this.minors.append(minor)
						for x in this.minors_M: x.append(0)
						this.minors_M.append([0 for x in range(-1,s)])
					this.minors_M[r][s] = -1
					this.minors_M[s][r] = 1
					if minor not in new: new.append(minor)

		this.minors_ranks = [[0]]+this.minors_ranks
		for i in range(0,len(this.minors_M)):
			this.minors_M[i] = [-1]+this.minors_M[i]
		this.minors_M = [[0]+[1 for i in range(0,len(this.minors_M))]]+this.minors_M

		transClose(this.minors_M)
		this.n=len(this.genL)
		this.lastrk=0
		this.maxrk=max([len(r) for r in this.minors_ranks])
		this.lengths=this.minors_ranks
		this.ranked=True

	def get_rk(this,i):
		return this.lengths[0] if i==0 else this.lengths[1+len(this.minors[i-1][1])]
	def loc_x(this,i):
		rk=this.get_rk(i)
		if len(rk)==1: return str(0)
		rkwidth=(log(len(rk))/log(this.maxrk))*float(this.vars.width)
		return str((rkwidth/float(len(rk)-1))*float(rk.index(i))-(rkwidth/2.0))

	def loc_y(this,i):
		if i==this.minors_ranks[0][0]: return str(0)
		rk=this.get_rk(i)
		if len(this.minors[i-1][1])==this.n: return str(this.vars.height)
		delta=float(this.vars.height)/(2*this.n)
		return str(float(2*(len(this.minors[i-1][1])))*delta+delta)

	def extra_packages(this):
		return ""

	def nodeName(this,i):
		if i==0: return "empty"
		return '/'.join([str(this.minors[i-1][0])]+[str(x) for x in this.minors[i-1][1]])

	def nodeLabel(this,i):
		if i==0: return "$\\emptyset$"
		minor=this.minors[i-1]
		return this.diagram.draw(minor)

	def less(this,i,j):
		return this.minors_M[i][j]==1
