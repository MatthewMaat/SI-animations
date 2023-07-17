from graph import *

def addd(a,b,player):
    #add edge from a to b and add it to the strategy
    #of player "player", 2 means do not add to strategy
    global G
    global init0
    global init1
    e=Edge(a,b)
    G.add_edge(e)
    if player==0:
        init0.add(e)
    elif player==1:
        init1.add(e)

def create_phicounter(n):
    #create exponential counterexample for symmetric strategy iteration
    # input: n
    # output:
    #  G (graph G_n)
    #  strat0 (initial player 0 strategy as set of edges)
    #  strat1 (initial player 1 strategy as set of edges)
    #  scalef (scaling factor for rendering)
    global G
    init0=set()
    init1=set()
    scalef = 10
    G=MyGraph(True, 0, False)
    x=Vertex(G, 1, False, 0, pos='0,'+str(2*n))
    G.add_vertex(x)
    e=Edge(x,x)
    G.add_edge(e)
    init0.add(e)
    y=Vertex(G, 2*n+4, True, 1, pos='2,'+str(2*n))
    G.add_vertex(y)
    e=Edge(y,x)
    G.add_edge(e)
    init1.add(e)
    r0f = Vertex(G, 3, False, 2, pos='-0.01,0')
    G.add_vertex(r0f)
    r1f = Vertex(G, 4, True, 3, pos='2,0')
    G.add_vertex(r1f)
    r00=r0f
    r11=r1f
    r0=r0f
    r1=r1f
    for i in range(2,n+1):
        r0=Vertex(G, 2*i+1, False, 2*i, pos='0,'+str(2*(i-1)))
        G.add_vertex(r0)
        r1=Vertex(G, 2*i+2, True, 2*i+1, pos='2,'+str(2*(i-1)))
        G.add_vertex(r1)
        G.add_edge(Edge(r0, r0f))
        G.add_edge(Edge(r1,r1f))
        G.add_edge(Edge(r00,r1))
        e=Edge(r00, r0)
        G.add_edge(e)
        init0.add(e)
        e=Edge(r11, r1)
        G.add_edge(e)
        init1.add(e)
        G.add_edge(Edge(r11, r0))
        r00=r0
        r11=r1
    G.add_edge(Edge(r0, y))
    e=Edge(r0, x)
    G.add_edge(e)
    init0.add(e)
    e=Edge(r1, y)
    G.add_edge(e)
    init1.add(e)
    G.add_edge(Edge(r1, x))
    return G,init0, init1, scalef

def create_relaxed_phicounter(n):
    #Create a simpler (but less general) version of the counterexample for generalized symmetric strategy iteration
    # input: n
    # output:
    #  G (graph G_n)
    #  strat0 (initial player 0 strategy as set of edges)
    #  strat1 (initial player 1 strategy as set of edges)
    #  scalef (scaling factor for rendering)
    global G
    init0 = set()
    init1 = set()
    scalef=12
    G = MyGraph(True, 0, False)
    x = Vertex(G, 1, False, 0, pos='0,'+str(3*n))
    G.add_vertex(x)
    e = Edge(x, x)
    G.add_edge(e)
    init0.add(e)
    y = Vertex(G, 2, True, 1, pos='3,'+str(3*n))
    G.add_vertex(y)
    e = Edge(y, y)
    G.add_edge(e)
    init1.add(e)
    r0=x
    r1=y
    r00=Vertex(G, 5, False, 6*n, pos='0,0')
    r10=Vertex(G, 6, True, 6*n+1, pos='3,0')
    G.add_vertex(r00)
    G.add_vertex(r10)
    for i in range(n):
        l1=Vertex(G,3, False, 6*i+2, pos='-1,'+str(3*(n-i-1)+1))
        l2=Vertex(G,3, False, 6*i+3, pos='1,'+str(3*(n-i-1)+1))
        l3=Vertex(G,4, True, 6*i+4, pos='2,'+str(3*(n-i-1)+1))
        l4=Vertex(G,4, True, 6*i+5, pos='4,'+str(3*(n-i-1)+1))
        G.add_vertex(l1)
        G.add_vertex(l2)
        G.add_vertex(l3)
        G.add_vertex(l4)
        e=Edge(l1,r0)
        G.add_edge(e)
        init0.add(e)
        G.add_edge(Edge(l2,r1))
        G.add_edge(Edge(l1,l2))
        e=Edge(l2,l1)
        G.add_edge(e)
        init0.add(e)
        if i<n-1:
            G.add_edge(Edge(l1,r00))
            G.add_edge(Edge(l2,r00))
        e = Edge(l4, r1)
        G.add_edge(e)
        init1.add(e)
        G.add_edge(Edge(l3, r0))
        G.add_edge(Edge(l4, l3))
        e = Edge(l3, l4)
        G.add_edge(e)
        init1.add(e)
        if i<n-1:
            G.add_edge(Edge(l3, r10))
            G.add_edge(Edge(l4, r10))
        if i<n-1:
            r0=Vertex(G, 2*n+3-2*i, False, 6*i+6, pos='0,'+str(3*(n-i-1)))
            G.add_vertex(r0)
            r1=Vertex(G, 2*n+4-2*i, True, 6*i+7, pos='3,'+str(3*(n-i-1)))
            G.add_vertex(r1)
        else:
            r0=r00
            r1=r10
        e=Edge(r0, l1)
        G.add_edge(e)
        init0.add(e)
        G.add_edge(Edge(r0,l2))
        e = Edge(r1, l4)
        G.add_edge(e)
        init1.add(e)
        G.add_edge(Edge(r1,l3))
        for i in range(len(G.vertices)):
            G.vertices[i].index=i
    return G, init0, init1, scalef

