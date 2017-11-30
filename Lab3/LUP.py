class Matrix:
    limit = 1e-6

    def __init__(self, rows, columns):
        self.rows, self.columns = rows, columns
        self.data = []
        for i in range(self.rows):
            self.data.append([None] * self.columns)

    def forward_substitution(self, b):
        if (self.columns != self.rows): return 0
        n = self.rows
        y = b.copy()

        for i in range(n - 1):
            for j in range(i + 1, n):
                y.data[j][0] -= (self.data[j][i] * y.data[i][0])

        return y

    def back_substitution(self, y):
        if (self.columns != self.rows): return 0
        n = self.rows
        x = y.copy()

        for i in range(n - 1, -1, -1):
            if (abs(self.data[i][i]) < self.limit):
                print("Postupak zaustavljen u supstituciji unatrag jer je pivot manji od zadane granice!")
                return
            x.data[i][0] /= self.data[i][i]
            for j in range(i):
                x.data[j][0] -= (self.data[j][i] * x.data[i][0])

        return x

    def tolist(self):
        res = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(self.get_element((i,j)))
            res.append(row)
        return res

    def read_from_file(filename):
        data = []
        columns, rows = 0, 0
        with open(filename) as f:
            lines = list(f)
            rows = len(lines)
            for l in lines:
                row = l.split()
                columns = len(row)
                data.append(row)

        matrix = Matrix(rows, columns)
        matrix.set_data(data)
        return matrix

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))
        return

    def LU_decomposition(self):
        if (self.rows != self.columns):
            raise Exception("LU dekompozicija izvediva je samo na kvadratnoj matrici!");
        work_matrix = self.copy()
        for i in range(self.rows - 1):
            for j in range(i + 1, self.columns):
                if (abs(work_matrix.data[i][i]) < self.limit):
                    print(
                        "LU dekompozicija je zaustavljena jer je detektiran stozerni element manji od zadane granice!");
                    print("Pokrećem LUP dekompoziciju..")
                    return self.LUP_decomposition()
                work_matrix.data[j][i] /= work_matrix.data[i][i]
                for k in range(i + 1, self.rows):
                    work_matrix.data[j][k] -= work_matrix.data[j][i] * work_matrix.data[i][k]
        return work_matrix

    def LUP_decomposition(self):
        P = Matrix.eye(self.rows)
        work_matrix = self.copy()

        for i in range(self.rows - 1):
            pivot = i
            for j in range(i + 1, self.rows):
                if (abs(work_matrix.get_element((j, i))) > abs(work_matrix.get_element((pivot, i)))):
                    pivot = j
            if (abs(work_matrix.data[pivot][i]) < self.limit):
                print("LUP dekompozicija je zaustavljena jer je detektiran stozerni element manji od zadane granice!");
                return

            work_matrix = work_matrix.switch_rows(i, pivot)
            P = P.switch_rows(i, pivot)

            for j in range(i + 1, self.rows):
                work_matrix.data[j][i] /= work_matrix.data[i][i]
                for k in range(i + 1, self.rows):
                    work_matrix.data[j][k] -= work_matrix.data[j][i] * work_matrix.data[i][k]

        return work_matrix, P

    def switch_rows(self, i, j):
        m = self.copy()
        for k in range(self.columns):
            m.set_element((i, k), self.get_element((j, k)))
            m.set_element((j, k), self.get_element((i, k)))
        return m

    def get_L(self):
        L = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                if (i == j):
                    L.set_element((i, j), 1)
                elif (i > j):
                    L.set_element((i, j), self.data[i][j])
                else:
                    L.set_element((i, j), 0)
        return L

    def get_U(self):
        U = Matrix(self.rows, self.columns)
        for i in range(self.rows):
            for j in range(self.columns):
                if (i <= j):
                    U.set_element((i, j), self.get_element((i, j)))
                else:
                    U.set_element((i, j), 0)
        return U

    def copy(self):
        new_matrix = Matrix(self.rows, self.columns)
        new_matrix.set_data(self.data)
        return new_matrix

    def eye(size):
        matrix = Matrix(size, size)
        for i in range(size):
            for j in range(size):
                if (i == j):
                    matrix.set_element((i, j), 1)
                else:
                    matrix.set_element((i, j), 0)
        return matrix

    def set_data(self, data):
        for i in range(self.rows):
            for j in range(self.columns):
                self.set_element((i, j), float(data[i][j]))

    def set_element(self, index, value):
        self.data[index[0]][index[1]] = float(value)

    def get_element(self, index):
        return self.data[index[0]][index[1]]

    def scalar(self, other):
        matrix = [[] for y in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                matrix[i].append(self.data[i][j] * other)
        self.set_data(matrix)
        return self

    def __str__(self):
        result = ""
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                result += str(self.data[i][j]) + " "
            result += "\n"
        return result

    def __add__(self, other):
        if (self.rows != other.rows or self.columns != other.columns): return 0
        matrix = [[] for y in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                matrix[i].append(self.data[i][j] + other.data[i][j])
        self.set_data(matrix)
        return self

    def __sub__(self, other):
        if (self.rows != other.rows or self.columns != other.columns): return 0
        matrix = [[] for y in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                matrix[i].append(self.data[i][j] - other.data[i][j])
        self.set_data(matrix)
        return self

    def __rmul__(self, other):
        if (not hasattr(other, "__len__")):
            return self.scalar(other)
        else:
            return self.__mul__(self, other)

    def __mul__(self, other):
        if (not isinstance(other, Matrix) or self.columns != other.rows): return
        m = self.columns
        matrix = [[] for y in range(self.rows)]

        for i in range(self.rows):
            for j in range(other.columns):
                result = 0
                for k in range(m):
                    result += self.data[i][k] * other.data[k][j]
                matrix[i].append(result)
        new_matrix = Matrix(self.rows, other.columns)
        new_matrix.set_data(matrix)
        return new_matrix

    def __invert__(self):
        rows, columns = self.rows, self.columns
        matrix = [[] for y in range(columns)]
        for i in range(rows):
            for j in range(columns):
                matrix[j].append(self.data[i][j])

        new_matrix = Matrix(self.rows, self.columns)
        new_matrix.set_data(matrix)
        return new_matrix

    def __iadd__(self, other):
        return self + other

    def __isub__(self, other):
        return self - other

    def __eq__(self, other):
        if (not isinstance(other, Matrix) or self.rows != other.rows or self.columns != other.columns):
            return False
        else:
            for i in range(self.rows):
                for j in range(self.columns):
                    if (self.get_element((i, j)) != other.get_element((i, j))): return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)