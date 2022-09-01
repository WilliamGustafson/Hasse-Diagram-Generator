#!/usr/bin/env python3
import sys
from importlib import import_module

#This is a class to assist with getting arguments from the command line
#and fill in default values
class HasseVars:
	def sindex(s,t): #index method for strings that won't throw
		return s.index(t) if t in s else len(s)
	#methods to get arguments from the command line and consume them
	def get_pos_arg(this,index):
		if index>=len(this.argv): return None
		ret=this.argv[index]
		this.argv=this.argv[:index]+this.argv[index+1:]
		return ret

	def get_arg(this,arg,default):
		arg='-'+arg
		i=HasseVars.sindex(this.argv,arg)
		if i>=len(this.argv)-1: return default
		ret=this.argv[i+1]
		this.argv=this.argv[:i]+this.argv[i+2:]
		return ret

	def get_flag(this,flag,default):
		flag="-"+flag
		if flag not in this.argv: return default
		i=this.argv.index(flag)
		this.argv=this.argv[:i]+this.argv[i+1:]
		return not default

	def __init__(this,vars=''):
		this.argv=vars
		try:
			this.width=float(this.get_arg('width',18))
		except:
			print("The argument width must be a decimal number")
			exit()
		try:
			this.height=float(this.get_arg('height',30))
		except:
			print("The argument height must be a decimal number")
			exit()
		this.nodescale=this.get_arg('nodescale','1')
		this.nodetikzscale=this.get_arg('nodetikzscale','1')
		this.scale=this.get_arg('scale','1')
		this.tikzscale=this.get_arg('tikzscale','1')
		this.line_options=this.get_arg('line_options','')
		if this.line_options!='': this.line_options='['+this.line_options+']'
		this.northsouth=this.get_flag('no_northsouth',True)
		this.lowsuffix=this.get_arg('lowsuffix','.north' if this.northsouth else '')
		this.highsuffix=this.get_arg('highsuffix','.south' if this.northsouth else '')
		this.labels=this.get_flag('no_labels',True)
		this.ptsize=this.get_arg('ptsize',None if this.labels else '2pt')
		this.debug=this.get_flag('debug',False)
		this.class_name=this.get_arg('class',None)
		this.module_name=this.get_pos_arg(1)
		if this.module_name[-3:]=='.py': this.module_name=this.module_name[:-3]
		if this.class_name==None: this.class_name=this.module_name

#prints all non-hidden and non-callable attributes for debugging
def print_attrs(o,name):
	for a in dir(o):
		if a[:2]=="__": continue
		attr=getattr(o,a)
		if not callable(attr):
			print(name+"."+a,"=",getattr(o,a))

usage_string='Usage: hasse.py MODULE [ARGS...]'
vars=HasseVars(sys.argv)
try:
	lib=import_module(vars.module_name)
except Exception as e:
	print("Encountered an error while importing module ",module_name)
	print(e)
	print(usage_string)
	print('If you are providing your own module the class defined in the module must have the same name as the module')
	exit(1)

#shorten syntax for encoding strings to ascii
def b(s):
	return s.encode('ascii')

#o is the object
o=getattr(lib,vars.class_name)(vars)
if 'exception' in dir(o) and o.exception!=None:
	print("Exception encountered in "+module_name+" constructor.")
	print(o.exception.args[0])
	exit()

if vars.debug:
	print_attrs(o,'o')
	if 'vars' in dir(o): print_attrs(o.vars,'o.vars')

#write preamble
f=open(sys.argv[0]+".tex","wb")
f.write(b'%'+b' '.join([b(a) for a in sys.argv])+b'\n')
f.write(b'\\documentclass{article}\n\\usepackage{tikz}\n')
f.write(b(o.extra_packages()))
f.write(b'\n\\usepackage[psfixbb,graphics,tightpage,active]{preview}\n')
f.write(b'\\PreviewEnvironment{tikzpicture}\n\\usepackage[margin=0in]{geometry}\n')
f.write(b'\\begin{document}\n\\pagestyle{empty}\n\\begin{tikzpicture}\n')

#write nodes for the poset elements
if not vars.labels:
	for rk in o.lengths:
		for r in rk:
			name=b(o.nodeName(r))
			f.write(b'\\coordinate('+name+b')at('+b(o.loc_x(r))+b','+b(o.loc_y(r))+b');\n')
			f.write(b'\\fill('+name+b')circle('+b(vars.ptsize)+b');\n')
else:
	for rk in o.lengths:
		for r in rk:
			f.write(b'\\node('+b(o.nodeName(r))+b')at('+b(o.loc_x(r))+b','+b(o.loc_y(r))+b')\n{')
			f.write(b'\scalebox{'+b(vars.nodescale)+b("}{"))
			f.write(b(o.nodeLabel(r)))
			f.write(b'}};\n\n')

#draw lines for covers
if o.ranked:
	for r in range(0,len(o.lengths)-1):
		for i in o.lengths[r]:
			for j in o.lengths[r+1]:
				if o.less(i,j):
					f.write(b'\\draw'+b(vars.line_options)+b'('+b(o.nodeName(i))+b(vars.lowsuffix)+b')--('+b(o.nodeName(j))+b(vars.highsuffix)+b");\n")

#for unranked version for each element we have to check all the higher length elements
if not o.ranked:
	for r in range(0,len(o.lengths)-1):
		for i in o.lengths[r]:
			covers=[] #elements covering i
			for s in o.lengths[r+1:]: #<--there's 2 colons this time
				for j in o.lengths[s]:
					if o.less(i,j):
						#check if j covers i
						is_cover=True
						for k in covers:
							if o.less(k,j):
								is_cover=False
								break
						if is_cover:
							covers.append(j)
							f.write(b'\\draw'+b(vars.line_options)+b'('+b(o.nodeName(i))+b(vars.lowsuffix)+b')--('+b(o.nodeName(j))+b(vars.highsuffix)+b");\n")
f.write(b'\\end{tikzpicture}\n\\end{document}')
f.close()

if vars.debug:
	print_attrs(o,'o')
	if 'vars' in dir(o):
		print_attrs(o.vars,'o.vars')
