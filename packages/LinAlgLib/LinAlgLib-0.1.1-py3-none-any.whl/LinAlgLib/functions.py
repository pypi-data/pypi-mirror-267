import numpy as np
import sympy as sym  
import inspect

def test ():
    print("Hello World")

def help(quiz_number: int = 0):
    functions = []
    if quiz_number == 0 or quiz_number == 1:
        functions += [
        vector_length,
        dot_product,
        ref,
        rref,
        can_multiply,
        multiply,
        multiply,
        add,]
    if quiz_number == 0 or quiz_number == 2:
        functions += [
        transpose,
        is_invertible,
        inverse,
        determinant,
        elementary_matrices,
        linear_transformation_to,
        linear_transformation_from,
        kernel,
        nullspace]
    if quiz_number == 0 or quiz_number == 3:
        functions += [
        check_transformation,
        range_of_transformation,
        is_euclidean_subspace,
        basis_of_subspace,
        null_space,
        column_space,
        row_space,
        are_orthogonal,
        are_bases_orthogonal,
        orthogonal_complement,
        orthogonal_complement_vector]
    if quiz_number == 0 or quiz_number == 4:
        functions += [
        is_eigenvector,
        is_eigenvalue,
        eigenvectors_for_eigenvalue,
        inner_product,
        norm,
        angle_between_vectors,
        get_matrix_D,
        find_matrix_A,
        find_eigvals_and_eigvecs,
        get_singular_values,
        get_steady_state,
        projection_v_onto_u,
        write_linear_combo_of_orthog_basis,
        make_orthogonal_basis_orthonormal,
        markov_steady_state,
        get_eigenvalues,
        get_eigenvectors,
        gram_schmidt]

    for func in functions:
        signature = inspect.signature(func)
        print(f"Function Name: {func.__name__}")
        print(f"Parameters:")
        for param_name, param_obj in signature.parameters.items():
            if param_name != 'showWork':  # Exclude the 'showWork' parameter
                print(f"- {param_name}: {param_obj.annotation}")
        print(f"Return Type: {signature.return_annotation}\n")
    return

'''
If contributing, please add boolean 'showWork' and show steps to calculate if true
'''

#Add functions below

def vector_length(vector: np.array, showWork: bool = False) -> float:
    if showWork:
        print("Step 1: Square each component of the vector.")
        squares = np.square(vector)
        print("Squared components:", squares)

        print("Step 2: Sum the squares of the components.")
        sum_of_squares = np.sum(squares)
        print("Sum of squares:", sum_of_squares)

        print("Step 3: Take the square root of the sum of squares.")
        length = np.sqrt(sum_of_squares)
        print("Length of the vector:", length)
    else:
        length = np.linalg.norm(vector)

    return length

def dot_product(vector1: np.array, vector2: np.array, showWork: bool = False) -> np.array:
    if len(vector1) != len(vector2):
        raise ValueError("Both vectors must have the same length.")

    if showWork:
        print("Step 1: Multiply corresponding components of the two vectors.")
        products = np.multiply(vector1, vector2)
        print("Products:", products)

        print("Step 2: Sum the products.")
        dot_product_result = np.sum(products)
        print("Dot product:", dot_product_result)
    else:
        dot_product_result = np.dot(vector1, vector2)

    return dot_product_result

def ref(matrix: np.array, showWork: bool = False) -> np.array:
    sympy_matrix = sym.Matrix(matrix)
    ref_matrix, pivots = sympy_matrix.rref(iszerofunc=lambda x: x.is_zero)

    if showWork:
        print("The original matrix is:")
        print(matrix)
        print("\nThe Row Echelon Form (REF) of the matrix is:")
        print(np.array(ref_matrix.tolist()).astype(np.float64))

    return np.array(ref_matrix.tolist()).astype(np.float64)

