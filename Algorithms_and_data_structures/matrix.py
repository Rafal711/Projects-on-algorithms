from copy import copy, deepcopy

class Matrix:
    def __init__(self, param, init_val=0):
        if isinstance(param, tuple):
            if len(param) == 2:
                self.matrix = [[init_val] * param[1] for _ in range(param[0])]
            else:
                raise ValueError
        else:
            self.matrix = param

    def __getitem__(self, index):
        return self.matrix[index]

    def __len__(self):
        return len(self.matrix)

    def __str__(self):
        str_matrix = "[" + str(self.matrix[0])
        for i in range(len(self.matrix) - 1):
            str_matrix += "\n" + " " + str(self.matrix[i + 1])
        return str_matrix + "]"

    def __add__(self, other):
        nr_of_rows = len(self.matrix)
        nr_of_cols = len(self.matrix[0])

        if nr_of_rows != len(other) or nr_of_cols != len(other[0]):
            raise ValueError
        sum_of_matrices = Matrix((nr_of_rows, nr_of_cols))
        for i in range(nr_of_rows):
            for j in range(nr_of_cols):
                sum_of_matrices[i][j] = self.matrix[i][j] + other[i][j]
        return sum_of_matrices

    def __mul__(self, other):
        num_of_rows_1 = len(self.matrix)
        num_of_cols_1 = len(self.matrix[0])
        num_of_cols_2 = len(other[0])

        if num_of_cols_1 != len(other):
            raise ValueError
        mul_of_matrices = Matrix((num_of_rows_1, num_of_cols_2))
        for i in range(num_of_rows_1):
            for j in range(num_of_cols_2):
                sum_of_elem = 0
                for k in range(num_of_cols_1):
                    sum_of_elem += self.matrix[i][k] * other[k][j]
                mul_of_matrices[i][j] = sum_of_elem
        return mul_of_matrices

    def chio_det(self, matrix=None, factor=1):
        if matrix is None:
            matrix = deepcopy(self.matrix)
        length = len(matrix)
        if length == 2:
            return ((matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0]))/factor
        if matrix[0][0] == 0:
            for i in range(1, length):
                if matrix[i][0] != 0:
                    matrix[0], matrix[i] = matrix[i], matrix[0]
                    factor *= (-1)
                    break
        if matrix[0][0] == 0:
            return 0
        matrix_s = []
        for i in range(length - 1):
            dets = []
            for j in range(1, length):
                dets.append(((matrix[0][0] * matrix[i + 1][j]) - (matrix[0][j] * matrix[i + 1][0])))
            matrix_s.append(dets)
        factor *= (matrix[0][0] ** (length - 2))
        return self.chio_det(matrix_s, factor)


def transpose(matrix):
    matrix_t = []
    for elem in zip(*matrix):
        matrix_t.append(list(elem))
    return Matrix(matrix_t)


# A = Matrix([[1, 0, 2], [-1, 3, 1]])
# B = Matrix([[-1, 3, 1], [1, 0, 2]])
# C = Matrix([[3, 1], [2, 1], [1, 0]])
#
# print("Transponowana macierz A:")
# print(transpose(A))
# print("\nA + B =")
# print(A + B)
# print("\nA * C =")
# print(A * C)

A2 = Matrix([[5, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9 , 1, 0, 7, 0],[1, 4, 7, 2, 2]])
B2 = Matrix([[0, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])

print("\nWyznaczniki:")
print("det(A2)=")
print(A2.chio_det())
print("det(B2)=")
print(B2.chio_det())





