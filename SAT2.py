import time
import random

class CNF:
    def __init__(self,vnum,cnum):  #number of variables, number of clauses
        self.state_var={i:True for i in range (vnum)}
        self.state_clauses={i:True for i in range (cnum)}
        self.var={}
        self.var[True]=[{} for i in range (vnum)]
        self.var[False]=[{} for i in range (vnum)]
        self.clauses=[]
        self.sol=[True for i in range (vnum)]
        self.hist=[]

    def add(self, c): # adds clause c
        n=len(self.clauses)
        self.clauses.append({})
        t=False
        for i in range (len(c)):
            if not t:
                if self.clauses[n].get(c[i][1])==None:
                    self.clauses[n][c[i][1]]=c[i][0]
                elif self.clauses[n].get(c[i][1])!=c[i][0]:
                    t=True
                    self.clauses[n]={}
                    del self.state_clauses[n]
        for v in self.clauses[n].keys():
            self.var[self.clauses[n][v]][v][n]=True

    def __repr__(self):
        s=str(self.state_var)+'\n'
        s+=str(self.state_clauses)+'\n'
        s+=str(self.var)+'\n'
        s+=str(self.clauses)+'\n'
        s+=str(self.sol)
        return s

    def set_val(self,b,v,c0=-1):
        del self.state_var[v]
        self.hist.append((0,v))
        self.sol[v]=b
        for c in self.var[b][v].keys():
            try:
                del self.state_clauses[c]
                self.hist.append((1,c))
                for u in self.clauses[c].keys():
                    if u!=v:
                        del self.var[self.clauses[c][u]][u][c]
                        self.hist.append((2,self.clauses[c][u],u,c))
            except:
                pass
        for c in self.var[not b][v].keys():
            del self.clauses[c][v]
            self.hist.append((3,c,v,not b))

    def undo(self,h):
        while len(self.hist)>h:
            g=self.hist[-1]
            if g[0]==0:
                self.state_var[g[1]]=True
            if g[0]==1:
                self.state_clauses[g[1]]=True
            if g[0]==2:
                self.var[g[1]][g[2]][g[3]]=True
            if g[0]==3:
                self.clauses[g[1]][g[2]]=g[3]
            self.hist.pop()
        
    def select(self):
        return (random.choice([True,False]),random.choice(list(self.state_var.keys())))
        
        
def satSolver(cnf):
    if len(cnf.state_var)==0:
        return dimacsOutput(cnf)
    t=True
    while t:  #trivial simplifications
        t=False
        for v in list(cnf.state_var.keys()):
            l1=len(cnf.var[False][v])
            l2=len(cnf.var[True][v])
            if (l1==0 and l2>0) or (l1>0 and l2==0):
                t=True
            if l1==0:
                cnf.set_val(True,v)
            elif l2==0:
                cnf.set_val(False,v)
                        
        for c in list(cnf.state_clauses.keys()):
            if len(cnf.clauses[c])==0:
                return None
            if len(cnf.clauses[c])==1:
                t=True
                try:
                    del cnf.state_clauses[c]
                    cnf.hist.append((1,c))
                    for v in cnf.clauses[c].keys():
                        cnf.set_val(cnf.clauses[c][v],v)
                except:
                    pass

    #print('after simplification')
    #print(cnf)
    if len(cnf.state_var)==0:
        return dimacsOutput(cnf)
    
    b,v=cnf.select()
    h=len(cnf.hist)
    cnf.set_val(b,v)
    y=satSolver(cnf)
    if y!=None:
        return y
    cnf.undo(h)
    #print('after undo')
    #print(cnf)
    cnf.set_val(not b,v)
    return satSolver(cnf)

        
def dimacsInput(pFile):  # transforms SAT from Dimacs form to CNF class, input is file name
    f=open(pFile,'r')
    for line in f:
        if line[0]=='p':
            s=line.strip().split()
            cnf=CNF(int(s[2]),int(s[3]))
        elif line[0]!='c':
            s=line.strip().split()
            for j in range (len(s)-1):
                if s[j][0]=='-':
                    s[j]=(False,int(s[j][1:])-1)
                else:
                    s[j]=(True,int(s[j])-1)
            cnf.add(s[:-1])
    f.close()
    return cnf

def dimacsOutput(cnf):
    s=''
    for i in range (len(cnf.sol)):
        if cnf.sol[i]:
            s+=str(i+1)+' '
        else:
            s+=str(-(i+1))+' '
    return s.strip()


def check(name,ans): #compares my output to correct output
    pfile='Samples/'+name+'_solution.txt'
    f=open(pfile,'r')
    t= ''
    for line in f:
        s=line.strip()
        if s==ans:
            t='Answer is correct.'
        else:
            t='Answer is incorrect or there are multiple solutions.'
    f.close()
    return t
    
    

def solve(n=0): #
    tests=['test1','sudoku1','sudoku2'] #list of test files
    tests += ['bf0432-007', 'aim-100-1_6-no-1', 'aim-50-1_6-yes1-4' ] #source> http://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html
    
    pfile='Samples/'+tests[n]+'.txt'
    t = time.time()
    cnf = dimacsInput(pfile)
    ans=satSolver(cnf)
    t = time.time() - t

    print('Answer:')
    print(ans)

    f = open(pfile[:-4]+'_solution.txt','w')
    print(ans,file = f)
    
    print('Time in seconds:')
    print(t)

    print(check(tests[n],ans))

def solveFile( fname ): # file should end in .txt
    t = time.time()
    cnf = dimacsInput(fname)
    ans=satSolver(cnf)
    t = time.time() - t

    outName = fname[:-4]+'_solution.txt'


    print('Answer found in {} seconds. Written to: {}'.format(t,fname))

    f = open(outName,'w')
    print(ans if ans != None else "NOT SATISFIABLE" ,file = f)    
