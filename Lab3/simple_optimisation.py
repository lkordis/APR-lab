from math import sqrt

def research(f,xp, dx=0.5):
    x = list(xp)
    for i in range(len(x)):
        P = f(x)
        x[i] += dx
        N = f(x)
        if N > P:
            x[i] -= 2*dx
            N = f(x)
            if N > P:
                x[i] += dx
    return x

def hooke_jeeves_search(f,x0,e=10e-6):
    xp,xb = list(x0), list(x0)
    dx = 0.5
    
    while(dx > 0.5*e):
        xn = research(f,xp,dx)
        if f(xn)<f(xb):
            xp = [2*xn[j] - xb[j] for j in range(len(xb))]
            xb = xn
        else:
            dx *= 0.5
            xp = list(xb)
            
    return xb

def unimodal_interval(f, starting_point, h = 1):
    l = starting_point - h
    r = starting_point + h
    m = starting_point
    step = 1
    
    fm = f(starting_point)
    fl,fr = f(l),f(r)
    
    if(fm < fr and fm < fl):
        return l,r
    elif(fm > fr):
        while(fm > fr):
            l,m,fm = m,r,fr
            step *= 2
            r = starting_point + h * step
            fr = f(r)
    else:
        while(fm > fl):
            r,m,fm = m,l,fl
            step *= 2
            l = starting_point - h * step;
            fl = f(l);
    return l,r

def golden_ratio(f, interval = None, starting_point = None, e=10e-6, trace=False):
    k = 0.5*(sqrt(5)-1)
    steps = 0
    
    if interval == None:
        a,b = unimodal_interval(f, starting_point=starting_point)
    else:
        a,b = interval
        
    c = b - k*(b-a)
    d = a + k*(b-a)
    fc = f(c)
    fd = f(d)
    
    while((b-a) > e):
        if(fc < fd):
            b = d
            d = c
            c = b - k*(b-a)
            fd = fc
            fc = f(c)
        else:
            a = c
            c = d
            d = a + k*(b-a)
            fc = fd
            fd = f(d)
        steps += 1
        if trace:
            print("a  c  d  b")
            print(a,c,d,b)
    
    return (a+b)/2
