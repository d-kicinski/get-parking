from pyomo.environ import *
import random
#random.seed(a="Na przypale albo wcale")

# Creation of a Concrete Model
m = ConcreteModel()


DRIVER_NUM = 10
PARKING_NUM = 2
PARKING_CAPACITY = 8
PARKING_MAX_PRICE = 0.6

# Brakujące miejsca

if DRIVER_NUM > PARKING_NUM * PARKING_CAPACITY:
    MISSING_PARKING_PLACES = DRIVER_NUM - PARKING_NUM * PARKING_CAPACITY
else:
    MISSING_PARKING_PLACES = 0


m.L = 5000

m.alpha = 1.0
m.gamma = 0.0

m.alpha_price = 1.2
m.gamma_price = 0.2
#m.eps = 0.05
m.eps =  1/(DRIVER_NUM*PARKING_NUM)
#m.eps2 = 1/(PARKING_NUM  * 5)


# cena
X_a = {1:5.5,
       2:5.5,
       3:5.5,
       4:6.5,
       5:6.0,
       6:1.5,
       7:1.5,
       8:1.5,
       9:1.0,
       10:1.5}#, 11:0.5 , 12:0.5 , 13:0.5 , 14:0.5 , 15:0.5 , 16:0.5, 17:0.5,
       #18:1000.5, 19:0.5, 20:0.5 }

X_r = {1:7.5,
       2:7.5,
       3:7.5,
       4:8.5,
       5:8.0,
       6:3.5,
       7:3.5,
       8:3.5,
       9:3.0,
       10:3.5}
# 11:4.0 , 12:6.0 , 13:8.0 , 14:10.0 , 15:30.0 , 16:32.0,
       #17:34.0, 18:36.0, 19:38.0, 20:40.0}


T1 = {
    (1, 1):  2000, (1, 2): 20000,
    (2, 1):  2000, (2, 2): 20000,
    (3, 1):  2000, (3, 2): 20000,
    (4, 1):  2000, (4, 2): 20000,
    (5, 1):  2000, (5, 2): 20000,
    (6, 1):  2000, (6, 2): 20000,
    (7, 1):  2000, (7, 2): 20000,
    (8, 1):  2000, (8, 2): 20000,
    (9, 1):  2000, (9, 2): 20000,
    (10,1):  2000, (10,2): 20000
    #(11, 1):  2000, (11, 2): 10000,
    #(12, 1):  2000, (12, 2): 10000,
    #(13, 1):  2000, (13, 2): 10000,
    #(14, 1):  2000, (14, 2): 10000,
    #(15, 1):  2000, (15, 2): 10000,
    #(16, 1):  2000, (16, 2): 10000,
    #(17, 1):  2000, (17, 2): 10000,
    #(18, 1):  2000, (18, 2): 10000,
    #(19, 1):  2000, (19, 2): 10000,
    #(20,1):  2000, (20,2): 10000,
}

T1_a = {
    (1, 1): 1000, (1,2):  1000,
    (2, 1): 1000, (2,2):  1000,
    (3, 1): 1000, (3,2):  1000,
    (4, 1): 1000, (4,2):  1000,
    (5, 1): 1000, (5,2):  1000,
    (6, 1): 1000, (6,2):  1000,
    (7, 1): 1000, (7,2):  1000,
    (8, 1): 1000, (8,2):  1000,
    (9, 1): 1000, (9,2):  1000,
    (10,1): 1000, (10,2): 1000
    #(11, 1): 1000, (11,2):  1000,
    #(12, 1): 1000, (12,2):  1000,
    #(13, 1): 1000, (13,2):  1000,
    #(14, 1): 1000, (14,2):  1000,
    #(15, 1): 1000, (15,2):  1000,
    #(16, 1): 1000, (16,2):  1000,
    #(17, 1): 1000, (17,2):  1000,
    #(18, 1): 1000, (18,2):  1000,
    #(19, 1): 1000, (19,2):  1000,
    #(20,1): 1000, (20,2): 1000,
}

