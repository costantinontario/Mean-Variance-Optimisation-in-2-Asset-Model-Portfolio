# Import Required Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to conduct Mean Variance Optimisation on Given Data
def Minimisation(File,Weight_Detail,Cost_A,Cost_B,Initial_Investment):
    
    #Load csv with Websites on the dataframe
    Data = pd.read_csv(File)
    
    # Calculate Daily Returns for Assets A & B using Vectoring
    Data['Returns_'+str(Data.columns[1])+'_(%)'] = (Data[Data.columns[1]] / Data[Data.columns[1]].shift(1) - 1) * 100
    Data['Returns_'+str(Data.columns[2])+'_(%)'] = (Data[Data.columns[2]] / Data[Data.columns[2]].shift(1) - 1) * 100
    
    # Replace NANs with zeros in first line (since there are no returns in the first period)
    Data['Returns_'+str(Data.columns[1])+'_(%)'].fillna(0, inplace=True)
    Data['Returns_'+str(Data.columns[2])+'_(%)'].fillna(0, inplace=True)

    #Calculate Covariance Matrix
    Covariance_Matrix = np.cov(Data['Returns_'+str(Data.columns[1])+'_(%)'],Data['Returns_'+str(Data.columns[2])+'_(%)'])
    
    
    # Create DataFrame containing all possible weights and resulting Variances
    index = np.arange(1 / Weight_Detail) 
    columns = ['Weight_'+str(Data.columns[1]),'Weight_'+str(Data.columns[2]),'Variance']
    Iteration_Matrix = pd.DataFrame(columns=columns, index = index)
    
    # Determine Initial Weight of Asset A
    Iteration_Matrix['Weight_'+str(Data.columns[1])][0] = 0
    
    for i in range(0,2000):
        
        # In period 0 the weight of asset A is already defined at 0 and hence cannot be calculated with the following formula
        if i > 0:
            
            # Determine weight of Asset A
            Iteration_Matrix['Weight_'+str(Data.columns[1])][i] = Iteration_Matrix['Weight_'+str(Data.columns[1])][i-1] + Weight_Detail
        
        # Determine Weight of Asset B
        Iteration_Matrix['Weight_'+str(Data.columns[2])][i] = 1 - Iteration_Matrix['Weight_'+str(Data.columns[1])][i]
        
        # Calculate Variance of Portfolio with specific Weights
        Iteration_Matrix['Variance'][i] = Iteration_Matrix['Weight_' + str(Data.columns[1])][i] * (Iteration_Matrix['Weight_' + str(Data.columns[1])][i] * Covariance_Matrix[0,0] + \
                Iteration_Matrix['Weight_'+ str(Data.columns[2])][i] * Covariance_Matrix[0,1]) + Iteration_Matrix['Weight_' + str(Data.columns[2])][i] * (Iteration_Matrix['Weight_' + \
                str(Data.columns[1])][i] * Covariance_Matrix[1,0] + Iteration_Matrix['Weight_' + str(Data.columns[2])][i] * Covariance_Matrix[1,1])
        
        # Determinine the weight of Asset A that minimises Variance
        try:
            
            # If the Variance in the current period is smaller than the Variance in the previous period
            if Iteration_Matrix['Variance'][i] < Iteration_Matrix['Variance'][i-1]:
                
                # Store the weights that minimise Variance
                Optimal_WeightA = Iteration_Matrix['Weight_'+str(Data.columns[1])][i]
                Optimal_WeightB = 1 - Optimal_WeightA
                Optimal_Variance = Iteration_Matrix['Variance'][i]
                
        except:
            pass
    
    # Display Results of Optimisation (Optimal Weight for the two Assets along with the Minimum Variance)
    print '--------------- Mean Variance Optimisation ---------------'
    print 'Variance of Portfolio is minimised with the following distribution - ' + str(Data.columns[1]) + ': ' + str(Optimal_WeightA*100) + '% and ' + \
    str(Data.columns[2]) + ': ' + str(Optimal_WeightB*100) + '%, with Variance: ' + str(Optimal_Variance)
    
    # Plot Efficient Frontier using Mean Variance Optimization
    plt.plot(Iteration_Matrix['Weight_'+str(Data.columns[1])] ,Iteration_Matrix['Variance'])
    plt.title('Efficient Frontier using Mean-Variance Optimization')
    plt.xlabel('Weight of Asset ' + str(Data.columns[1]))
    plt.ylabel('Variance')
    plt.show()




# Determine Name of the File with the Data (in '.csv' file) 
File = 'Data.csv'

# Determine weight detail required
Weight_Detail = 0.0005

# Determine Cost of Trading Asset 1 and 2 (in basis point)
Cost_A = 60
Cost_B = 40

# Determine Initial Amount Invested
Initial_Investment = 1000000

# Run the Mean Variance Optimisation
Minimisation(File,Weight_Detail,Cost_A,Cost_B,Initial_Investment)