def create_casual_phicounter(n):
    #create counterexample G_n that works for the generalization of symmetric strategy iteration
    #input: n
    #output:
    #  G (graph G_n)
    #  strat0 (initial player 0 strategy as set of edges)
    #  strat1 (initial player 1 strategy as set of edges)
    #  scalef (scaling factor for rendering)
    global G
    init0 = set()
    init1 = set()
    scalef=15
    N=16*n+16
    G = MyGraph(True, 0, False)
    x = Vertex(G, 1, False, 0, pos='0,'+str(2*n))
    G.add_vertex(x)
    e = Edge(x, x)
    G.add_edge(e)
    init0.add(e)
    y = Vertex(G, N+2*n+2, True, 1, pos='2,'+str(2*n))
    G.add_vertex(y)
    e = Edge(y, x)
    G.add_edge(e)
    init1.add(e)
    r0=x
    r1=y
    r00=Vertex(G, N+1, False, pos='0,0')
    r10=Vertex(G, N+2, True, pos='2,0')
    G.add_vertex(r00)
    G.add_vertex(r10)
    for j in range(n):
        i=n-j
        l1=Vertex(G,14*i+1, False, pos='-0.5,'+str(2*i-1.5))
        l2=Vertex(G,14*i+3, False, pos='0.5,'+str(2*i-1.5))
        l3=Vertex(G,14*i+8, True, pos='1.5,'+str(2*i-1.5))
        l4=Vertex(G,14*i+10, True, pos='2.5,'+str(2*i-1.5))
        l5=Vertex(G,14*i+4, True, pos='-0.5,'+str(2*i-1))
        l6=Vertex(G,14*i+6,True, pos='0.5,'+str(2*i-1))
        l7=Vertex(G,14*i+11, False, pos='1.5,'+str(2*i-1))
        l8=Vertex(G,14*i+13, False, pos='2.5,'+str(2*i-1))
        G.add_vertex(l1)
        G.add_vertex(l2)
        G.add_vertex(l3)
        G.add_vertex(l4)
        G.add_vertex(l5)
        G.add_vertex(l6)
        G.add_vertex(l7)
        G.add_vertex(l8)
        e=Edge(l1,l5)
        G.add_edge(e)
        init0.add(e)
        G.add_edge(Edge(l2,l6))
        G.add_edge(Edge(l1,l2))
        e=Edge(l2,l1)
        G.add_edge(e)
        init0.add(e)
        G.add_edge(Edge(l5, l2))
        G.add_edge(Edge(l6, l1))
        e=Edge(l5, r0)
        G.add_edge(e)
        init1.add(e)
        e=Edge(l6, r1)
        G.add_edge(e)
        init1.add(e)
        if j<n-1:
            G.add_edge(Edge(l1,r00))
            G.add_edge(Edge(l2,r00))
        e = Edge(l4, l8)
        G.add_edge(e)
        init1.add(e)
        G.add_edge(Edge(l3, l7))
        G.add_edge(Edge(l4, l3))
        e = Edge(l3, l4)
        G.add_edge(e)
        init1.add(e)
        G.add_edge(Edge(l7,l4))
        G.add_edge(Edge(l8,l3))
        e=Edge(l7, r0)
        G.add_edge(e)
        init0.add(e)
        e=Edge(l8,r1)
        G.add_edge(e)
        init0.add(e)
        if j<n-1:
            G.add_edge(Edge(l3, r10))
            G.add_edge(Edge(l4, r10))
        if j<n-1:
            r0=Vertex(G, N+2*i-1, False, pos='0,'+str(2*i-2))
            G.add_vertex(r0)
            r1=Vertex(G, N+2*i, True, pos='2,'+str(2*i-2))
            G.add_vertex(r1)
        else:
            r0=r00
            r1=r10
        e=Edge(r0, l1)
        G.add_edge(e)
        init0.add(e)
        G.add_edge(Edge(r0,l2))
        e = Edge(r1, l4)
        G.add_edge(e)
        init1.add(e)
        G.add_edge(Edge(r1,l3))
        for i in range(len(G.vertices)):
            G.vertices[i].index=i
    return G, init0, init1, scalef