def rref(matrix: np.array, showWork: bool = False) -> np.array:
    sympy_matrix = sym.Matrix(matrix)
    rref_matrix, pivots = sympy_matrix.rref(iszerofunc=lambda x: x.is_zero)

    if showWork:
        print("The original matrix is:")
        print(matrix)
        print("\nThe Reduced Row Echelon Form (RREF) of the matrix is:")
        print(np.array(rref_matrix.tolist()).astype(np.float64))

    return np.array(rref_matrix.tolist()).astype(np.float64)

def can_multiply(matrix1: np.array, matrix2: np.array, showWork: bool = False) -> bool:
    can_multiply = matrix1.shape[1] == matrix2.shape[0]

    if showWork:
        print("The shape of the first matrix is:", matrix1.shape)
        print("The shape of the second matrix is:", matrix2.shape)

        if can_multiply:
            print("\nThe number of columns in the first matrix is equal to the number of rows in the second matrix.")
            print("So, the matrices can be multiplied.")
            print("The resulting matrix will have a shape of:", (matrix1.shape[0], matrix2.shape[1]))
        else:
            print("\nThe number of columns in the first matrix is not equal to the number of rows in the second matrix.")
            print("So, the matrices cannot be multiplied.")

    return can_multiply

def multiply(scalar: int, vector: np.array, showWork: bool = False) -> np.array:
    if showWork:
        print("The original scalar is:", scalar)
        print("The original vector is:", vector)

        print("\nStep 1: Multiply each component of the vector by the scalar.")
        result_vector = np.multiply(scalar, vector)
        print("Resultant vector:", result_vector)
    else:
        result_vector = np.multiply(scalar, vector)

    return result_vector

def multiply(vector1: np.array, vector2: np.array, showWork: bool = False) -> np.array:
    if len(vector1) != len(vector2):
        raise ValueError("The number of columns in the first matrix is not equal to the number of rows in the second matrix.\nSo, the matrices cannot be multiplied.")

    if showWork:
        print("The first vector is:", vector1)
        print("The second vector is:", vector2)

        print("\nStep 1: Multiply corresponding components of the two vectors.")
        result_vector = np.multiply(vector1, vector2)
        print("Resultant vector:", result_vector)
    else:
        result_vector = np.multiply(vector1, vector2)

    return result_vector

def add(matrix1: np.array, matrix2: np.array, showWork: bool = False) -> np.array:
    if matrix1.shape != matrix2.shape:
        raise ValueError("Both matrices must have the same shape.")

    if showWork:
        print("The first matrix is:\n", matrix1)
        print("The second matrix is:\n", matrix2)

        print("\nStep 1: Add corresponding elements of the two matrices.")
        result_matrix = np.add(matrix1, matrix2)
        print("Resultant matrix:\n", result_matrix)
    else:
        result_matrix = np.add(matrix1, matrix2)

    return result_matrix

def transpose(matrix: np.array, showWork: bool = False) -> np.array:
    if showWork:
        print("The original matrix is:\n", matrix)

        print("\nStep 1: Swap the row and column indices of each element.")
        transposed_matrix = np.transpose(matrix)
        print("Transposed matrix:\n", transposed_matrix)
    else:
        transposed_matrix = np.transpose(matrix)

    return transposed_matrix

def is_invertible(matrix: np.array, showWork: bool = False) -> bool:
    determinant = sym.Matrix(matrix).det()

    if showWork:
        print("The determinant of a matrix is a special number that can be calculated from its elements (i.e., the numbers in the matrix).")
        print("If the determinant of a matrix is not zero, then the matrix is invertible.")
        print("\nCalculating the determinant of the matrix:\n", matrix)
        print("\nThe determinant of the matrix is:", determinant)

    return determinant != 0

def inverse(matrix: np.array, showWork: bool = False) -> np.array:
    if is_invertible(matrix):
        if showWork:
            print("The inverse of a matrix is a special matrix that, when multiplied with the original matrix, gives the identity matrix.")
            print("The identity matrix is a special matrix with ones on the diagonal and zeros elsewhere.")
            print("\nCalculating the inverse of the matrix:\n", matrix)
        inverse = np.linalg.inv(matrix)

        if showWork:
            print("\nThe inverse of the matrix is:\n", inverse)

        return inverse
    else:
        raise ValueError("The matrix is not invertible.")

