# coding=utf-8
import sys
import itertools
from z3 import *
			
def maxArea(val):
	n = 0;
	for i in range(xx):
		for j in range(yy):
			if (Board[i][j] == val):
				n = n+1
	return n

def getArea(a, b):
	area = []
	for i in range(xx):
		for j in range(yy):
			if Board[i][j]==Board[a][b]:
				area.append(cells[i][j])
	return area;

def getRows (v, x, y):
	row = []
	for i in range (limitX(x+1), limitX(x+v+1)):
		if (vals[i][y] == '.'):
			row.append(cells[i][y])
	for i in range (limitZ(x-v), x):
		if (vals[i][y] == '.'):
			row.append(cells[i][y])
	return row, v

def getCols (v, x, y):
	col = []
	for i in range (limitY(y+1), limitY(y+v+1)):
		if (vals[x][i] == '.'):
			col.append(cells[x][i])
	for i in range (limitZ(y-v), y):
		if (vals[x][i] == '.'):
			col.append(cells[x][i])
	return col, v

def limitX (k):
	if (k>xx):
		return xx
	else:
		return k

def limitZ (k):
	if (k<0):
		return 0
	else:
		return k

def limitY (k):
	if (k>yy):
		return yy
	else:
		return k


def checkSat (sol):
	if s.check() == sat:
		return 1
	else:
		return 0

def printCheckedBoard (m):
	print "   ",
	for y in range(yy):
		print str(unichr(65+y)),
	print("\n")
	for x in range(xx):
		print x+1,'|',
		for y in range(yy):
			print m.evaluate(cells[x][y]),
		print '\n'

def printBoard ():
	print "   ",
	for y in range(yy):
		print str(unichr(65+y)),
	print("\n")
	for x in range(xx):
		print x+1,'|',
		for y in range(yy):
			print vals[x][y],
		print '\n'
	print "------------------\n   ",
	for y in range(yy):
		print str(unichr(65+y)),
	print("\n")
	for x in range(xx):
		print x+1,'|',
		for y in range(yy):
			print Board[x][y],
		print '\n'

def pos2num (opt):
	if len(opt) != 4:		
		return 0,0,0,0
	elif ord(opt[0]) < 65 or ord(opt[0]) > 65+yy:
		return 0,0,0,0
	elif int(opt[1]) < 1 or int(opt[1]) > xx:
		return 0,0,0,0
	x = ord(opt[0])-65
	y = int(opt[1])-1
	v = int(opt[3])
	if int(opt[3]) < 1 or int(opt[3]) > maxArea(Board[y][x]):
		ret = 2
	elif vals[y][x] != '.':
		ret = 3
	else:
		ret = 1
	return ret,x,y,v

def solvePuzzle ():
	s = Solver()

	#Converts chars to ints in arrays
	#Starts adding asserts to solver
	for y in range(0,xx):
		for x in range(0,yy):
			Board[y][x] = int(Board[y][x])
			if vals[y][x] != '.':
				vals[y][x] = int(vals[y][x])
				s.add(cells[y][x] == vals[y][x])

	# Add cell constraints
	for x in range(xx):
		for y in range(yy):
		    s.add(And(1 <= cells[x][y], cells[x][y] <= maxArea(Board[x][y])))

	# Add group constraints
	for x in range(xx):
		for y in range(yy):
		    s.add(Distinct(getArea(x,y)))


	# Add column/row constraints
	for x in range(xx):
		for y in range(yy):
			if vals[x][y] != '.':
				row, v = getRows(vals[x][y], x, y)
				for l in range (len(row)):
					s.add(row[l] != v)
				col, v = getCols(vals[x][y], x, y)
				for l in range (len(col)):
					s.add(col[l] != v)
			else :
				for i in range (1, 1 + maxArea(Board[x][y])):
					row, v = getRows(i, x, y)
					for l in range (len(row)):
						#print 'Se', cells[x][y], '==', i, 'entao', row[l], '!=', v
						s.add(Implies(cells[x][y] == i, row[l] != v))
					col, v = getCols(i, x, y)
					for l in range (len(col)):
						#print 'Se', cells[x][y], '==', i, 'entao', col[l], '!=', v
						s.add(Implies(cells[x][y] == i, col[l] != v))
	return s

def checkFim():
	for i in range(0,xx):
		for j in range(0,yy):
			if vals[i][j]=='.':
				return 0
	return 1

def save2file (s):
	f = open('asserts-' + sys.argv[1],'w')
	for a in s.assertions():
		f.write(str(a)+'\n')
	f.close()
#-------------------------------------#
#Code starts here. Above only methods.#
#-------------------------------------#

#Read board from file to array:
f = open(sys.argv[1], "rU")
d = f.readlines()
i = 0
Board = []
vals = []
if (d[i]=="areas\n"):
	try:
		while (d[i+1]!="board\n"):
			Board.append(d[i+1].split())
			i = i+1
		i = i+1
		while (d[i+1]!="END"):
			vals.append(d[i+1].split())
			i = i+1
	except (RuntimeError, TypeError, NameError, IndexError):
		print "Algum problema com o tabuleiro (ficheiro de input)"
		sys.exit()
f.close()

xx = len(Board) #Width of the Board
yy = len(Board[0]) #Height of the Board

# Create Z3 integer variables for matrix cells
cells = [ [ Int("h_%s_%s" % (i+1, j+1)) for j in range(yy) ] for i in range(xx) ]

menu = 1

while menu:
	opt = raw_input("Bem-vindo ao Jogo do Hadoku!\n\nO que pretende fazer? [j=jogar, r=resolver, outra=sair]: ");
	if (opt=='r'):
		s = solvePuzzle()
		if checkSat(s):
			m = s.model()
			print "Modelo encontrado:"
			printCheckedBoard(m)
			print "Verifique a pasta pelo ficheiro com as asserções!"
			save2file(s)
		else:
			print "Impossivel de resolver"
		menu = 0
	elif opt=='j':
		game = 1
		while game:
			printBoard()
			opt = raw_input("Próximo movimento [p.ex. B3-2] (s=sair) (d=desistir): ");
			if opt=='s':
				game = 0
			elif opt=='d':
				s = solvePuzzle()
				if checkSat(s):
					m = s.model()
					print "Modelo encontrado:"
					printCheckedBoard(m)
					print "Verifique a pasta pelo ficheiro com as asserções!"
					save2file(s)
				else:
					print "Impossivel de resolver"
				game = 0
				menu = 0
			else:
				ret,x,y,v = pos2num(opt)
				if ret==1:
					aux = vals[y][x]
					vals[y][x] = v
					s = solvePuzzle()
					if checkSat(s):
						print "Boa jogada! :)\n"
						if checkFim():
							print "||| Parabéns!! Completou o Puzzle!! |||\n"
							m = s.model()
							printCheckedBoard(m)
							game = 0
							menu = 0
					else:
						print "Mal Jogado :(\n"
						vals[y][x] = aux
				elif ret==2:
					print "Valor demasiado alto para a posição!"
				elif ret==3:
					print "Posição com valor já correto!"
				else:
					print "Posição Inválida!"
	else:
		print "Até à próxima!!"
		menu = 0
