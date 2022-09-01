##########################################
#This file provides a class Diagram that provides utitlities to parse an input
#file describing a directed graph, intended for posets, and produce tikz code for the
#diagram and a matrix describing the incidences. A draw function provides a
#method to produce tikz code for subsets of the diagram with elements removed.
#
#This class is used by Minor.py and loi.py
#
#The input file consists of a series of commands seperated by new lines.
#Arguments to commands are specified in between { and }
#The signed incidence matrix encoding the directed graph is constructed from the commands to draw lines when the commands are parsed.
#Commands can each be "stuck" to one or more vertices and when the draw method is called
#tikz code is produced with any commands stuck to a vertex not specified in the draw call removed
#The default behaviour of what commands are kept can be overwritten by replacing the stuck method, see Minor.py for an example
#
#See examples/loi and examples/Minor for example input files
#
#The commands are:
#	coord[..tikz options...]{x}{y}
#		Creates a tikz coordinate named x at (y)
#		Additionally ensures that x is an element
#		and sticks this command to the element x
#
#		Optionally, you can include tikz option to the \coordinate command in brackets
#
#	draw[...tikz options...]{x}{y}{b1}{b2}
#		Draws a line from node x to node y.
#		If x and y are not elements they are added.
#		The edge from x to y is encoded in the incidence matrix.
#		The arguments b1 and b2 are each optional, if
#		added they are used as the control points
#		to make a curved line in the tikz code.
#
#	\
#		Any line beginning with \ is written verbatim including the leading \
#	-\
#		Any line beginning with -\ is written verbatim excluding the leading -\
#	#
#		Lines beginning with # are comments and have no effect
#
#	elem{x1}...{xn}
#		x1 through xn are added as elements. This produces no tikz code.
#
#	hide
#		The previous line will produce no tikz code, other effects
#		such as adding elements and incidences still occur
#
#	stick{x1}...{xn}
#		The previous command is stuck to x1 through xn.
#
#	scale{x}
#		The scale of the tikz diagrams produced by the draw method is x, that is, the beginning of the tikz code is something like \begin{tikzpicture}[scale=x]
#	@
#		An @ symbol at the beginning of a line starts a block of python code
#		and the @ symbol ends the block. This block of code is executed.
#		You can parse a command from inside a code block as this.read_line(line_to_parse)
##########################################

