# SAT Solver
# Created by: Matej Aleksandrov, Jure Kukovec
# (c) March, 2016 
#
# Program for solving arbitrary SAT problem quite efficiently.


import time

class CNF:  #Entire SAT formula is stored in class CNF.
    
    def __init__(self,vnum,cnum):  #Initialization takes number of variables and number of clauses from dimacs form.
        
        self.state_var={i:True for i in range (vnum)}      # Contains variables which are not yet determined. 
        self.state_clauses={i:True for i in range (cnum)}  # Contains clauses which are not yet solved.
        self.var={}
        self.var[True]=[{} for i in range (vnum)]          # Stores connections between non-negated variables and clauses.
        self.var[False]=[{} for i in range (vnum)]         # Stores connections between negated variables and clauses.
        self.clauses=[]                                    # Stores connections between clauses and variables.
        self.sol=[True for i in range (vnum)]              # Stores solutions.
        self.hist=[]                                       # Stores history for backtracking
        self.end_var=[]                                    # Waiting list for variables that can be determined.
        self.end_clauses=[]                                # Waiting list for clauses that can be solved.

    def add(self, c): # Adds clause c to formula.
        
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

    def prepare(self): # Prepares formula before the start of satSolver()
        for v in self.state_var.keys():
            if len(self.var[False][v])==0 or len(self.var[True][v])==0:
                if len(self.var[False][v])==0:
                    self.end_var.append((v,True))
                else:
                    self.end_var.append((v,False))
        for c in self.state_clauses.keys():
            if len(self.clauses[c])<=1:
                self.end_clauses.append(c)
        
    
    def __repr__(self):     # Informative representation used during coding.
        s='------------------\n'
        s+=str(self.state_var)+'\n'
        s+=str(self.state_clauses)+'\n'
        s+=str(self.var)+'\n'
        s+=str(self.clauses)+'\n'
        s+=str(self.sol)+'\n'
        s+=str(self.end_var)+'\n'
        s+=str(self.end_clauses)+'\n'
        s+='------------------'
        return s

    def set_val(self,v,b):  # Method for setting value b to variable v.
        del self.state_var[v]
        self.hist.append((0,v))
        self.sol[v]=b
        for c in self.var[b][v].keys():
            try:
                del self.state_clauses[c]
                self.hist.append((1,c))
                for u in self.clauses[c].keys():
                    if u!=v:
                        b0=self.clauses[c][u]
                        del self.var[b0][u][c]
                        self.hist.append((2,b0,u,c))
                        if len(self.var[b0][u])==0 and len(self.var[not b0][u])!=0:
                            self.end_var.append((u,not b0))
            except:
                pass
        for c in self.var[not b][v].keys():
            del self.clauses[c][v]
            self.hist.append((3,c,v,not b))
            if len(self.clauses[c])<=1:
                self.end_clauses.append(c)

    def undo(self,h):   # Method that undoes history of algorithm.
        self.end_var=[]
        self.end_clauses=[]
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
        # Very important method which determines which variable will be chosen next for recursion.
        # Currently takes the variable that is present in most number of unsolved clauses out all undetermined variables.
        m=-1
        for v in self.state_var.keys():
            m1=len(self.var[True][v])
            m2=len(self.var[False][v])
            if m1+m2>m:
                m=m1+m2
                u=v
                t=(m1>m2)
        return (t,u)

      
def satSolver(cnf):
    # Function where the recursive algorithm runs.
    # Each step algorthm makes (some sort of) DFS search for determening all variables and clauses that can be trivially
    # solved. After that it makes a guess about the value of some variable and recursively repeats itself.  
    
    while len(cnf.end_var)>0 or len(cnf.end_clauses)>0: # Here DFS runs.
        while len(cnf.end_var)>0:
            v,b=cnf.end_var[-1]
            cnf.end_var.pop()
            if cnf.state_var.get(v)==None:
                if cnf.sol[v]!=b: # If we reach a contradiction.
                    return None  
            else:
                cnf.set_val(v,b)

        while len(cnf.end_clauses)>0:
            c=cnf.end_clauses[-1]
            cnf.end_clauses.pop()
            if cnf.state_clauses.get(c)!=None:
                if len(cnf.clauses[c])==0: # If we reach a contradiction.
                    return None
                del cnf.state_clauses[c]
                cnf.hist.append((1,c))
                v=list(cnf.clauses[c])[0]
                b=cnf.clauses[c][v]
                if cnf.state_var.get(v)==None:
                    if cnf.sol[v]!=b: # If we reach a contradiction.
                        return None
                else:
                    cnf.set_val(v,b)

    if len(cnf.state_var)==0: # In case we have found the solution.
        return dimacsOutput(cnf)
    
    b,v=cnf.select()
    h=len(cnf.hist)   # Remembers current size of history list.
    cnf.set_val(v,b)  # We set value b to variable v.
    
    y=satSolver(cnf)
    if y!=None: # In case we have found the solution.
        return y

    cnf.undo(h)  #Undoes history.
    cnf.set_val(v,not b)
    return satSolver(cnf)

        
def dimacsInput(pfile):  # Function that transforms SAT from Dimacs form to CNF class, input is file name.
    f=open(pfile,'r')
    s = []
    for line in f:
        if line[0]=='p':
            s=line.strip().split()
            cnf=CNF(int(s[2]),int(s[3]))
            s = []
        elif line[0]!='c':
            s += line.strip().split()
            if s[-1] != '0':
                continue
            
            for j in range (len(s)-1):
                if s[j][0]=='-':
                    s[j]=(False,int(s[j][1:])-1)
                else:
                    s[j]=(True,int(s[j])-1)
            cnf.add(s[:-1])
            s = []
    f.close()
    return cnf

def dimacsOutput(cnf): # Function that creates output string from CNF class in case solution is found.
    s=''
    for i in range (len(cnf.sol)):
        if cnf.sol[i]:
            s+=str(i+1)+' '
        else:
            s+=str(-(i+1))+' '
    return s.strip()

'''
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
    return t'''

def solve(x=0):
    #Main function for running SAT solver.
    #Input can be: - string as the name of the file, e.g. solve('fileName.txt'),
    #              - number which is index the file in array samples below. 

    samples=['test1','test2','sudoku1','sudoku2',
              'bf0432-007', 'aim-100-1_6-no-1', 'aim-50-1_6-yes1-4', 'zebra_v155_c1135']
    if str(x)==x:
        pfile=x
    else:
        pfile='Samples/'+samples[x]+'.txt'

    t = time.time()
    cnf = dimacsInput(pfile)
    cnf.prepare()
    ans=satSolver(cnf)
    if ans==None:
        ans='NOT SATISFIABLE'
    t = time.time() - t

    outName = pfile[:-4]+'_solution.txt'

    print('Answer found in {} seconds. Written to: {}'.format(t,outName))

    f = open(outName,'w')
    print(ans,file=f)
    f.close()

