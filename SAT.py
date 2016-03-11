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
            raise Exception("Multiple valuation exception. " +  pAtom.name + " has already been assigned a value." )
        self.assigned[ pAtom.name ] = pAtom.isTrue
        

class CNF:
    def __init__(self):
        self.clauses = []
        self.saved = []
    def add( self, pClause ) :
        #maintain sorted clauses (by length)
        bisect.insort( self.clauses, pClause )
    def save(self):
        self.saved = self.clauses
    def load(self):
        self.clauses = self.saved
    def addUnit(self, pName, pIsTrue):
        c = Clause()
        c.add(Atom( pName, pIsTrue ))
        self.clauses.insert(0,c)
    def clearUnits(self, pValuation):
        if not self.clauses:
            return
        newUnits = []
        while self.clauses and self.clauses[0].isUnit():
            clause = self.clauses.pop(0)
            newUnits.append( clause.atoms[0] )
            pValuation.add( clause.atoms[0] )
        newUnits.sort()
        if not newUnits:
            return
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
                
            
            
    def isNonSat(self):
        for clause in self.clauses:
            if clause.isNotSat():
                return True
        return False

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
    b= Valuation()
    a.clearUnits(b)

    