def determinant(matrix: np.array, showWork: bool = False) -> float:
    if showWork:
        print("The determinant of a matrix is a special number that can be calculated from its elements (i.e., the numbers in the matrix).")
        print("The determinant can be used to solve systems of linear equations (Cramer's rule), to find the inverse of a matrix, to calculate the volume of a parallelepiped, and many other things.")
        print("\nCalculating the determinant of the matrix:\n", matrix)
    determinant = sym.Matrix(matrix).det()

    if showWork:
        print("\nThe determinant of the matrix is:", determinant)

    return determinant

def elementary_matrices(matrix: np.array, showWork: bool = False) -> list:
    sympy_matrix = sym.Matrix(matrix)
    nrows, ncols = sympy_matrix.shape

    elementary_matrices = []
    for i in range(nrows):
        for j in range(ncols):
            if i != j:
                # Create an identity matrix of the same size as the input matrix
                elementary_matrix = sym.eye(nrows)

                # Replace one element to create an elementary matrix
                elementary_matrix[i, j] = sympy_matrix[i, j]

                elementary_matrices.append(elementary_matrix)

                if showWork:
                    print(f"\nElementary matrix E{i+1}{j+1} is obtained by replacing element at position ({i+1}, {j+1}) of the identity matrix with the corresponding element of the original matrix:")
                    print(np.array(elementary_matrix.tolist()).astype(np.float64))

    if not showWork:
        for i, elementary_matrix in enumerate(elementary_matrices, start=1):
            print(f"\nElementary matrix E{i} is:")
            print(np.array(elementary_matrix.tolist()).astype(np.float64))

    return elementary_matrices

def linear_transformation_to(matrix: np.array, transformation_matrix: np.array, showWork: bool = False) -> np.array:
    if showWork:
        print("The original matrix is:\n", matrix)
        print("The transformation matrix is:\n", transformation_matrix)

        print("\nStep 1: Multiply the transformation matrix with the original matrix.")
    transformed_matrix = np.dot(transformation_matrix, matrix)

    if showWork:
        print("Transformed matrix:\n", transformed_matrix)

    return transformed_matrix

def linear_transformation_from(matrix: np.array, transformation_matrix: np.array, showWork: bool = False) -> np.array:
    if showWork:
        print("The original matrix is:\n", matrix)
        print("The transformation matrix is:\n", transformation_matrix)

        print("\nStep 1: Multiply the original matrix with the transformation matrix.")
    transformed_matrix = np.dot(matrix, transformation_matrix)

    if showWork:
        print("Transformed matrix:\n", transformed_matrix)

    return transformed_matrix

def kernel(matrix: np.array, showWork: bool = False) -> list:
    sympy_matrix = sym.Matrix(matrix)
    kernel = sympy_matrix.nullspace()

    if showWork:
        print("The kernel of a transformation is the set of all vectors that are mapped to the zero vector.")
        print("\nCalculating the kernel of the matrix:\n", matrix)

    if showWork or not showWork:
        print("\nThe kernel of the matrix is:")
        for vector in kernel:
            print(np.array(vector.tolist()).astype(np.float64))

    return kernel

def nullspace(matrix: np.array, showWork: bool = False) -> list:
    return kernel(matrix, showWork)

def check_transformation(matrix: np.array, showWork: bool = False) -> str:
    sympy_matrix = sym.Matrix(matrix)
    nrows, ncols = sympy_matrix.shape

    is_one_to_one = sympy_matrix.rank() == ncols
    is_onto = sympy_matrix.rank() == nrows

    if showWork:
        print("A transformation is one-to-one if each element of the domain is mapped to a unique element of the codomain.")
        print("A transformation is onto if each element of the codomain has a corresponding element in the domain.")
        print("\nChecking the transformation of the matrix:\n", matrix)

    if is_one_to_one and is_onto:
        result = "The transformation is both one-to-one and onto."
    elif is_one_to_one:
        result = "The transformation is one-to-one but not onto."
    elif is_onto:
        result = "The transformation is onto but not one-to-one."
    else:
        result = "The transformation is neither one-to-one nor onto."

    if showWork or not showWork:
        print("\n" + result)

    return result

