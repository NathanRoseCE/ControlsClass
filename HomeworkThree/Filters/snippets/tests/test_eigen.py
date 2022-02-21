import sympy
from ..eigen import *

def test_eigvals_2_by_2_in_jordan():
    A = sympy.Matrix([[1, 0],
                      [0,-1]])
    work, calc_eigs = eigenvalues(A, show_work=False)
    assert -1 in calc_eigs
    assert 1 in calc_eigs

def test_eigvals_2_by_2_in_jordan_repeated_eigs():
    A = sympy.Matrix([[1, 0],
                      [0, 1]])
    work, calc_eigs = eigenvalues(A, show_work=False)
    assert [1,1] == calc_eigs
    
def test_eigvals_2_by_2():
    A = sympy.Matrix([[1, 4],
                      [1, 1]])
    work, calc_eigs = eigenvalues(A, show_work=False)
    assert 3 in calc_eigs
    assert -1 in calc_eigs
    
def test_eigvals_3_by_3():
    A = sympy.Matrix([[2, -3, 0],
                      [2, -5, 0],
                      [0,  0, 3]])
    work, calc_eigs = eigenvalues(A, show_work=False)
    assert 1 in calc_eigs
    assert 3 in calc_eigs
    assert -4 in calc_eigs

def test_eigenvector_2_by_2():
    A = sympy.Matrix([[1, 4],
                      [1, 1]])
    work, modal = modal_matrix(A, show_eigen_work=False)
    P, J = A.jordan_form()
    eig_vectors = [P.col(i) for i in range(A.shape[0])]
    P, J = A.jordan_form()
    print(P)
    V = np.array(modal).astype(np.float64)
    A = np.array(A).astype(np.float64)
    print(V)
    print(np.linalg.inv(V) @ A @ V)
    assert (np.allclose(np.linalg.inv(V) @ A @ V, np.array([[-1, 0],[0,3]])) or
            np.allclose(np.linalg.inv(V) @ A @ V, np.array([[3, 0],[0,-1]])))
    

def test_eigenvector_3_by_3_repeated():
    A = sympy.Matrix([[2,-1,  1],
                      [1, 5, -2],
                      [0, 1, 2]])
    work, modal = modal_matrix(A, show_eigen_work=False)
    P, J = A.jordan_form()
    eig_vectors = [P.col(i) for i in range(A.shape[0])]
    P, J = A.jordan_form()
    print(P)
    V = np.array(modal).astype(np.float64)
    A = np.array(A).astype(np.float64)
    
    print(f"V_cal = {V}")
    print(f"V_cor = {np.array(P).astype(np.float64)}")
    print(np.linalg.inv(V) @ A @ V)
    assert (np.allclose(np.linalg.inv(V) @ A @ V, np.array([[3,1,0], [0,3,1], [0,0,3]])))
    
