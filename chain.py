#This module provides a class for use with hasse.py to create Hasse diagrams of a chain of specified length
#This is provided as an example to serve as a specification

#If the class name does not match the file name you must provide the class
#name as named argument "class" to hasse.py
class chain:
	#vars is an instance of HasseVars (see hasse.py for definition)
	#vars.argv contains all remaining arguments

	def __init__(this,vars):
		this.exception=None
		try:
			this.vars=vars
			this.n=int(this.vars.get_arg('n',1)) #this will return the argument following 'n' on the command line if there is one and otherwise 1, then those two arguments are sliced out of vars.argv
		except:
		#if exception is not None hasse.py will print the message and terminate
			this.exception=Exception('You must provide an integer length as argument n')
			return
		this.lengths=[[i] for i in range(0,this.n+1)] #lengths should be a list whose ith element contains the elements, or some identifier for the elements, of length i
		this.ranked=True #boolean indicating whether poset is ranked or not
		return

	#return the tikz x-coordinate for the element i (i is an element of an element of lengths)
	def loc_x(this,i):
		return '0'

	#return the tikz y-coordinate for the element i
	def loc_y(this,i):
		return str(i)

	#return True if i<=j in the poset and False otherwise
	def less(this,i,j):
		return i<=j

	#the label to be displayed for the element i
	def nodeLabel(this,i):
		return str(i)

	#the name of the node in the tex file for the element i, must be a legal tikz identifier
	def nodeName(this,i):
		return str(i)

	#the returned value is written into the tex file just after \documentclass{article}\n\usepackage{tikz}\n
	#include any packages and set up any macros needed here
	#preview and geometry are already included after the return value
	def extra_packages(this):
		return ""