def range_of_transformation(matrix: np.array, showWork: bool = False) -> list:
    sympy_matrix = sym.Matrix(matrix)
    _, pivots = sympy_matrix.rref()

    if showWork:
        print("The range (or image) of a transformation is the set of all possible outputs of the transformation.")
        print("\nCalculating the range of the transformation of the matrix:\n", matrix)

    range_matrix = sympy_matrix[:, pivots]

    if showWork or not showWork:
        print("\nThe range of the transformation is:")
        print(np.array(range_matrix.tolist()).astype(np.float64))

    return range_matrix

def is_euclidean_subspace(set_of_vectors: list, showWork: bool = False) -> bool:
    zero_vector = np.zeros_like(set_of_vectors[0])
    is_closed_under_vector_addition = all(np.add(v1, v2) in set_of_vectors for v1 in set_of_vectors for v2 in set_of_vectors)
    is_closed_under_scalar_multiplication = all(np.multiply(scalar, v) in set_of_vectors for v in set_of_vectors for scalar in range(-10, 11))
    contains_zero_vector = zero_vector in set_of_vectors

    is_subspace = is_closed_under_vector_addition and is_closed_under_scalar_multiplication and contains_zero_vector

    if showWork:
        print("A set is a Euclidean subspace if it is closed under vector addition and scalar multiplication, and contains the zero vector.")
        print("\nChecking if the set of vectors is a Euclidean subspace:\n", set_of_vectors)

    if showWork or not showWork:
        print("\nThe set is a Euclidean subspace:" if is_subspace else "\nThe set is not a Euclidean subspace.")

    return is_subspace

def basis_of_subspace(matrix: np.array, showWork: bool = False) -> list:
    sympy_matrix = sym.Matrix(matrix)
    _, pivots = sympy_matrix.rref()

    if showWork:
        print("The basis of a subspace is a set of vectors in the subspace that are linearly independent and span the subspace.")
        print("\nCalculating the basis of the subspace of the matrix:\n", matrix)

    basis_matrix = sympy_matrix[:, pivots]

    if showWork or not showWork:
        print("\nThe basis of the subspace is:")
        print(np.array(basis_matrix.tolist()).astype(np.float64))

    return basis_matrix

def null_space(matrix: np.array, showWork: bool = False) -> list:
    sympy_matrix = sym.Matrix(matrix)
    null_space = sympy_matrix.nullspace()

    if showWork:
        print("The null space of a matrix is the set of all vectors that when multiplied by the matrix result in the zero vector.")
        print("\nCalculating the null space of the matrix:\n", matrix)

    if showWork or not showWork:
        print("\nThe null space of the matrix is:")
        for vector in null_space:
            print(np.array(vector.tolist()).astype(np.float64))

    return null_space

def column_space(matrix: np.array, showWork: bool = False) -> list:
    sympy_matrix = sym.Matrix(matrix)
    column_space = [sympy_matrix[:, i] for i in range(sympy_matrix.shape[1])]

    if showWork:
        print("The column space of a matrix is the set of all possible linear combinations of its column vectors.")
        print("\nCalculating the column space of the matrix:\n", matrix)

    if showWork or not showWork:
        print("\nThe column space of the matrix is:")
        for vector in column_space:
            print(np.array(vector.tolist()).astype(np.float64))

    return column_space

def row_space(matrix: np.array, showWork: bool = False) -> list:
    sympy_matrix = sym.Matrix(matrix)
    row_space = [sympy_matrix[i, :] for i in range(sympy_matrix.shape[0])]

    if showWork:
        print("The row space of a matrix is the set of all possible linear combinations of its row vectors.")
        print("\nCalculating the row space of the matrix:\n", matrix)

    if showWork or not showWork:
        print("\nThe row space of the matrix is:")
        for vector in row_space:
            print(np.array(vector.tolist()).astype(np.float64))

    return row_space