def create_switchbest_counter(n):
    #create binary counter example for switch-best improvement rule by Friedmann
    # input: n
    # output:
    #  G (graph G_n)
    #  strat0 (initial player 0 strategy as set of edges)
    #  strat1 (initial player 1 strategy as set of edges)
    #  scalef (scaling factor for rendering)
    global G,init0,init1
    init0 = set()
    init1 = set()
    scalef = 50
    A=["THIS IS A FILLER ITEM THAT SHOULD NOT BE SELECTED"]
    F=[0 for j in range(n+1)]
    GG=[0 for j in range(n+1)]
    G = MyGraph(True, 0, False)
    s=Vertex(G, 20*n+2, False, pos='10,'+str(4*n))
    r=Vertex(G, 20*n+4, False, pos='10,-1')
    x=Vertex(G, 1, True, pos='15,3')
    c=Vertex(G, 20*n, True, pos='0,0')
    G.add_vertex(s)
    G.add_vertex(r)
    G.add_vertex(x)
    G.add_vertex(c)
    addd(c,r,1)
    addd(s,x,0)
    addd(r,x,0)
    addd(x,x,1)
    t=Vertex(G, 8*n+3, False, pos='0,1') #t_1 and a_1
    a=Vertex(G, 8*n+4, True, pos='1,1')
    G.add_vertex(t)
    G.add_vertex(a)
    addd(t,s,2)
    addd(t,r,2)
    addd(t,c,0)
    addd(a,t,1)
    A.append(a)
    for i in range(2,6*n-1): #construct deceleration lane
        tnew=Vertex(G,8*n+2*i+1, False, pos='0,'+str(i))
        G.add_vertex(tnew)
        if i<=3:
            addd(tnew, t, 0)
            addd(tnew, r, 2)
        else:
            addd(tnew, t, 2)
            addd(tnew, r, 0)
        addd(tnew, s, 2)
        t=tnew
        a=Vertex(G,8*n+2*i+2,True, pos='1,'+str(i))
        G.add_vertex(a)
        A.append(a)
        addd(a,t,1)
    for i in range(n,0, -1): #construct bits from high to low
        d1=Vertex(G,8*i+1-6, False, pos='5,'+str(4*i-1))
        G.add_vertex(d1)
        d2=Vertex(G, 8 * i + 3-6, False, pos='4,'+str(4*i-2))
        G.add_vertex(d2)
        d3=Vertex(G, 8 * i + 5-6, False, pos='5,'+str(4*i-3))
        G.add_vertex(d3)
        ei=Vertex(G, 8 * i + 6-6, True, pos='6,'+str(4*i-2))
        G.add_vertex(ei)
        yi = Vertex(G, 8 * i + 7-6, False, pos='8,'+str(4*i-4))
        G.add_vertex(yi)
        gi = Vertex(G, 8 * i + 8-6, False, pos='9,'+str(4*i-4))
        G.add_vertex(gi)
        GG[i]=gi
        k = Vertex(G, 20*n+4*i+3, False, pos='10,'+str(4*i-2))
        G.add_vertex(k)
        f = Vertex(G, 20*n+4*i+5, True, pos='7,'+str(4*i-4))
        G.add_vertex(f)
        F[i]=f
        h = Vertex(G, 20*n+4*i+6, True, pos='8,'+str(4*i-2))
        G.add_vertex(h)
        addd(d1,s,2)
        addd(d1,c,2)
        addd(d1,d2,0)
        for j in range(2*i-1):
            addd(d1,A[3*j+3],2)
        addd(d2,d3,2)
        addd(d2,A[2],0)
        for j in range(1, 2*i-1):
            addd(d2,A[3*j+2],2)
        addd(d3, ei, 2)
        addd(d3, A[1], 0)
        for j in range(1, 2*i):
            addd(d3,A[3*j+1],2)
        addd(ei, h, 1)
        addd(ei,d1, 2)
        addd(yi, f, 2)
        addd(yi,k, 0)
        addd(gi, yi, 2)
        addd(gi, k, 0)
        addd(k, x,0)
        for j in range(i+1,n+1):
            addd(k, GG[j], 2)
        addd(f,ei, 1)
        addd(h,k,1)
    for j in range(1,n+1):
        addd(s, F[j],2)
        addd(r, GG[j],2)
    return G, init0, init1, scalef

