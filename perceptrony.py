"""
Autor: Maciej Falbogowski
drobna zmiana: m
"""
import random
 
class Variable: # x albo w
    def __init__(self, name, value=0):
        self.value = value
        self.name = name
    def __str__(self):
        return "{}={}".format(self.name, self.value)
 
class Node:
    def __init__(self, connections, activation):
        """
        connections to lista: (Variable albo Node, Variable reprezentująca wagę)
        """
        self._connections = connections
        self._activation = activation
    @property
    def value(self):
        value = sum([node.value * weight.value for node, weight in self._connections])
        return self._activation(value)
 
def check(X, output_node, truth_table):
    for x_list, y in TRUTH_TABLE:
        for variable, x in zip(X, x_list):
            variable.value = x
        if output_node.value != y:
            return False
    return True
 
def solve(X, weights, output_node, iters=10, weights_decimal_places=0, n=1000, *, truth_table):
    """
    wagi będą szukane w przedziale [-iters, iters]
    X: lista Variable reprezentująca x'y w zadaniu. len(X) powinien równać się ilości x'ów w tabelce prawdy
    weights: lista wag do modyfikacji.
    output_node: perceptron zwracający wynik
    weights_decimal_places: Do ilu miejsc po przecinku dopuszczać wartości wag. 0 oznacza, że wagi będą całkowite
    """
    while True:
        r = 1
        for _ in range(iters+1):
            for _ in range(n): 
                for weight in weights:
                    exp = 10 ** weights_decimal_places
                    weight.value = random.randint(-r * exp, r * exp) / exp
                if check(X, output_node, truth_table):
                    print("Znaleziono rozwiązanie!")
                    for w in weights:
                        print(w)
                    return
            r += 1
        weights_decimal_places += 1
 
 
#
#  Obszar studenta
#
 
#funkcja aktywacji
def activation(x):
    #Funkcja skokowa Heaviside
    #zamieńcie na inne jeśli trzeba
    return 0 if x < 0 else 1
 
#tableka prawdy do zmiany.
# równoważność logiczna
TRUTH_TABLE = [
   #[[x1, x2...], y]
    [[0, 0], 1],
    [[0, 1], 0],
    [[1, 0], 0],
    [[1, 1], 1],
]
# alternatywa wykluczająca (xor)
# TRUTH_TABLE = [
#    #[[x1, x2...], y]
#     [[0, 0], 0],
#     [[0, 1], 1],
#     [[1, 0], 1],
#     [[1, 1], 0],
# ]


 
#Składowe grafu
x1 = Variable("x1")
x2 = Variable("x2")

x10 = Variable("x10", value=1)
x20 = Variable('x20', value=1)
x30 = Variable('x30', value=1)
w10 = Variable("w10")
w11 = Variable("w11")
w12 = Variable("w12", value=-1)
w20 = Variable('w20')
w21 = Variable('w21', value=1)
w22 = Variable('w22', value=1)
w30 = Variable('w30')
w31 = Variable('w31')
w32 = Variable('w32')

 
#Struktura grafu (zmienna, waga)
y1 = Node([
    (x1, w11),
    (x2, w12),
    (x10, w10),
], activation=activation)

y2 = Node([
    (x1, w21),
    (x2, w22),
    (x20, w20),
], activation=activation)
 
z = Node([
    (y1, w31),
    (y2, w32),
    (x30, w30),
], activation=activation)
 
X = [x1, x2]
weights = [w10, w11, w20, w30, w31, w32] #rozwiązanie będzie szukane poprzez zmienianie wartości tych zmiennych
solve(X=X, weights=weights, output_node=z, weights_decimal_places=0, truth_table=TRUTH_TABLE)