def are_orthogonal(vector1: np.array, vector2: np.array, showWork: bool = False) -> bool:
    dot_product = np.dot(vector1, vector2)
    are_orthogonal = dot_product == 0

    if showWork:
        print("Two vectors are orthogonal if their dot product is zero.")
        print("\nCalculating the dot product of the vectors:", vector1, "and", vector2)

    if showWork or not showWork:
        print("\nThe vectors are orthogonal:" if are_orthogonal else "\nThe vectors are not orthogonal.")

    return are_orthogonal

def are_bases_orthogonal(basis1: list, basis2: list, showWork: bool = False) -> bool:
    are_orthogonal = all(are_orthogonal(v1, v2) for v1 in basis1 for v2 in basis2)

    if showWork:
        print("Two bases are orthogonal if each pair of vectors from the two bases are orthogonal.")
        print("\nChecking if the bases are orthogonal:\n", basis1, "\nand\n", basis2)

    if showWork or not showWork:
        print("\nThe bases are orthogonal:" if are_orthogonal else "\nThe bases are not orthogonal.")

    return are_orthogonal

def orthogonal_complement(subspace: list, showWork: bool = False) -> list:
    matrix = np.array(subspace).T
    sympy_matrix = sym.Matrix(matrix)
    orthogonal_complement = sympy_matrix.nullspace()

    if showWork:
        print("The orthogonal complement to a subspace is the set of all vectors that are orthogonal to every vector in the subspace.")
        print("\nCalculating the orthogonal complement to the subspace:\n", subspace)

    if showWork or not showWork:
        print("\nThe orthogonal complement to the subspace is:")
        for vector in orthogonal_complement:
            print(np.array(vector.tolist()).astype(np.float64))

    return orthogonal_complement

def orthogonal_complement_vector(vector: np.array, showWork: bool = False) -> list:
    return orthogonal_complement([vector], showWork)

def is_eigenvector(matrix: np.array, vector: np.array, showWork: bool = False) -> bool:
    # Calculate the matrix-vector product
    matrix_vector_product = np.dot(matrix, vector)

    # Check if the matrix-vector product is a scalar multiple of the vector
    is_eigenvector = np.allclose(matrix_vector_product, np.dot(matrix_vector_product[0] / vector[0], vector))

    if showWork:
        print("A vector is an eigenvector of a matrix if it satisfies the equation Av = λv, where A is the matrix, v is the vector, and λ is a scalar known as the eigenvalue.")
        print("\nChecking if the vector is an eigenvector of the matrix:\n", matrix)

    if showWork or not showWork:
        print("\nThe vector is an eigenvector of the matrix:" if is_eigenvector else "\nThe vector is not an eigenvector of the matrix.")

    return is_eigenvector

def is_eigenvalue(matrix: np.array, value: float, showWork: bool = False) -> bool:
    sympy_matrix = sym.Matrix(matrix)
    eigenvalues = sympy_matrix.eigenvals()

    is_eigenvalue = value in eigenvalues

    if showWork:
        print("A number is an eigenvalue of a matrix if there exists a non-zero vector v such that Av = λv, where A is the matrix, v is the vector, and λ is the eigenvalue.")
        print("\nChecking if the number is an eigenvalue of the matrix:\n", matrix)

    if showWork or not showWork:
        print("\nThe number is an eigenvalue of the matrix:" if is_eigenvalue else "\nThe number is not an eigenvalue of the matrix.")

    return is_eigenvalue

def eigenvectors_for_eigenvalue(matrix: np.array, value: float, showWork: bool = False) -> list:
    sympy_matrix = sym.Matrix(matrix)
    eigenvectors = [v for v in sympy_matrix.eigenvects() if v[0] == value]

    if showWork:
        print("The eigenvectors corresponding to a given eigenvalue are the non-zero solutions to the equation (A - λI)v = 0, where A is the matrix, λ is the eigenvalue, I is the identity matrix, and v is the vector.")
        print("\nFinding all eigenvectors for the eigenvalue of the matrix:\n", matrix)

    if showWork or not showWork:
        print("\nThe eigenvectors for the eigenvalue are:")
        for vector in eigenvectors:
            print(np.array(vector[2][0].tolist()).astype(np.float64))

    return eigenvectors
  