#TODO: make switch all function
def create_switchall_counter(n):
    #create binary counter example for switch-all improvement rule by Friedmann
    # input: n
    # output:
    #  G (graph G_n)
    #  strat0 (initial player 0 strategy as set of edges)
    #  strat1 (initial player 1 strategy as set of edges)
    #  scalef (scaling factor for rendering)
    global G,init0,init1
    init0 = set()
    init1 = set()
    scalef = 50
    A=["THIS IS A FILLER ITEM THAT SHOULD NOT BE SELECTED"]
    F=[0 for j in range(n+1)]
    GG=[0 for j in range(n+1)]
    G = MyGraph(True, 0, False)
    s=Vertex(G, 20*n+2, False, pos='10,'+str(4*n))
    r=Vertex(G, 20*n+4, False, pos='10,-1')
    x=Vertex(G, 1, True, pos='15,3')
    c=Vertex(G, 20*n, True, pos='0,0')
    G.add_vertex(s)
    G.add_vertex(r)
    G.add_vertex(x)
    G.add_vertex(c)
    addd(c,r,1)
    addd(s,x,0)
    addd(r,x,0)
    addd(x,x,1)
    t=Vertex(G, 8*n+3, False, pos='0,1') #t_1 and a_1
    a=Vertex(G, 8*n+4, True, pos='1,1')
    G.add_vertex(t)
    G.add_vertex(a)
    addd(t,s,2)
    addd(t,r,2)
    addd(t,c,0)
    addd(a,t,1)
    A.append(a)
    for i in range(2,6*n-1): #construct deceleration lane
        tnew=Vertex(G,8*n+2*i+1, False, pos='0,'+str(i))
        G.add_vertex(tnew)
        if i<=3:
            addd(tnew, t, 0)
            addd(tnew, r, 2)
        else:
            addd(tnew, t, 2)
            addd(tnew, r, 0)
        addd(tnew, s, 2)
        t=tnew
        a=Vertex(G,8*n+2*i+2,True, pos='1,'+str(i))
        G.add_vertex(a)
        A.append(a)
        addd(a,t,1)
    for i in range(n,0, -1): #construct bits from high to low
        d1=Vertex(G,8*i+1-6, False, pos='5,'+str(4*i-1))
        G.add_vertex(d1)
        d2=Vertex(G, 8 * i + 3-6, False, pos='4,'+str(4*i-2))
        G.add_vertex(d2)
        d3=Vertex(G, 8 * i + 5-6, False, pos='5,'+str(4*i-3))
        G.add_vertex(d3)
        ei=Vertex(G, 8 * i + 6-6, True, pos='6,'+str(4*i-2))
        G.add_vertex(ei)
        yi = Vertex(G, 8 * i + 7-6, False, pos='8,'+str(4*i-4))
        G.add_vertex(yi)
        gi = Vertex(G, 8 * i + 8-6, False, pos='9,'+str(4*i-4))
        G.add_vertex(gi)
        GG[i]=gi
        k = Vertex(G, 20*n+4*i+3, False, pos='10,'+str(4*i-2))
        G.add_vertex(k)
        f = Vertex(G, 20*n+4*i+5, True, pos='7,'+str(4*i-4))
        G.add_vertex(f)
        F[i]=f
        h = Vertex(G, 20*n+4*i+6, True, pos='8,'+str(4*i-2))
        G.add_vertex(h)
        addd(d1,s,2)
        addd(d1,c,2)
        addd(d1,d2,0)
        for j in range(2*i-1):
            addd(d1,A[3*j+3],2)
        addd(d2,d3,2)
        addd(d2,A[2],0)
        for j in range(1, 2*i-1):
            addd(d2,A[3*j+2],2)
        addd(d3, ei, 2)
        addd(d3, A[1], 0)
        for j in range(1, 2*i):
            addd(d3,A[3*j+1],2)
        addd(ei, h, 1)
        addd(ei,d1, 2)
        addd(yi, f, 2)
        addd(yi,k, 0)
        addd(gi, yi, 2)
        addd(gi, k, 0)
        addd(k, x,0)
        for j in range(i+1,n+1):
            addd(k, GG[j], 2)
        addd(f,ei, 1)
        addd(h,k,1)
    for j in range(1,n+1):
        addd(s, F[j],2)
        addd(r, GG[j],2)
    return G, init0, init1, scalef