T1_r = {
    (1, 1): 11000, (1, 2): 11000,
    (2, 1): 11000, (2, 2): 11000,
    (3, 1): 11000, (3, 2): 11000,
    (4, 1): 11000, (4, 2): 11000,
    (5, 1): 11000, (5, 2): 11000,
    (6, 1): 11000, (6, 2): 11000,
    (7, 1): 11000, (7, 2): 11000,
    (8, 1): 11000, (8, 2): 11000,
    (9, 1): 11000, (9, 2): 11000,
    (10,1): 11000, (10,2): 11000
    #(11, 1): 11000, (11, 2): 11000,
    #(12, 1): 11000, (12, 2): 11000,
    #(13, 1): 11000, (13, 2): 11000,
    #(14, 1): 11000, (14, 2): 11000,
    #(15, 1): 11000, (15, 2): 11000,
    #(16, 1): 11000, (16, 2): 11000,
    #(17, 1): 11000, (17, 2): 11000,
    #(18, 1): 11000, (18, 2): 11000,
    #(19, 1): 11000, (19, 2): 11000,
    #(20,1): 11000,  (20,2): 11000
}


#X_a = {i: random.uniform(1.01, 1.5) for i in range(1, DRIVER_NUM+1)}
#X_r = {i: random.uniform(7.5, 10.0) for i in range(1, DRIVER_NUM+1)}

'''
# droga
#T1 = {(i,j): random.randint(2000, 10000) for i in range(1, DRIVER_NUM+1) for j
      #in range(1, PARKING_NUM+1)}
#
#T2 = {(i,j): random.randint(50, 500) for i in range(1, DRIVER_NUM+1) for j
      #in range(1, PARKING_NUM+1)}
#
#T1_a = {(i,j): random.randint(100, 1000) for i in range(1, DRIVER_NUM+1) for j
      #in range(1, PARKING_NUM+1)}
#
#T2_a = {(i,j): random.randint(2, 100) for i in range(1, DRIVER_NUM+1) for j
      #in range(1, PARKING_NUM+1)}
#
#T1_r = {(i,j): random.randint(8000, 20000) for i in range(1, DRIVER_NUM+1) for j
      #in range(1, PARKING_NUM+1)}
#
#T2_r = {(i,j): random.randint(500, 1000) for i in range(1, DRIVER_NUM+1) for j
      #in range(1, PARKING_NUM+1)}
'''

# Zbiory i indeksy
m.m = Param(within=PositiveIntegers, initialize=DRIVER_NUM)
m.n = Param(within=PositiveIntegers, initialize=PARKING_NUM)

# Zbiory
m.M = RangeSet(1, m.m, doc="Zbior klientow")
m.N = RangeSet(1, m.n, doc="Zbior parkingow")


global L
L = 2
m.K =  RangeSet(1, L-1)
m.K_ar = RangeSet(1, L)


# Parametry
m.T1 = Param(m.M, m.N, initialize=T1, doc="Czas dojazdu do parkingu")
# m.T2 = Param(m.M, m.N, initialize=T2, doc="Czas dojscia do miejsca docelowego")
m.U = Param(m.M, m.N, doc="Zuzycie paliwa")
m.Q = Param(m.N, doc="Jakosc parkingu")

m.T1_a = Param(m.M, m.N, initialize=T1_a, doc="Czas dojazdu do parkingu")
# m.T2_a = Param(m.M, m.N, initialize=T2_a, doc="Czas dojazdu do miejsca docelowego")
m.U_a = Param(m.M, m.N, doc="Zuzycie paliwa")
m.Q_a = Param(m.N, doc="Jakosc parkingu")
m.X_a = Param(m.M, initialize=X_a, doc="Aspiracja do ceny")