def inner_product(v1: np.array, v2: np.array = None, coeffs: list = None, showWork: bool = False):
    result = 0
    if showWork:
        print("To find the inner product: Plug in each vector component to the cooresponding variable in the inner product equation")
    
    size = len(v1)
    if not coeffs:
            coeffs = [1] * size

    if size != len(coeffs):
         return print("Please make sure the coefficent list is the same size as np.array (put 1 as a coeff if need to fill the space)")
        
    if v2: 
        for i in range(size):
            result += v1[i] * v2[i] * coeffs[i]

    else:
        for i in range(size):
            result += v1[i] * v1[i] * coeffs[i]
    return result

        
    

def norm (v1: np.array, inner_product_coeff: list = None, showWork: bool=False) -> int:

    if showWork:
        print("The norm is found by taking the inner product of the vector(s) and taking the square root of the result")
        print("\nTo find the inner product: Plug in each vector component to the cooresponding variable in the inner product equation")
        return inner_product(v1, coeffs=inner_product_coeff, showWork=True)**(1/2)
    
    return inner_product(v1, coeffs=inner_product_coeff, showWork=False)**(1/2)
    


def angle_between_vectors(v1: np.array, v2: np.array, inner_product_coeff: list = None, showWork: bool=False ):
    if showWork:
        print("Take inner product and divide it by ||v1|| * ||v2||, then take inverse cos")
        return np.degrees(np.arccos(inner_product(v1,v2,inner_product_coeff,showWork=True) / (norm(v1,showWork=True) * norm(v2,showWork=True))))
    print("This answer is in degrees to change to radians do np.radians() or multiply answer by np.pi/180")
    return np.degrees(np.arccos(inner_product(v1,v2,inner_product_coeff,showWork=False) / (norm(v1,showWork=False) * norm(v2,showWork=False))))


def diagonalize(matrix: np.array, showWork=False):
    if showWork:
        print("Get eigvals and eigvecs and then multiply eigvecs@np.diag(eigvals)@np.linalg.inv(eigvecs)")
    
    eigvals,eigvecs = np.linalg.eig(matrix)
    return eigvecs@get_matrix_D(matrix)@np.linalg.inv(eigvecs)

def get_matrix_D(matrix: np.array, showWork=False):
    if showWork:
        print("Find eigvals and then call np.diag")
    eigvals,eigvecs = np.linalg.eig(matrix)
    return np.diag(eigvals)


def find_matrix_A(P: np.array, D: np.array, exponent: float=1, showWork=False):
    if showWork:
        print("Follow formula P@D^exponent_of_A@inv(P)")
    return P@D**exponent@np.linalg.inv(P)

def find_eigvals_and_eigvecs(matrix: np.array, showWork=False):
    return sym.Matrix(matrix).eigenvects()

def get_singular_values(matrix: np.array, showWork=False):
    if showWork:
        print("Find transpose of array then multiply it with A and find the square root of the eigvals")
    A = matrix.T@matrix
    return np.linalg.eig(A)[0]**(1/2)
    
def get_steady_state(matrix: np.array, showWork=False):
    if showWork:
        print("Find eigvals and eigvec of the matrix, then eigvecs[:,0]/ sum(eigvecs[:,0])")
        print("\nIf you need to find how many of something is in a room in the long run do the total number of things * the steadystate[room#-1]")
        print("\nEX: Assume that there are total 12 cats, so in the long-term, how many cats will be in room 3 (12*steadystate[2])")

    eigvals, eigvecs = np.linalg.eig(matrix)
    return eigvecs[:,0] / sum(eigvecs[:,0])

