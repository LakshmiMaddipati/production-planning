import numpy as np
import pandas as pd

def simplex_tableau(cost_var, variables, A, BV, count, phase):    
    cost_basicvar  = [cost_var[x] for x in BV]    
    initial_bv = BV[:]
    zjcj = np.dot(cost_basicvar,A) - list(cost_var.values())    

    table = np.vstack((zjcj,A))   
   
    indexvar = [x for x in variables if x in BV]
    
    indexvar.insert(0,"z")
    newindex = indexvar[:]
    df = pd.DataFrame(data=table, index=indexvar, columns=variables)
    
    rowlen = zjcj.shape[1]
    Run = True
    while Run:       
        ZC = np.delete(zjcj, rowlen-1, axis=1)  
        ZCarray = np.squeeze(np.asarray(ZC))     
       
        if len(list(set(df.index.to_list()) & set(originalBV)))!=0 : #np.any([element >0 for element in ZCarray]):  
            print("Current LP solution is not optimal")             

            newdf = df.drop(df.columns[len(df.columns)-1], axis=1)
            #Z is always the index for cost variables row and checking for max reduced cost
            pivot_col = newdf.loc["z"].idxmax()   

            if (df[pivot_col] < 0).sum().sum() == df.shape[0]:
                print("Lp is unbounded")
            else: 
                print("LP is bounded")      
                df["Ratio"] = df.apply(lambda x:x["RHS"]/x[pivot_col] if x[pivot_col]>0 else float('inf'), axis=1)             
                df_dummy = df.drop('z')                            
                leaving_row = df_dummy['Ratio'].idxmin() 
            
            
            print("Iteration - "+ str(count)+" :" + str(leaving_row) + " is leaving the basis and "+ str(pivot_col)+" entering the basis")            
            
            newindex=[pivot_col if x==leaving_row else x for x in newindex]
            
            
            ##updating the BFS

            BV=[pivot_col if x==leaving_row else x for x in BV]
            
            leaving_row_index = [i for i, item in enumerate(variables) if item in leaving_row]
            pivot_col_index = [i for i, item in enumerate(variables) if item in pivot_col]             
            
            pvt_key = df.loc[leaving_row]
            pvt_key = pvt_key.loc[pivot_col]
            
            df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)
            df.loc[leaving_row] = df.loc[leaving_row]/pvt_key
            df["index"]=newindex
            #print(newindex, "index before 2nd df")
            df = df.set_index("index")    
            
            #updating the entries

            for index, row in df.iterrows(): 
                if index!=pivot_col:                
                    df.loc[index] = df.loc[index] - (df.loc[index]).loc[pivot_col]*df.loc[pivot_col]        
                       
            zjcj = zjcj - np.dot(zjcj[0,pivot_col_index],df.loc[[pivot_col]])  
            count+=1              
            #df=df.round(3)            
        else:
            Run = False
            print("Current LP solution is optimal") 
                     
            if phase == "one":         
                ### checking for infeasibility 
                infeasibledf = df.head(1).drop("RHS", axis=1)
                costvar_list = infeasibledf.iloc[0].to_list()   
                if all(v == 0 for v in costvar_list):
                    print("The Lp problem is infeasible")
                else:
                    print("The Lp problem is Feasible")
                ###checking for redundancy
                redundancy = [v in df.index for v in initial_bv]                
                if any(redundancy):
                    print("There are redundant varaibles in this LP")
                   
                    df =  df.drop(redundancy)
                   
                    print("All redundant constraints have been removed from this LP")
                else:
                    print("No redundant constraints are present in this LP")                     
                    
            else:
                pass    
            
                     
            finaldf.to_csv("C:/Users/prasa/OneDrive/Documents/ML_HW4/phaseprod.csv")         
           
    return df
       
variables = ["P11","P12","P13","P21","P22","P23","P31","P32","P33","S1","S2","S3","S4","S5","S6","S7","S8","S9","A1","A2","A3","A4","A5","A6","A7","A8","A9","RHS"]
#opti_variables = ["F1","F2","F3","S1","S2","S3","RHS"]
original_costvar = {"P11":-385,"P12":-330,"P13":-275,"P21":-385,"P22":-330,"P23":-275,"P31":-385,"P32":-330,"P33":-275,"S1":0,"S2":0,"S3":0,"S4":0,"S5":0,"S6":0,"S7":0,"S8":0,"S9":0,"A1":1,"A2":1,"A3":1,"A4":1,"A5":1,"A6":1,"A7":1,"A8":1,"A9":1,"RHS":0}
basic_var = range(11, 17) #corresponding to A1,A2,A3
BV = ["A1","A2","A3","A4","A5","A6","A7","A8","A9"]
originalBV = BV[:]
initial_matrix = np.matrix([[1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,750],
                            [0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,900],
                            [0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,450],
                            [12,15,20,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,13000],
                            [0,0,0,12,15,20,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,12000],
                            [0,0,0,0,0,0,12,15,20,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,5000],
                            [1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,750],
                            [0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1200],
                            [0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,900],
                            ])
b = np.matrix([750,900,450, 13000,12000,5000,750,1200,900])
count = 0

print("************Phase 1 begins***************")

cost_var = {"P11":0,"P12":0,"P13":0,"P21":0,"P22":0,"P23":0,"P31":0,"P32":0,"P33":0,"S1":0,"S2":0,"S3":0,"S4":0,"S5":0,"S6":0,"S7":0,"S8":0,"S9":0,"A1":1,"A2":1,"A3":1,"A4":1,"A5":1,"A6":1,"A7":1,"A8":1,"A9":1,"RHS":0}

A = initial_matrix 
starting_basicsvar = [x for x in list(cost_var.values()) if x<0]

basicsfeasibledf = simplex_tableau(cost_var, variables,A, BV, count, phase="one")
BFS = basicsfeasibledf.index

print("************Phase 1 ends and Phase 2 begins***************")

###removing artifical varaibles from the problem
BFS = [x for x in BFS if x!="z"]
variables_P2 = [x for x in variables if x not in BV]
A_P2 = basicsfeasibledf.drop(columns=BV)

A_P2 =A_P2.drop("z")
A_P2 = np.asmatrix(A_P2.values)

cost_var_P2 = {key: val for key, val in original_costvar.items() if key not in BV}
#cost_var_P2.update((x, -y) for x, y in cost_var_P2.items())


OptimalBFS = simplex_tableau(cost_var_P2, variables_P2,A_P2, BFS, count, phase="two")