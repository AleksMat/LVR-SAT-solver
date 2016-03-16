import bisect

class Atom:
    def __init__(self, pName, pIsTrue):
        self.name = pName
        self.isTrue = pIsTrue
    def toggle(self):
        self.isTrue = not self.isTrue
    def __lt__(self, other):
        if self.name < other.name:
            return True
        elif self.name == other.name:
            return self.isTrue
        return False
    def __eq__(self, other):
        return self.name == other.name and self.isTrue == other.isTrue
    def __repr__(self):
        return "{}{}".format(  "" if self.isTrue else "NOT ", self.name )

class Clause:
    def __init__(self):
        self.atoms = []
    def add( self, pAtom ) :
        #maintain sorted atoms (by name) for fast removal
        bisect.insort( self.atoms, pAtom )
    def isNonSat(self):
        return not self.atoms
    def isUnit(self):
        return len(self.atoms) == 1
    def __lt__(self, other):
        return len(self.atoms) < len(other.atoms)
    def __repr__(self):
        return "( " + " OR ".join([at.__repr__() for at in self.atoms ]) + " )"

class Valuation:
    def __init__(self):
        self.assigned = dict()
        self.saved = dict()
    def save(self):
        self.saved = self.assigned
    def load(self):
        self.assigned = self.saved
    def add( self, pAtom ):
        if( pAtom.name in self.assigned ):
            return
            #raise Exception("Multiple valuation exception. " +  pAtom.name + " has already been assigned a value." )
        self.assigned[ pAtom.name ] = pAtom.isTrue
        

class CNF:
    def __init__(self):
        self.clauses = []
        self.guessHistory = []
    def add( self, pClause ) :
        #maintain sorted clauses (by length)
        bisect.insort( self.clauses, pClause )
    def prepareForNewGuess(self):
        self.guessHistory.append(self.clauses)
    def undoGuess(self):
        if not self.guessHistory:
            raise Exception( "" )
        self.clauses = self.guessHistory.pop()
    def addUnit(self, pName, pIsTrue):
        c = Clause()
        c.add(Atom( pName, pIsTrue ))
        self.clauses.insert(0,c)
    def clearUnits(self, pValuation):
        if not self.clauses:
            return False
        newUnits = []
        while self.clauses and self.clauses[0].isUnit():
            clause = self.clauses.pop(0)
            newUnits.append( clause.atoms[0] )
            pValuation.add( clause.atoms[0] )
        newUnits.sort()
        if not newUnits:
            return False
        tbd = []
        for i in range(0,len(self.clauses)):
            otherClause = self.clauses[i]
            nUnitIndex = 0
            index = bisect.bisect( otherClause.atoms, newUnits[0] )
            while( nUnitIndex < len(newUnits) and index < len(otherClause.atoms) ):
                if otherClause.atoms[index].name < newUnits[nUnitIndex].name:
                    index += 1
                elif otherClause.atoms[index].name == newUnits[nUnitIndex].name:
                    if( otherClause.atoms[index].isTrue == newUnits[nUnitIndex].isTrue ):
                        #remove whole clause (mark for deletion)
                        tbd.append(i);
                        break;
                    else:
                        #remove negated atom
                        otherClause.atoms.pop(index)
                else :
                    # end matching for the current new unit
                    nUnitIndex += 1
        #remove marked clauses
        while tbd:
            self.clauses.pop( tbd.pop() )

        return True
                
            
            
    def isNonSat(self):
        for clause in self.clauses:
            if clause.isNotSat():
                return True
        return False
    def __repr__(self):
        return "[ " + " AND ".join([cl.__repr__() for cl in self.clauses ]) + " ]"

class SATSolver:
    def __init__(self):
        pass
    def __call__( self, pCNF ):
        retVal = Valuation()
        ## DO STUFF

        return retVal

def test():
    a = CNF()
    a.addUnit("q",True)
    a.addUnit("s",True)
    c = Clause()
    c.add( Atom("p",True) )
    c.add( Atom("r",True) )
    c.add( Atom("s",False) )

    a.add( c )
    print("a before clear: {}".format(a))

    
    b= Valuation()
    a.clearUnits(b)

    print("a after clear: {}".format(a))


def dimacsTransformer(file):  # transforms SAT from Dimacs form to CNF class, input is file name
    f=open(file,'r')
    cnf=CNF()
    num=0
    for line in f:
        if num>=3:
            c=Clause()
            s=line.strip().split()
            for j in range (len(s)-1):
                if s[j][0]=='-':
                    c.add( Atom(s[j][1:],False))
                else:
                    c.add( Atom(s[j],True))
        num+=1
    f.close()
    return cnf

dimacsTransformer('Samples/sudoku1-2.txt')
#dimacsTransformer('Samples/sudoku2.txt')
    