def Gram_Schmidt_2():
    print("Inner Product Function: ")
    print("\ndef inner_product(v1, v2):return 4 * v1[0] * v2[0] + 3 * v1[1] * v2[1]")
    print("\ngs_algo:")
    print("\ndef gs(v1, v2, v3):    b = [[v1]]    u2 = v2 - (inner_product(v1,v2)/inner_product(v1,v1) * v1)    b.append(u2)    return b")
    return

def Gram_Schmidt_3():
    print("Inner Product Function: ")
    print("\ndef inner_product(v1, v2):return 4 * v1[0] * v2[0] + 3 * v1[1] * v2[1] + 5 * v1[2] * v2[2]")
    print("\ngs_algo:")
    print("\ndef gs(v1, v2, v3):    b = [[v1]]    u2 = v2 - (inner_product(v1,v2)/inner_product(v1,v1) * v1)    b.append(u2)    u3 = v3 - (inner_product(v1,v3)/inner_product(v1,v1) * v1) - (inner_product(u2,v3)/inner_product(u2,u2) * u2)  b.append(u3) return b")
    return

def Gram_Schmidt_4():
    print("Inner Product Function: ")
    print("\ndef inner_product(v1, v2):return 4 * v1[0] * v2[0] + 3 * v1[1] * v2[1] + 5 * v1[2] * v2[2] + 5 * v1[3] * v2[3]")
    print("\ngs_algo:")
    print("\ndef gs(v1, v2, v3):    b = [[v1]]    u2 = v2 - (inner_product(v1,v2)/inner_product(v1,v1) * v1)    b.append(u2)    u3 = v3 - (inner_product(v1,v3)/inner_product(v1,v1) * v1) - (inner_product(u2,v3)/inner_product(u2,u2) * u2)  b.append(u3)    u4 = v4 - (inner_product(v1,v4)/inner_product(v1,v1) * v1) - (inner_product(u2,v4)/inner_product(u2,u2) * u2) - (inner_product(u3,v4)/inner_product(u3,u3) * u3)    b.append(u4)  return b")
    return

def projection_v_onto_u(v: np.array, u: np.array, inner_prod_coeffs: list=None,showWork: bool=False):
    if not inner_prod_coeffs:
        inner_prod_coeffs = [1] * len(v)

    if len(inner_prod_coeffs) != len(v):
        print("Either not enough inner product coefficents were given or there is an error in the vectors given")

    numerator = inner_product(v, u, coeffs=inner_prod_coeffs, showWork=False)
    denomonator = inner_product(u,u,coeffs=inner_prod_coeffs, showWork=False)
    return (numerator / denomonator) * np.array(u)



def write_linear_combo_of_orthog_basis(v1: np.array, basis: np.array, inner_coeffs: list=None, showWork: bool=False):
    if showWork:
        print("Find projection of given vector onto the basis vector and the result is the coefficent for the basis vector in the linear combination")

    coefficients = []
    for v in basis:
        coefficient = inner_product(v1, v,coeffs=inner_coeffs) / inner_product(v, v, coeffs=inner_coeffs)
        coefficients.append(coefficient)
    print("These are the coefficents for the linear combination. The first value given cooresponds with the first vector in the basis")
    return coefficients

def make_orthogonal_basis_orthonormal(num_vectors_in_basis: int=2):
    print("Perform Gram_Schmidt then once you get the vectors normalize then divde by the norm of the vector")
    if num_vectors_in_basis == 2:
        return Gram_Schmidt_2()
    elif num_vectors_in_basis == 3:
        return Gram_Schmidt_3()
    else:
        return Gram_Schmidt_4()

def markov_steady_state(matrix: np.array, showWork: bool = False) -> list:
    eigval, eigvect = np.linalg.eig(matrix)
    index = 0
    for i in range(len(eigval)):
        if eigval[i] == 1:
            index = i
    steady_state = eigvect[:,index]
    steady_state = steady_state * -1
    constant = 1/(sum(steady_state))
    steady_state = steady_state * constant
    if showWork:
        print("To calculate the steady state matrix, you must obtain the eigenvector corresponding to the eigenvalue λ = 1. Then you must calculate a constant such that the sum of all values in the eigenvector equals to 1.")
        print("The eigenvector corresponding to λ = 1, is:\n", eigvect[:,index] * -1)
        print("Dividing 1 by the sum of all values gives us the constant: ", constant)
    if showWork or not showWork:
        print("The normalized steady state vector is:\n", steady_state)
        
    return steady_state