def create_highest_valuation_counter(n):
    #binary counter for highest valuation rule
    global G, init0, init1
    init0 = set()
    init1 = set()
    scalef = 10
    G = MyGraph(True, 0, False)
    N=5
    x = Vertex(G, 1, False, 0, pos='0,' + str(2 * n))
    G.add_vertex(x)
    e = Edge(x, x)
    G.add_edge(e)
    init0.add(e)
    y = Vertex(G, 4*N*(n+1), False, 1, pos='2,' + str(2 * n))
    G.add_vertex(y)
    e = Edge(y, x)
    G.add_edge(e)
    init0.add(e)
    aiprev = Vertex(G, 2*N, False, 2, pos='-0.01,0')
    G.add_vertex(aiprev)
    d1 = Vertex(G, 4*N, False, 3, pos='2,0')
    G.add_vertex(d1)
    fiprev = Vertex(G, 2*N-2, False, 3, pos='1.5,0.5')
    G.add_vertex(fiprev)
    addd(d1, fiprev, 0)
    for i in range(2, n + 1):
        ai = Vertex(G, N*(4*i-2), False, 2 * i, pos='0,' + str(2 * (i - 1)))
        G.add_vertex(ai)
        di = Vertex(G,4*N*i , False, 2 * i + 1, pos='2,' + str(2 * (i - 1)))
        G.add_vertex(di)
        fi = Vertex(G, N*(4*i-2)-2, False, 2 * i + 1, pos='1.5,' + str(2 * (i - 1)+0.5))
        G.add_vertex(fi)
        addd(aiprev, ai, 0)
        addd(aiprev, di, 2)
        addd(di, fi, 0)
        addd(fiprev, ai, 2)
        addd(fiprev, di, 0)
        fiprev=fi
        aiprev=ai
    addd(ai, x, 2)
    addd(ai, y, 0)
    addd(fi, x, 0)
    addd(fi, y, 2)
    return G, init0, init1, scalef

def create_lowest_valuation_counter(n):
    # binary counter for highest valuation rule
    global G, init0, init1
    init0 = set()
    init1 = set()
    scalef = 10
    G = MyGraph(True, 0, False)
    N = 5
    x = Vertex(G, 1, False, 0, pos='0,' + str(2 * n))
    G.add_vertex(x)
    e = Edge(x, x)
    G.add_edge(e)
    init0.add(e)
    y = Vertex(G, 2, False, 1, pos='2,' + str(2 * n))
    G.add_vertex(y)
    e = Edge(y, y)
    G.add_edge(e)
    init0.add(e)
    aiprev = Vertex(G, N, False, 2, pos='-0.01,0')
    G.add_vertex(aiprev)
    diprev = Vertex(G, 3 * N, False, 3, pos='2,0')
    G.add_vertex(diprev)
    for i in range(2, n + 1):
        ai = Vertex(G, N * (4 * i - 3), False, 2 * i, pos='0,' + str(2 * (i - 1)))
        G.add_vertex(ai)
        di = Vertex(G, N*(4*i-1), False, 2 * i + 1, pos='2,' + str(2 * (i - 1)))
        G.add_vertex(di)
        addd(aiprev, ai, 2)
        addd(aiprev, di, 0)
        addd(diprev, ai, 2)
        addd(diprev, di, 0)
        diprev = di
        aiprev = ai
    addd(ai, x, 0)
    addd(ai, y, 2)
    addd(di, x, 0)
    addd(di, y, 2)
    return G, init0, init1, scalef