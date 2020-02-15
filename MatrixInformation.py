"""Goal: Return various information about a matrix and learn about classes
   Start Date: 31st December, 2019
   End Date: 1st January, 2020
   Notes:
       According to PEP8, module imports should be at the very top
       Need to import numpy outside of the class thing
       Why do I have to call the class itself anytime I want to do something?
       When naming classes, always do uppercase: UpperCase
       You define all of the functions available for the class
       Each definition should have 1 line space between the others
       Constructor (__init__):
            A function that gets called at the time of creating an object"""

import numpy as np
from scipy.linalg import null_space
from scipy.linalg import norm
# Create a list of lists
A = [[1, 0],
     [0, 2]]

 class MatrixInfo:
    """
    Get various information about a matrix
    An MxN matrix and a conditional norm are the only input needed
    I feel like the items themselves are self-explanatory"""

    # Initialization:
    def __init__(self, Matrix, ConditionNorm): # Write all inputs to function here
        self.Matrix = Matrix
        self.ConditionNorm = ConditionNorm
        # Self is the MatrixInfo function itself

    # Return the original matrix
    def Get_Matrix(self):
        return self.Matrix
    # Rank:

    def Rank(self):
        import numpy as np
        print(np.linalg.matrix_rank(self.Matrix))
    # Kernel / Null Space:

    def NullSpace(self):
        return null_space(self.Matrix)
    # Determinant:

    def Determinant(self):
        return np.linalg.det(self.Matrix)
    # Eigenvalues:

    def Eigenvalues(self):
        return np.linalg.eigvals(self.Matrix)
    # Eigenvectors:

    def Eigenvectors(self):
        return np.linalg.eig(self.Matrix)
    # Multiplicative Inverse:

    def Inverse(self):
        return np.linalg.inv(self.Matrix)
    # Transpose:

    def Transpose(self):
        return np.transpose(self.Matrix)
    # Trace:

    def Trace(self):
        """Sum of diagonals"""
        return np.trace(self.Matrix)
    # Identity Matrix:

    def Identity(self):
        length = len(self.Matrix)
        return np.identity(length)
    # Conjugate:

    def Conjugate(self):
        return np.conjugate(self.Matrix)
    # Diagonal:

    def Diagonal(self):
        return np.diagonal(self.Matrix)
    # L1 Norm:

    def L1Norm(self):
        return norm(self.Matrix)

    # Condition Number
    def Condition(self):
        return np.linalg.cond(self.Matrix, p = self.ConditionNorm)

# Testing:
# Convert to a matrix
A = np.matrix(A)

# Initialize the class object:
Matrix = MatrixInfo(Matrix = A, ConditionNorm = 1)

# Retrieve information about the matrix
Matrix.get_matrix() #I
Matrix.Identity() #I
Matrix.Conjugate() #I
Matrix.Trace() #2
Matrix.Transpose() #I
Matrix.Inverse() #I
Matrix.Eigenvalues() #1
Matrix.Eigenvectors() #(1,0), (0,1)
Matrix.Determinant() #1
Matrix.NullSpace() #Empty
Matrix.Rank() #2
Matrix.Diagonal() #just the diagonal entries
Matrix.L1Norm() #np.sqrt(2)
Matrix.Condition() #1