m.T1_r = Param(m.M, m.N, initialize=T1_r, doc="Czas dojazdu do parkingu")
# m.T2_r = Param(m.M, m.N, initialize=T2_r, doc="Czas dojazdu do miejsca docelowego")
m.U_r = Param(m.M, m.N, doc="Zuzycie paliwa")
m.Q_r = Param(m.N, doc="Jakosc parkingu")
m.X_r = Param(m.M, initialize=X_r, doc="Rezerwacja do ceny")

#m.K_ = [m.T1, m.T2, m.U, m.Q]
#m.K_a = [m.T1_a, m.T2_a, m.U, m.Q_a, m.X_a]
#m.K_r = [m.T1_r, m.T2_r, m.U_r, m.Q_r, m.X_r]

#m.K_ = [m.T1, m.T2]
#m.K_a = [m.T1_a, m.T2_a, m.X_a]
#m.K_r = [m.T1_r, m.T2_r, m.X_r]

m.K_ = [m.T1]
m.K_a = [m.T1_a, m.X_a]
m.K_r = [m.T1_r, m.X_r]





# Zmienne decyzyjne
m.V = Var(m.M, m.N, within=Binary)
m.x = Var(m.N, within=PositiveReals, bounds=(0.0, None))
m.a = Var(m.M, m.K_ar, within=Reals)
m.a_ = Var()


# Funkcje pomocnicze
def C_m(m, i, j, k):
    """ Zwraca wartosc k-tego kryterium dla i-tego klienta i j-tego parkingu"""
    k=k-1
    if k in (0,1):
        C = m.K_[k][i,j]
    elif k in (2,):
        C = m.K_[k][i]
    else:
        raise ValueError("brak kryterium dla k={}".format(k))
    return C


def Ca_m(m, i, j, k):
    k=k-1
    if k in (0,1):  # droga
        C = m.K_a[k][i,j]
    elif k in (2,):  # cena
        C = m.K_a[k][i]
    else:
        raise ValueError("brak kryterium dla k={}".format(k))
    return C


def Cr_m(m, i, j, k):
    k=k-1
    if k in (0,1):
        C = m.K_r[k][i,j]
    elif k in (2,):
        C = m.K_r[k][i]
    else:
        raise ValueError("brak kryterium dla k={}".format(k))
    return C



# Ograniczenia
if DRIVER_NUM <= PARKING_NUM * PARKING_CAPACITY:
    # Więcej miejsc niż kierowców -> dokładnie jeden parking dla każdego klienta
    def assigment_rule(m, i):
        value = sum(m.V[i,j] for j in m.N)
        return value == 1
    m.assigment = Constraint(m.M, rule=assigment_rule)

    # Ograniczenie zapobiegające przepełnieniu parkingu
    def capacity_rule(m, j):
        value = sum(m.V[i,j] for i in m.M)
        return value <= PARKING_CAPACITY
    m.capacity = Constraint(m.N, rule=capacity_rule)
else:
    # To jeszcze chyba nie działa
    # Jeden klient maksymalnie dostanie jeden parking
    def assigment_rule(m, i):
        value = sum(m.V[i,j] for j in m.N)
        return value <= 1
    m.assigment = Constraint(m.M, rule=assigment_rule)

    # Więcej kierowców niż miejsc -> każdy parking załadowany do pełna
    def capacity_rule(m, j):
        value = sum(m.V[i,j] for i in m.M)
        return value == PARKING_CAPACITY
    m.capacity = Constraint(m.N, rule=capacity_rule)



## this gud
def price_ref1(m, i, j):
    global L
    k=L
    #val = (-1/m.X_a[i]**2) * (( m.x[j] - m.X_a[i] /
                     #(m.X_r[i]-m.X_a[i]) - (1-m.V[i,j])*m.L)

     val =  m.gamma_price * (m.x[j]-m.X_a[i]*m.V[i,j])/(m.X_r[i]-m.X_a[i]) - (1-m.V[i,j])*m.L

    return m.a[i,k] >= val
m.price_ref1 = Constraint(m.M, m.N, rule=price_ref1)