class Diagram:
	def parseElems(s):
		return [x.split('}')[0].strip() for x in s.split('{')[1:]]

	def stick_handler(this,s):
		for e in Diagram.parseElems(s):
			this.commands[-1][1].append(e)

	def get_options(s):
		t=s.lstrip()
		if t[0]!='[': return ""
		a=t.index('[')
		b=a+1 #should point just past the ] at the end of the options
		i=1
		for c in t[1:]:
			b+=1
			if c=='[':
				i+=1
			elif c==']':
				i-=1
			if i==0: break
		if i!=0: return None #brackets are mismatched
		return t[a:b]


	def read_line(this,line):
		line+='#'
		line=line[:line.index('#')].strip()
		this.index+=1
		if line=="": return
		if line[0]=='\\':
			this.commands.append([line,this.com_default_stick(line)])
			return
		if line[0:2]=='-\\':
			this.commands.append([line[2:],this.escaped_default_stick(line)])
			return
		if line[0:4]=='hide':
			this.commands[-1][0]==''
			return
		if line[0:5]=='stick':
			this.stick_handler(line[5:])
			return
		if line[0:5]=='coord':
			options=Diagram.get_options(line[5:])
			if options==None: return "Error mismatched [ and ]"
			temp=Diagram.parseElems(line[5:])
			if len(temp)<2:
				return "Error coord requires two arguments"
			this.commands.append(['\\coordinate'+options+'('+temp[0]+')at('+temp[1]+');',this.coord_default_stick(line,temp)])

			if temp[0] not in this.names: #make sure coordinate name is an element name
				this.names[temp[0]]=len(this.M)
				this.M.append([0 for l in this.M])
				for l in this.M: l.append(0)
			stick_index=line.find('stick')
			if stick_index==-1: return
			this.stick_handler(line[stick_index+4:])
		if line[0:4]=='node':
			options=Diagram.get_options(line[4:])
			if options==None: return "Error mismatched [ and ]"
			temp=Diagram.parseElems(line[4:])
			if len(temp)<3:
				return "Error node requires three arguments"
			this.commands.append(['\\node'+options+'('+temp[0]+')at('+temp[1]+'){'+temp[2]+'};',this.node_default_stick(line,temp)])

			if temp[0] not in this.names: #make sure coordinate name is an element name
				this.names[temp[0]]=len(this.M)
				this.M.append([0 for l in this.M])
				for l in this.M: l.append(0)
			stick_index=line.find('stick')
			if stick_index==-1: return
			this.stick_handler(line[stick_index+4:])

		if line[0:4]=='draw':
			options=Diagram.get_options(line[4:])
			if options==None: return "Error mismatched [ and ]"
			elems=Diagram.parseElems(line[4:(line+' ').find('stick')])

			#add elements and cover to L
			if elems[0] in this.names: i=this.names[elems[0]]
			else:
				this.names[elems[0]]=len(this.M)
				i=len(this.M)
				this.M.append([0 for l in this.M])
				for r in this.M: r.append(0)
			if elems[1] in this.names: j=this.names[elems[1]]
			else:
				this.names[elems[1]]=len(this.M)
				j=len(this.M)
				this.M.append([0 for l in this.M])
				for r in this.M: r.append(0)
			this.M[i][j]=1
			#check for hide but allow it to be in an options or a node name
			temp=line[4:].find('hide')
			#if hide is not in the line or if it is but is but in between [] or ()
			#(check fails on mismatched brackets)
			if temp==-1 or (line[:temp].index('[')>line[:temp].index(']') and line[:temp].index('(')>line[:temp].index(')')):
				this.commands.append(['\\draw'+options,this.draw_default_stick(line,elems)])

				if len(elems)==2:
					this.commands[-1][0]+='('+elems[0]+'.north)--('+elems[1]+'.south);'
				if len(elems)>2:
					this.commands[-1][0]+='('+elems[0]+'.north)..controls'+elems[2]
					if len(elems)==3:
						this.commands[-1][0]+='..('+elems[1]+'.south);'
					if len(elems)>=4:
						this.commands[-1][0]+='and'+elems[3]+'..('+elems[1]+'.south);'
				temp=line[4:].find('stick')
				if temp!=-1:
					this.stick_handler(line[4+temp:])
		if line[0:5]=='scale':
			this.scale=Diagram.parseElems(line[5:])[0]
		if line[0:4]=='elem':
			temp=Diagram.parseElems(line[4:])
			for t in temp:
				this.names[t]=len(this.M)
				this.M.append([0 for l in this.M])
				for r in this.M: r.append(0)

	def parse(this,s):
		code_line=False
		code=[]
		line_index=-1
		for line in [x for x in s.split('\n')]:
			line_index+=1
			if len(line)==0: continue
			if code_line==False:
				if line[0]=='@':
					code_line=True
					code.append(line[1:])
				msg=this.read_line(line.strip())
				if msg!=None: return "Line "+str(line_index)+": "+msg #error reading line
			else:
				code.append(line[:line.index('@')])
				exec('\n'.join(code),globals(),locals())
				code_line=False
	def stuck(nodes,item_args):
		for i in item_args:
			if i not in nodes: return False
		return True

	def draw(this,nodes):
		ret=['\\begin{tikzpicture}[scale='+this.scale+']\\begin{scope}\n']
		for com in this.commands:
			if this.stuck(nodes,com[1]):
				ret.append(com[0])
		ret+=['\n\\end{scope}\\end{tikzpicture}']
		return '\n'.join(ret)

	def __init__(this,the_input=None,scale=1):
		this.com_default_stick=lambda line: []
		this.escaped_default_stick=lambda line: []
		this.coord_default_stick=lambda line,elems: [elems[0]]
		this.node_default_stick=lambda line,elems: [elems[0]]
		this.draw_default_stick=lambda line,elems: [elems[0],elems[1]]
		this.commands=[]
		this.names={}
		this.index=-1
		this.stuck=Diagram.stuck
		this.scale=str(scale)
		this.M=[]
