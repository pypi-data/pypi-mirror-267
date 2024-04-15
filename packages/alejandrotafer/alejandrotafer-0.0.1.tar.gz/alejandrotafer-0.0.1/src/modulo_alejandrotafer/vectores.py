def suma_vectores(x,y):
    n=len(x)
    r=[]
    for i in range(n):
        r.append(x[i]+y[i])
    return r


def resta_vectores(x,y):
    n=len(x)
    r=[]
    for i in range(n):
        r.append(x[i]-y[i])
    return r


def multiplicacion_vectores(x,y):
    n=len(x)
    r=[]
    for i in range(n):
        r.append(x[i]*y[i])
    return r


def division_vectores(x,y):
    n=len(x)
    r=[]
    for i in range(n):
        r.append(x[i]/y[i])
    return r