def price_ref2(m, i, j):
    global L
    k=L
    val = ((m.x[j] - m.X_a[i]*m.V[i,j]) /
                     (m.X_r[i]-m.X_a[i])) - (1-m.V[i,j])*m.L

    return m.a[i,k] >= val
m.price_ref2 = Constraint(m.M, m.N,rule=price_ref2)


def price_ref3(m, i, j):
    global L
    k=L
    val =  m.alpha_price * (( m.x[j] - m.X_r[i]*m.V[i,j]) /
                     (m.X_r[i]-m.X_a[i])) + 1 - (1-m.V[i,j])*m.L

    return m.a[i,k] >= val
m.price_ref3 = Constraint(m.M, m.N ,rule=price_ref3)


# Metoda punktu referencyjnego dla pozostałych
def ref1(m,i,k):
    val = m.gamma * sum(m.V[i,j] * ((C_m(m,i,j,k) - Ca_m(m,i,j,k)) /
    (Cr_m(m,i,j,k) - Ca_m(m,i,j,k))) for j in m.N)

    return m.a[i,k] >= val
m.ref1 = Constraint(m.M, m.K, rule=ref1)

def ref2(m,i,k):
    val = sum(m.V[i,j] *((C_m(m,i,j,k) - Ca_m(m,i,j,k)) /
    (Cr_m(m,i,j,k) - Ca_m(m,i,j,k))) for j in m.N)

    return m.a[i,k] >= val
m.ref2 = Constraint(m.M, m.K, rule=ref2)


def ref3(m,i,k):
    val = m.alpha * sum(m.V[i,j] * ((C_m(m,i,j,k) - Cr_m(m,i,j,k)) /
    (Cr_m(m,i,j,k) - Ca_m(m,i,j,k))) for j in m.N) + 1

    return m.a[i,k] >= val
m.ref3 = Constraint(m.M, m.K, rule=ref3)


# idk
def idk(m,i,k):
    return m.a_ >= m.a[i,k]
m.idk = Constraint(m.M, m.K_ar, rule=idk)


def objective_rule(m):
     return m.a_ + (m.eps * (sum(m.a[i,k] for i in m.M for k in m.K_ar) +
                    MISSING_PARKING_PLACES * m.L))

m.objective = Objective(rule=objective_rule, sense=minimize, doc='Define objective function')


def pyomo_postprocess(options=None, instance=None, results=None):
    m.V.display()
    m.x.display()
    m.a.display()
    m.a_.display()
    m.objective.display()
    print("Sum(a_ij) = ", sum(value(m.a[i,k]) for i in m.M for k in m.K_ar))

    val = sum(value(m.a[i,k]) for i in m.M for k in m.K_ar) + MISSING_PARKING_PLACES * m.L
    print("Sum po korekcji:", sum(value(m.a[i,k]) for i in m.M for k in m.K_ar) +
                    MISSING_PARKING_PLACES * m.L)
    print("Sum po korekcji z eps({}): {}".format(m.eps, m.eps*val))
    print("eps = ", m.eps)



def calc_prices():
    prices = []

    parking 1 : ceny

    V = values(m.V)
    for j in m.N:
        asp_prices =[]
        for i in m.M:
            if V[i,j] == 1:
                asp_prices.append(X_a[i]
        prices.appen(max(asp_prices))

    return prices



if __name__ == '__main__':
    # This emulates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("cplex")
    #opt = SolverFactory("clp")
    #opt = SolverFactory("glpk")
    #opt = SolverFactory("ipopt")
    #opt = SolverFactory("couenne")
    #opt.set_instance(m)

    #option = {
        #"mip strategy miqcpstrat ": 1
    #}
    #results = opt.solve(m, tee=True,options=option, keepfiles=True)

    results = opt.solve(m) #, tee=True, keepfiles=True)
    #sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + '-'*60)
    pyomo_postprocess(None, m, results)

    print(calc_prices())

#m.pprint()
