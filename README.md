# Overview

This is a program for generating Hasse diagrams of posets. To use the program
you specify a python module that will compute the poset and the labels for elements. Several example modules are
included and example input for modules is included in the examples folder. This program will output a tex file hasse.py.tex which you may compile
into a viewable file using LaTeX.

# Options

The following command line options can be specified to change the appearence
of the Hasse diagram generated.

`-width`
	
This sets the width of the Hasse diagram in tikz units.
The default value is 18.
		
`-height`

Sets the height of the Hasse diagram in tikz units.
The default value is 30.


`-nodescale`

Nodes are wrapped in a \scalebox with the scale
factor the value of -nodescale. The default value is 1.

`-nodetikzscale`

Modules whose nodelabels are tikz figures (UC.py,loi.py and
minor_poset.py) use this argument as the scale of the figures.
The default value is 1.

`-tikzscale`

Sets the tikz scale of the Hasse diagram, the default value
is 1.

`-line_options`

This argument is added to each draw command just after \draw.
Provide tikz options enclosed in brackets here. The default
value is the empty string.

`-no_northsouth`

If this flag is provided lines will be drawn between nodes
themselves without appending ".north" and ".south". If this flag
is not provided ".north" and ".south" are added to node names.

`-lowsuffix`

The value of this argument is appended to the node name of
the lower element of each cover drawn. When the flag
-no_northsouth is present the default value is the empty
string and otherwise it is ".north".

`-highsuffix`

The value of this argument is appended to the node name of
the higher element of each cover drawn. When the flag
-no_northsouth is present the default value is the empty
string and otherwise it is ".south".

`-no_labels`

When this flag is provided no node labels are drawn
and instead each element is represented as a filled circle.
The default behavior is to draw node labels.

`-ptsize`

If the flag -no_labels is provided this specifies the size
of the circles drawn for elements. If the flag is not provided
this argument has no effect. The default value is "2pt".


`-debug`

If this flag is provided extra information is printed that
may be useful for debugging.

`-class`

The module provided as the first argument to hasse.py provides
a class, this argument specifies the name of the class.
The default value is the same as the module name.


# Modules

## chain
Usage: ```hasse.py chain -n RANK```

This module computes a chain of length RANK. The comments in this file serve
as documentation for how to provide your own module.

## booleanAlgebra

Usage: ```hasse.py booleanAlgebra -n RANK [-labels LABEL_CODE]```

This module computes the Boolean algebra of a specified rank n, that is, the poset of
all subsets of {1,...,n}. The argument -n specifies the rank of the Boolean algebra
to compute.

The optional argument -labels if provided should be the name of a
file containing python code to form the labels. In this code the variable ```i```
is the subset to make the label for. This set is encoded as a number with the
1 bits indicating the elements. The variable ```this``` is the booleanAlgebra
object. You should set the variable ```ret``` to the label as a string.
For an example see the file examples/booleanAlgebra/boxes.

## FpSubspaces

Usage: ```hasse.py FpSubspaces -n DIMENSION -p ORDER```

This module computes the lattice of subspaces of the vector space of dimension
DIMENSION over the prime field of order ORDER. The argument ORDER must be a prime.
Elements are displayed as the row spaces of matrices.

## ranked

Usage: ```hasse.py ranked INPUT```

This module computes a ranked poset from input describing the cover relations.
The argument INPUT may be a file name containing the input, if the file does not
exist INPUT itself is taken as the input. 

The input is formatted as follows. For each element other than the minimum, the
maximum, and the coatoms there is a cover list containing the indices of elements of
the next rank that cover it. The indices start at 1 and are seperated by commas.
For each rank, beginning at rank 1, the input contains the cover lists of each
element in the rank separated by semicolons. After the last cover list of each rank
there is another semicolon.
For example, the Boolean algebra of rank 3 is described as `1,2;1,3;2,3;;` when
the elements are ordered lexicographically.

## uncrossing

Usage: ```hasse.py uncrossing TOP_PAIRING [-bend BEND]```

This module computes lower intervals in the
[uncrossing poset](https://arxiv.org/pdf/1406.5671.pdf), a partial ordering
of pairings on a set {1,...,2n}. The argument TOP_PAIRING
specifies the maximum element in the form a1,b1,a2,b2,...,an,bn where ai and bi are
the pairs. For example, ```hasse.py uncrossing 1,4,2,5,3,6``` will produce a Hasse
diagram of the entire uncrossing poset of order 3.

The optional argument BEND is a parameter controlling how far the arcs are bent.
The default is 0.5. A value of 0 for BEND will produce straight lines for all
arcs.

## loi

Usage: ```hasse.py loi INPUT```

This module computes the lattice of lower order ideals of a given poset P described
in the file INPUT. The file INPUT describes the Hasse diagram of the poset P
via a series of commands separated by new lines. These commands are mapped to
tikz commands and are used to read off the poset P.

In each command arguments are enclosed between { and } with tikz options
enclosed between [ and ]. Lines beginning with #
are ignored. Lines beginning with \ are unchanged when mapped to tikz code.
To draw subsets of the diagram each command is stuck to some number of poset
elements, when drawing a subset commands stuck to elements not contained in
the subset are removed.

The commands are:

`draw[TIKZ_OPTIONS]{x}{y}{b1}{b2}`

Draws a line beteen tikz identifiers x and y,
ensures that x and y are elements of the poset P
and records the relation x<y.
The arguments b1 and b2 are each optional, if provided
these are the first and second control points to
draw a curved line between x and y.

A draw command is stuck to x and y.

`node[TIKZ_OPTIONS]{x}{y}{z}`

Creates a tikz node named x at location (y) with label z
and ensures that x is an element of the poset P.

A node command is stuck to x.

`coord[TIKZ_OPTIONS]{x}{y}`

Creates a tikz coordinate x at location (y)
and ensures that x is an element of the poset P.

A coord command is stuck to x.

`hide`

The last command will not produce any tikz code.
This can also be placed at the end of a draw command.

`stick{x1}...{xn}`

Sticks the last command to poset elements x1,...,xn.
This can also be placed at the end of a draw,node or coord command.

`scale{x}`

Sets the scale of the tikz picture to x.

`elem{x}`

Declares x as an element of the poset P.

## minor_poset

Usage: ```hasse.py minor_poset INPUT```

This module computes the [minor poset](https://arxiv.org/pdf/2205.01200.pdf) of a given generator-enriched lattice
and depicts the minors via an associated diagram analagous to Cayley graphs.
The file INPUT specifies the diagram of the generator-enriched lattice
using the same syntax as the input to loi.py.