def similar_matrix_check(matrix1: np.array, matrix2: np.array, showWork: bool=False):
    eigvals1, eigvecs1 = np.linalg.eig(matrix1)
    eigvals2, eigvecs1 = np.linalg.eig(matrix2)
    print(eigvals1, eigvals2)
    print("If both have the same values then they are similar if the are not the same then they are not similar") 


def is_diaonalizable(matrix: np.array, showWork: bool = False):
    eigvals1, eigvecs1 = np.linalg.eig(matrix)
    if (len(eigvals1) != len(eigvecs1)):
        print("This matrix is not diagoniable becuase the number of eigen values does not equal the number of eigen vects", eigvals1, eigvecs1)
    else:
         print("This matrix is not diagoniable becuase the number of eigen values equals the number of eigen vects", eigvals1, eigvecs1)

def get_eigenvalues(matrix: np.array, showWork: bool = False) -> list:
    eigval = np.linalg.eig(matrix)[0]
    I = np.identity(len(matrix))
    λ = sym.symbols('λ')
    Iλ = I * λ 
    A = matrix - Iλ
    
    if showWork:
        print("The eigenvalues (λ) can be calculates using the equation (A - λI) = 0, and then solving for λ")
        print("First simplifying A - λI gives the matrix:\n", sym.Matrix(A))
        print("Then you must solve for its determinant, which simplifies to this equation:\n", sym.Matrix(A).det(), "= 0")
    if showWork or not showWork:
        print("Solving for λ gives:")
        for i in range(len(eigval)):
            print("λ" + str(i+1) + " = " + str(eigval[i]))
    return eigval

def get_eigenvectors(matrix: np.array, showWork: bool = False) -> list:
    eigvects = np.linalg.eig(matrix)[1]
    eigvals = np.linalg.eig(matrix)[0]
    λ = sym.symbols('λ')
    n = matrix.shape[0]
    I = np.identity(n)
    Iλ = I * λ
    v = sym.Matrix(n, 1, lambda i, j: sym.symbols(f'x{i+1}'))
    system = (matrix - Iλ)@v
    if showWork:
        print("The eigenvectors can be calculated by first finding a matrix's eigenvalues (λ), then using the equation (A-λI)v = 0, where v is an eigenvector corresponding to an eigenvalue.")
        print("\nSubstituting A, and any eigenvalue into the equation gives the matrix system:")
        for i in range(len(system)):
            print("["+str(system[i])+"]")
        print("\nSubstituting λ into the matrix system of equation allows us to solve for all variables.")
    if showWork or not showWork:
        print("\nSubstituting all values of λ, and solving for unknowns gives these eigenvectors:")
        for i in range(len(eigvects)):
            print("Eigenvector λ =", str(eigvals[i]), "=", eigvects[:,i])
    
    return eigvects

def gram_helper_dont_use(*vectors):
    basis = []
    
    for v in vectors:
        # Remove the projection from all previous basis vectors
        for b in basis:
            proj = (v.dot(b) / b.dot(b)) * b
            v = v - proj
        
        # Normalize the vector
        v = v / v.norm()
        
        # Add the normalized vector to the basis
        basis.append(v)
    
    return basis

def gram_schmidt(vector_list):

    # Convert the list of lists to sympy Matrix objects
    vectors = [sym.Matrix(v) for v in vector_list]
    
    # Perform the Gram-Schmidt process
    basis = gram_helper_dont_use(*vectors)
    
    # Convert the symbolic expressions to numerical approximations (floating-point numbers)
    basis_approx = [b.evalf() for b in basis]
    
    return basis_approx
