# Can a white king be placed, that is not in check ?
# pijn = (i,j) th field is figure n,
# n vals:
##    0 - white king
##    1 - black queen
##    2 - EMPTY
## ri : exists 

nPcs = 2

def generalCNF( boardDim ): 
    clauses = []
    # each field has a piece
##    for i in range(boardDim):
##        for j in range(boardDim):
##           clauses.append(["p{}{}{}".format(i,j,n) for n in range(nPcs)])

    #each field has at most 1 piece
    for i in range(boardDim):
        for j in range(boardDim):
            for n in range(nPcs):
                for n2 in range(n+1,nPcs):
                    clauses.append(["-p{}{}{}".format(i,j,n), "-p{}{}{}".format(i,j,n2)])
    
##    clauses.append(["r{}".format(i) for i in range(boardDim)]) # each col has wk
##    clauses.append(["c{}".format(i) for i in range(boardDim)]) # each row has wk

##    or i in range(boardDim):
##        for n in range(nPcs):
##            for j in range(boardDim):
##                for j2 in range(j+1,boardDim):
##                    clauses.append(["r{}".format(i) for i in range(boardDim)]) # each col has wk

    clauses.append( [ "p{}{}0".format(i,j) for i in range(boardDim) for j in range(boardDim) ] ) # at least 1 wk

    #at most 1 wk
    for i in range(boardDim):
        for j in range(boardDim):
            for i2 in range(boardDim):
                for j2 in range(boardDim):
                    if (i,j) == (i2,j2):
                        continue
                    clauses.append(["-p{}{}0".format(i,j), "-p{}{}0".format(i2,j2)])

    #not check as rook
    for i in range(boardDim):
        for j in range(boardDim):
           p0 = "-p{}{}0".format(i,j)
           for t in range(boardDim):
               if t != i:
                   clauses.append([p0,"-p{}{}1".format(t,j)])
               if t != j:
                   clauses.append([p0,"-p{}{}1".format(i,t)])

    #not check as bishop
    for i in range(boardDim):
        for j in range(boardDim):
           p0 = "-p{}{}0".format(i,j)
           s1 = i + j
           s2 = i - j
           for t in range( boardDim ):
               i2 = t
               j2 = s1 - t
               if t != i and 0 <= j2 and j2 < boardDim: 
                   clauses.append([p0,"-p{}{}1".format(i2,j2)])
               i3 = t
               j3 = t - s2
               if t != i and 0 <= j3 and j3 < boardDim: 
                   clauses.append([p0,"-p{}{}1".format(i3,j3)])
              
               
    return clauses
              
           

    
def produceDIMACS( queens,  outFileName, boardDim = 8 ): #i, j = white king pos
    clauses = generalCNF(boardDim)
    # add specifics from queens pos
    for (i,j) in queens:
        clauses.append(["p{}{}1".format(i,j)])

    nvars = 2 * boardDim**2
    nclauses = len(clauses)

    f = open(outFileName,'w')
    print( "p cnf {} {}".format(nvars, nclauses), file = f )
    for clause in clauses:
        #print(clause)
        for s in clause:
            neg = False
            if s[0]=='-':
                neg = True
                s = s[1:]
            ID = 1 + ( int(s[1]) + int(s[2]) * boardDim ) + (boardDim**2) * int(s[3])
            ID *= -1 if neg else 1
            print( ID , file = f, end = " ")
        print(0 , file = f)

def test():
    fName = "testDIMACS.txt"
    dim = 4
    queens = [(0,0),(1,1)]
    produceDIMACS(queens, fName, dim )
                    

                
            
        
    
