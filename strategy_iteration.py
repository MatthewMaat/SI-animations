#functions that are used for strategy iteration

from graph import *
import math
import os
import imageio.v2 as imageio
from graphviz import *
from tqdm import tqdm
from counterexamples import *
from graph_io import *

def get_priority(v):
    return v.label

def raise_priorities(G):
    vertexlist = [v for v in G.vertices]
    vertexlist.sort(key=get_priority)
    scale = 0
    for i in range(1,len(vertexlist)):
        if i==12:
            pass
        if vertexlist[i-1].label==260 or vertexlist[i].label==260:
            pass
        if vertexlist[i-1].label == vertexlist[i].label + scale:
            scale += 2
        vertexlist[i].label += scale


def decompose_scc(G):
    #decompose G into strongly connected components
    decomp=[]
    reachedlists=[]
    reachablelists=[]
    remaining_vertices=set(G.vertices)
    while remaining_vertices!=set():
        r=list(remaining_vertices)
        r0=r[0]
        reachable={r0}
        reached={r0}
        stack=[r0]
        while len(stack)>0: #bfs what they can reach
            current_vertex=stack.pop(0)
            E=current_vertex.incidence
            for e in E:
                if e.tail==current_vertex:
                    if e.head not in reachable:
                        stack.append(e.head)
                        reachable.add(e.head)
        stack=[r0]
        while len(stack)>0: #bfs if they can be reached
            current_vertex=stack.pop(0)
            E=current_vertex.incidence
            for e in E:
                if e.head==current_vertex:
                    if e.tail not in reached:
                        stack.append(e.tail)
                        reached.add(e.tail)
        ints=reached.intersection(reachable)
        reachedlist=[]
        reachablelist=[]
        for d in range(len(decomp)):
            lizzt=list(decomp[d])
            el=lizzt[0]
            if el in reachable:
                reachablelist.append(d)
            elif el in reached:
                reachedlist.append(d)
        reachablelists.append(reachablelist)
        reachedlists.append(reachedlist)
        decomp.append(ints)
        remaining_vertices=remaining_vertices.difference(ints)
    for i in range(len(reachedlists)):
        for j in reachedlists[i]:
            reachablelists[j].append(i)
    return decomp, reachablelists #reachablelists[i] has components that component i can reach

def find_lambda(G, stratplayer):
    #find best cycle for a player in a strongly connected subgraph using BFS
    #G: graph, stratplayer: player doing the counterstrategy
    bestval=-1
    bestvertex = None
    for v in G.vertices:
        reachable = set()
        stack = [v]
        stop=False
        while len(stack) > 0 and not stop:  # bfs what they can reach
            current_vertex = stack.pop(0)
            E = current_vertex.incidence
            for e in E:
                if e.tail == current_vertex:
                    if e.head==v:
                        stop=True
                    elif e.head not in reachable and e.head.label<v.label:
                        stack.append(e.head)
                        reachable.add(e.head)
                if stop:
                    break
        if stop:
            if bestval==-1:
                bestval=v.label
                bestvertex=v
            elif stratplayer==True and bestval*pow(-1, bestval)>v.label*pow(-1,v.label):
                bestval=v.label
                bestvertex=v
            elif stratplayer == False and bestval * pow(-1, bestval) < v.label * pow(-1, v.label):
                bestval = v.label
                bestvertex = v
    return bestval, bestvertex

def set_lambdas(decomp, reachablelists, stratplayer):
    #set the first component of the valuation for the nodes in the graph
    #decomp: decomposition into strongly connected components
    #reachablelists: list of which components can reach which components
    #stratplayer: player other than the one currently trying to find a valuation for
    lambdalist=[]
    lambdadict={}
    for i in range(len(decomp)): #find lambdas for each connected component
        H,I=induced_subgraph(decomp[i])
        bestval, bestvertex=find_lambda(H, stratplayer)
        lambdalist.append(bestval)
    for i in range(len(decomp)): #see what the best component is that component i can reach
        bestnum=lambdalist[i]
        for j in reachablelists[i]:
            if bestnum==-1 and lambdalist[j]!=-1:
                lambdalist[i] = lambdalist[j]
                bestnum = lambdalist[j]
            elif stratplayer and lambdalist[j]!=-1 and pow(-1, lambdalist[j])*lambdalist[j] < pow(-1,bestnum)*bestnum:
                lambdalist[i]=lambdalist[j]
                bestnum=lambdalist[j]
            elif (not stratplayer) and lambdalist[j]!=-1 and pow(-1, lambdalist[j])*lambdalist[j] > pow(-1,bestnum)*bestnum:
                lambdalist[i]=lambdalist[j]
                bestnum=lambdalist[j]
    for i in range(len(decomp)):
        for v in decomp[i]:
            v.set_lambda(stratplayer, lambdalist[i]) #stratplayer is the one doing the counterstrategy
    for l in lambdalist:
        for v in HH.vertices:
            if v.label==l:
                lambdadict[l]=v
    return lambdadict

def induced_subgraph(vertexset):
    #construct induced subgraph based on vertex set
    H=MyGraph(True, 0, False)
    listsz=list(vertexset)
    dictz={listsz[d].index:d for d in range(len(listsz))}
    for d in range(len(listsz)):
        v=Vertex(H,listsz[d].label, listsz[d].player, d)
        H.add_vertex(v)
    for d in range(len(listsz)):
        E=listsz[d].incidence
        for e in E:
            if e.tail==listsz[d] and e.head in vertexset:
                H.add_edge(Edge(H.vertices[d], H.vertices[dictz[e.head.index]]))
    return H,listsz

def set_shortest_paths(G, lambdadict, counterplayer):
    #set shortest paths for the whole graph, per subgraph with the same value of lambda
    #G: graph
    #lambdadict: dictionary of lambdas
    #counterplayer: other player than the one currently trying to find the valuation for
    global Gsp, targetvertex
    for l in lambdadict.keys():
        if counterplayer:
            relevantvertices = {v for v in G.vertices if v.valuation0[0]==l}
        else:
            relevantvertices = {v for v in G.vertices if v.valuation1[0]==l}
        Gsp, listsz = induced_subgraph(relevantvertices)
        for v in Gsp.vertices:
            if v.label==l:
                targetvertex=v
                break
        set_shortest_path(counterplayer)
        for ll in range(len(listsz)):
            if counterplayer:
                listsz[ll].set_path(counterplayer,Gsp.vertices[ll].valuation0[1:3])
            else:
                listsz[ll].set_path(counterplayer, Gsp.vertices[ll].valuation1[1:3])
    return

def set_shortest_path(counterplayer):
    #calculate shortest or longest paths towards the node that dominates the cycle
    #if counterplayer is False(player 0), then find longest paths, else, find shortest paths
    global Gsp, targetvertex
    priorities=[]
    priodict={}
    for e in targetvertex.incidence:
        if targetvertex==e.tail:
            Gsp.remove_edge(e)
    for v in Gsp.vertices:
        if v.label>targetvertex.label:
            priorities.append(v.label)
            priodict[v.label]=v
    priorities.sort()
    priorities=priorities[::-1] #sorted from high to low
    for p in priorities: #priority of r
        if (p%2==0 and counterplayer==True) or (p%2==1 and counterplayer==False):
            W = {targetvertex} #vertices with path to t without r
            stack = [targetvertex]
            while len(stack) > 0:  # bfs what can reach t
                current_vertex = stack.pop(0)
                E = current_vertex.incidence
                for e in E:
                    if e.head== current_vertex:
                        if e.tail not in W and e.tail!=priodict[p]:
                            stack.append(e.tail)
                            W.add(e.tail)
            for ee in Gsp.edges:
                if (ee.tail in W or ee.tail==priodict[p]) and (ee.head not in W):
                    Gsp.remove_edge(ee)
        elif (p%2==1 and counterplayer==True) or (p%2==0 and counterplayer==False):
            U = {priodict[p]}  # vertices with path to r
            stack = [priodict[p]]
            while len(stack) > 0:  # bfs what can reach t
                current_vertex = stack.pop(0)
                E = current_vertex.incidence
                for e in E:
                    if e.head == current_vertex:
                        if e.tail not in U:
                            stack.append(e.tail)
                            U.add(e.tail)
            for ee in Gsp.edges:
                if (ee.tail in U and ee.tail != priodict[p]) and (ee.head not in U):
                    Gsp.remove_edge(ee)
    #preprocessing is done, now find shortest paths to t
    targetvertex.set_path(counterplayer, [[],0])
    #calculate shortest paths by Bellman-Ford
    for i in range(len(Gsp.vertices)):
        for eee in Gsp.edges:
            if counterplayer:
                othervalue = [list(eee.head.valuation0[1]), eee.head.valuation0[2]+0]
            else:
                othervalue = [list(eee.head.valuation1[1]), eee.head.valuation1[2]+0]
            if eee.tail.label>targetvertex.label:
                othervalue[0].append(eee.tail.label)
                othervalue[0].sort()
                othervalue[0]=othervalue[0][::-1]
            othervalue[1]+=1
            if counterplayer:
                if (eee.tail.valuation0[1:3]==[[],-1] or distance_greater(eee.tail.valuation0[1:3],othervalue,targetvertex.label)) and eee.head.valuation0[1:3]!=[[],-1]:
                    eee.tail.set_path(counterplayer, othervalue)
            else:
                if (eee.tail.valuation1[1:3]==[[],-1] or distance_greater(othervalue, eee.tail.valuation1[1:3], targetvertex.label)) and eee.head.valuation1[1:3]!=[[],-1]:
                    eee.tail.set_path(counterplayer, othervalue)
    return

def distance_greater(a,b, lambbda):
    #return whether a is larger than b
    #a,b are pairs of path (sorted from high to low priority) and distance, lambbda is the first component of valuation
    la=len(a[0])
    lb=len(b[0])
    greaterr=False
    for i in range(min(la,lb)):
        if a[0][i]*pow(-1,a[0][i]) > b[0][i]*pow(-1,b[0][i]):
            return True
        elif a[0][i]*pow(-1,a[0][i]) < b[0][i]*pow(-1,b[0][i]):
            return False
    if la>lb and a[0][lb]%2==0:
        return True
    elif la>lb and a[0][lb]%2==1:
        return False
    elif la<lb and b[0][la]%2==1:
        return True
    elif la<lb and b[0][la]%2==0:
        return False
    elif lambbda%2==0 and a[1]<b[1]:
        return True
    elif lambbda%2==1 and b[1]<a[1]:
        return True
    else:
        return False

def valuation_is_greater(val1,val2):
    #returns whether valuation 1 is larger than valuation 2
    if val1[0]*(-1)**val1[0] > val2[0]*(-1)**val2[0]:
        return True
    elif val1[0]*(-1)**val1[0] < val2[0]*(-1)**val2[0]:
        return False
    else:
        return distance_greater(val1[1:3], val2[1:3], val1[0])

def difference_is_greater(v1, v2):
    #format of d1,d2: d1[0]: 2-tuple of two lambdas, d1[1]: dictionary of occurrence per priority. Path lengths: maybe implement later
    v1l0 = v1.valuation0[0]
    v1l1 = v1.valuation1[0]
    v2l0 = v2.valuation0[0]
    v2l1 = v2.valuation1[0]
    if (-2)**v1l1-(-2)**v1l0 > (-2)**v2l1-(-2)**v2l0:
        return True
    elif (-2)**v1l1-(-2)**v1l0 < (-2)**v2l1-(-2)**v2l0:
        return False
    else:
        v1p0 = v1.valuation0[1]
        v1p1 = v1.valuation1[1]
        v2p0 = v2.valuation0[1]
        v2p1 = v2.valuation1[1]
        d1=sorted(v1p1+v2p0)
        d1=d1[::-1]
        d2=sorted(v1p0+v2p1)
        d2=d2[::-1]
        if distance_greater((d1,0), (d2,0),0):
            return True
        elif distance_greater((d2,0), (d1,0),0):
            return False
        else:
            if v1.player == True:
                path1 = v1.valuation1[2]
            else:
                path1 = v1.valuation0[2]
            if v2.player ==True:
                path2 = v2.valuation1[2]
            else:
                path2 = v2.valuation0[2]
            if path1>path2:
                return True
            else:
                return False

def valuation(G, strat, firstplayer):
    #compute valuation for strategy strat and player firstplayer (True=player 1, False=player 0)
    global HH
    HH = makeGsigma(G, strat, firstplayer)
    a, b = decompose_scc(HH)
    c = set_lambdas(a, b, not firstplayer)
    set_shortest_paths(HH, c, not firstplayer)
    if firstplayer:
        for i in range(len(G.vertices)):
            G.vertices[i].set_lambda(False, HH.vertices[i].valuation1[0])
            G.vertices[i].set_path(False, [list(HH.vertices[i].valuation1[1]), HH.vertices[i].valuation1[2]+0])
    else:
        for i in range(len(G.vertices)):
            G.vertices[i].set_lambda(True, HH.vertices[i].valuation0[0])
            G.vertices[i].set_path(True, [list(HH.vertices[i].valuation0[1]), HH.vertices[i].valuation0[2]+0])

def makeGsigma(G,strat,stratplayer):
    #construct subgraph G_sigma
    H=MyGraph(True, 0, False)
    for v in G.vertices:
        vert=Vertex(H, v.label, v.player, v.index)
        H.add_vertex(vert)
    for e in G.edges:
        if e.tail.player==stratplayer:
            if e in strat:
                H.add_edge(Edge(H.vertices[e.tail.index], H.vertices[e.head.index]))
        else:
            H.add_edge(Edge(H.vertices[e.tail.index], H.vertices[e.head.index]))
    return H

def evaluate_distance0(v):
    return v.distance0

def evaluate_distance1(v):
    return v.distance1

#############################Improvement rules####################################################################
def select_edges(G, I0, I1, mode, imp_rule, successors=None):
    #select edges based on an improvement rule from the sets of improving moves.
    select0=set() #this will be filled with the choices for player 0
    select1=set() #choices for player 1
    if mode == 'symmetric':
        if imp_rule == 'symmetric' or imp_rule == None:
            select0,select1 = imp_rule_symmetric(G, I0, I1)
        elif imp_rule == 'generalizedsymmetric':
            select0,select1 = imp_rule_generalized_symmetric(G, I0, I1, successors)
        elif imp_rule == 'othervaluation':
            select0, select1 = imp_rule_other_valuation(G, I0, I1)
        elif imp_rule == 'switchall':
            select0, select1 = imp_rule_switch_all(G, I0, I1)
        elif imp_rule == 'highestpriority' or imp_rule == 'lowestpriority':
            lh_bool = (imp_rule == 'lowestpriority')
            select0, select1 = imp_rule_lowest_highest_priority(G, I0, I1, lh_bool)
        else:
            raise ValueError('"'+imp_rule+'" is not a valid improvement rule for symmetric strategy improvement' )
    elif mode == 'even' or mode == 'odd':
        if imp_rule == 'switchall' or imp_rule == None:
            select0, select1 = imp_rule_switch_all(G, I0, I1)
        elif imp_rule == 'lowestvaluation' or imp_rule == 'highestvaluation':
            lh_bool = (imp_rule == 'lowestvaluation')
            select0, select1 = imp_rule_lowest_highest_valuation(G, I0, I1, mode, lh_bool)
        elif imp_rule == 'highestpriority' or imp_rule == 'lowestpriority':
            lh_bool = (imp_rule == 'lowestpriority')
            select0, select1 = imp_rule_lowest_highest_priority(G, I0, I1, lh_bool)
        else:
            raise ValueError('"' + imp_rule + '" is not a valid improvement rule for strategy improvement')
    else:
        raise ValueError('"' + mode +'" is not a valid mode')
    return select0,select1

def imp_rule_symmetric(G,I0,I1):
    select0=set()
    select1=set()
    for e in I0:
        if e.head.valuation1[0] == e.tail.valuation1[0]:
            if e.tail.label == e.head.valuation1[0] and e.head.valuation1[1] == []:
                select0.add(e) #if the edge is part of cycle determining valuation
            else:
                if e.tail.label > e.head.valuation1[0]:
                    othervalue = [list(e.head.valuation1[1]), e.head.valuation1[2] + 1]
                    othervalue[0].append(e.tail.label)
                    othervalue[0].sort()
                    othervalue[0] = othervalue[0][::-1]
                else:
                    othervalue = [list(e.head.valuation1[1]), e.head.valuation1[2] + 1]
                if othervalue == e.tail.valuation1[1:3]:
                    select0.add(e)  # if target is best among successors, it can be optimal
    for e in I1:
        if e.head.valuation0[0] == e.tail.valuation0[0]:
            if e.tail.label == e.head.valuation0[0] and e.head.valuation0[1] == []:
                select1.add(e)
            else:
                if e.tail.label > e.head.valuation0[0]:
                    othervalue = [list(e.head.valuation0[1]), e.head.valuation0[2] + 1]
                    othervalue[0].append(e.tail.label)
                    othervalue[0].sort()
                    othervalue[0] = othervalue[0][::-1]
                else:
                    othervalue = [list(e.head.valuation0[1]), e.head.valuation0[2] + 1]
                if othervalue == e.tail.valuation0[1:3]:
                    select1.add(e)  # if in optimal and improving
    # remove extra edges
    for v in G.vertices:
        if v.player == False:
            g1 = {e for e in v.incidence if e.tail == v}
            if len(g1.intersection(select0)) > 1:
                g = list(g1.intersection(select0))
                for i in range(1, len(g)):
                    select0.remove(g[i])
        else:
            g1 = {e for e in v.incidence if e.tail == v}
            if len(g1.intersection(select1)) > 1:
                g = list(g1.intersection(select1))
                for i in range(1, len(g)):
                    select1.remove(g[i])
    return select0, select1

def imp_rule_generalized_symmetric(G,I0,I1, successors):
    #SWITCH-ALL for generalized symmetric strategy improvement
    select0 = set()
    select1 = set()
    for e in I0:
        l1 = e.head.valuation1[0]
        l2 = successors[e.tail].valuation1[0]
        if l1 == l2:
            if distance_greater(e.head.valuation1[1:3], successors[e.tail].valuation1[1:3], e.head.valuation1[0]):
                select0.add(e)
        elif (-1) ** l1 * l1 > (-1) ** l2 * l2:
            select0.add(e)
    for e in I1:
        l1 = e.head.valuation0[0]
        l2 = successors[e.tail].valuation0[0]
        if l1 == l2:
            if distance_greater(successors[e.tail].valuation0[1:3], e.head.valuation0[1:3], e.head.valuation1[0]):
                select1.add(e)
        elif (-1) ** l1 * l1 < (-1) ** l2 * l2:
            select1.add(e)
    # remove extra edges
    for v in G.vertices:
        if v.player == False:
            g1 = {e for e in v.incidence if e.tail == v}
            if len(g1.intersection(select0)) > 1:
                g = list(g1.intersection(select0))
                for i in range(1, len(g)):
                    select0.remove(g[i])
        else:
            g1 = {e for e in v.incidence if e.tail == v}
            if len(g1.intersection(select1)) > 1:
                g = list(g1.intersection(select1))
                for i in range(1, len(g)):
                    select1.remove(g[i])
    return select0, select1

def imp_rule_other_valuation(G,I0,I1):
    #select a successor with the highest valuation of the other player's strategy. Can be seen as
    # an even more relaxed version of generalized symmetric strategy improvement
    select0 = set()
    select1 = set()
    imprvertices = set()
    currbestimprovement = {}
    for e in I0:
        if e.tail not in imprvertices:
            imprvertices.add(e.tail)
            select0.add(e)
            currbestimprovement[e.tail] = e
        else:
            l1 = e.head.valuation1[0]
            l2 = currbestimprovement[e.tail].head.valuation1[0]
            if l1 == l2:
                if distance_greater(e.head.valuation1[1:3], currbestimprovement[e.tail].head.valuation1[1:3],
                                    e.head.valuation1[0]):
                    select0.remove(currbestimprovement[e.tail])
                    select0.add(e)
                    currbestimprovement[e.tail] = e
            elif (-1) ** l1 * l1 > (-1) ** l2 * l2:
                select0.remove(currbestimprovement[e.tail])
                select0.add(e)
                currbestimprovement[e.tail] = e
    for e in I1:
        if e.tail not in imprvertices:
            imprvertices.add(e.tail)
            select1.add(e)
            currbestimprovement[e.tail] = e
        else:
            l1 = e.head.valuation0[0]
            l2 = currbestimprovement[e.tail].head.valuation0[0]
            if l1 == l2:
                if distance_greater(currbestimprovement[e.tail].head.valuation0[1:3], e.head.valuation0[1:3],
                                    e.head.valuation0[0]):
                    select1.remove(currbestimprovement[e.tail])
                    select1.add(e)
                    currbestimprovement[e.tail] = e
            elif (-1) ** l1 * l1 < (-1) ** l2 * l2:
                select1.remove(currbestimprovement[e.tail])
                select1.add(e)
                currbestimprovement[e.tail] = e
    return select0, select1

def imp_rule_switch_all(G, I0, I1):
    #switch-all rule, select a successor with the highest valuation, from every node where there is one.
    select0 = set()
    select1 = set()
    imprvertices = set()
    currbestimprovement = {}
    for e in I0:
        if e.tail not in imprvertices:
            imprvertices.add(e.tail)
            select0.add(e)
            currbestimprovement[e.tail] = e
        else:
            l1 = e.head.valuation0[0]
            l2 = currbestimprovement[e.tail].head.valuation0[0]
            if l1 == l2:
                if distance_greater(e.head.valuation0[1:3], currbestimprovement[e.tail].head.valuation0[1:3],
                                    e.head.valuation0[0]):
                    select0.remove(currbestimprovement[e.tail])
                    select0.add(e)
                    currbestimprovement[e.tail] = e
            elif (-1) ** l1 * l1 > (-1) ** l2 * l2:
                select0.remove(currbestimprovement[e.tail])
                select0.add(e)
                currbestimprovement[e.tail] = e
    for e in I1:
        if e.tail not in imprvertices:
            imprvertices.add(e.tail)
            select1.add(e)
            currbestimprovement[e.tail] = e
        else:
            l1 = e.head.valuation1[0]
            l2 = currbestimprovement[e.tail].head.valuation1[0]
            if l1 == l2:
                if distance_greater(currbestimprovement[e.tail].head.valuation1[1:3], e.head.valuation1[1:3],
                                    e.head.valuation1[0]):
                    select1.remove(currbestimprovement[e.tail])
                    select1.add(e)
                    currbestimprovement[e.tail] = e
            elif (-1) ** l1 * l1 < (-1) ** l2 * l2:
                select1.remove(currbestimprovement[e.tail])
                select1.add(e)
                currbestimprovement[e.tail] = e
    return select0, select1

def imp_rule_lowest_highest_valuation(G, I0, I1, mode, lh_bool):
    #prefers switches at the nodes with the lowest valuation if lh_bool = True, and highest if lh_bool=false
    vertexorder = [v for v in G.vertices]
    vl = len(vertexorder)
    for ii in range(vl):  # bubblesort
        for jj in range(vl - 1):
            if mode == 'odd':
                greater_bool = valuation_is_greater(vertexorder[jj].valuation1, vertexorder[jj + 1].valuation1)
            else:
                greater_bool = valuation_is_greater(vertexorder[jj].valuation0, vertexorder[jj + 1].valuation0)
            if greater_bool:
                vertexorder[jj:jj + 2] = [vertexorder[jj + 1], vertexorder[jj]]
    if not lh_bool:
        vertexorder = vertexorder[::-1]
    for v in vertexorder:
        for e in v.incidence:
            if e.tail == v:
                if e in I0:
                    select0={e}
                    select1=set()
                    if e.tail.label==23:
                        pass
                    return select0, select1
                elif e in I1:
                    select0=set()
                    select1={e}
                    return select0, select1
    return set(), set()

def imp_rule_lowest_highest_priority(G, I0, I1, lh_bool):
    #prefer switching at nodes with lowest priority if lh_bool = True, and with highest priority if lh_bool=False
    vertexorder = [v for v in G.vertices]
    vl = len(vertexorder)
    for ii in range(vl):  # bubblesort
        for jj in range(vl - 1):
            greater_bool = (vertexorder[jj].label > vertexorder[jj+1].label)
            if greater_bool:
                vertexorder[jj:jj + 2] = [vertexorder[jj + 1], vertexorder[jj]]
    if not lh_bool:
        vertexorder = vertexorder[::-1]
    for v in vertexorder:
        for e in v.incidence:
            if e.tail == v:
                if e in I0:
                    select0 = {e}
                    select1 = set()
                    return select0, select1
                elif e in I1:
                    select0 = set()
                    select1 = {e}
                    return select0, select1
    return set(), set()

def run_strategy_iteration_with_counterexample(n=3, mode='symmetric', imp_rule=None,
                                               counterexample='symmetric', render=True, print_iterations=False,
                                               check_strategy = True):
    #Run a version of (symmetric) strategy iteration on a counterexample parity game G_n.
    # Assumes valuation from Jurdzinksi and Vöge.
    #Inputs:
    #n: index of the graph G_n
    #mode: Version of strategy iteration:
    #      mode = 'even' - strategy iteration for player 0/player even
    #      mode = 'odd' - strategy iteration for player 1/player odd
    #      mode = 'symmetric' - symmetric strategy iteration/ improve both player's strategies
    #imp_rule: selects improvement rule
    #counterexample: select which class to take the counterexample from
    #render: if set to True, render a GIF animation, which is saved as animation.Example animations.
    #         Additionally, every frame is saved as picture and as gv file in the png/gv folder
    #print_iterations: if set to True, output the strategies in every iteration
    #check_strategy: if set to True, check if strategies are valid in the counterexample
    #
    #Outputs:
    #G: the graph. one could find the values of nodes in the
    #     v.valuation0 or v.valuation1 attribute for vertices v of G
    #     (depending on type of strategy iteration)
    #strat0, strat1: player 0 resp. player 1 optimal strategies
    global G
    if counterexample == 'symmetric':
        G, init0, init1, s = create_phicounter(n)
    elif counterexample == 'generalizedsymmetric':
        G, init0, init1, s = create_casual_phicounter(n)
    elif counterexample == 'lessgeneralizedsymmetric':
        G, init0, init1, s = create_relaxed_phicounter(n)
    elif counterexample == 'switchbest':
        G, init0, init1, s = create_switchbest_counter(n)
    elif counterexample == 'highestvaluation':
        G, init0, init1, s = create_highest_valuation_counter(n)
    elif counterexample == 'lowestvaluation':
        G, init0, init1, s = create_lowest_valuation_counter(n)
    else:
        raise ValueError("Counterexample "+counterexample+" is unknown")

    if check_strategy:
        stratcorrect = True
        for v in G.vertices:
            p0count = 0
            p1count = 0
            for e in v.incidence:
                if e.tail == v:
                    if e in init0:
                        p0count +=1
                    if e in init1:
                        p1count +=1
            if (v.player == True and p0count > 0) or (v.player == False and p1count>0):
                print('Node ', v, 'has edges from the wrong player in the initial strategy')
                stratcorrect = False
            elif (v.player == True and p1count != 1) or (v.player == False and p0count != 1):
                if v.player:
                    aa = p1count
                else:
                    aa = p0count
                print('Node', v,'has', aa,'outgoing edges in the initial strategy')
                stratcorrect = False
        if not stratcorrect:
            raise ValueError("Invalid strategy")


    for i in range(len(G.vertices)):  # fix indices
        G.vertices[i].index = i
    impr0 = set()
    impr1 = set()
    strat0 = init0
    strat1 = init1
    startt = True
    iters = 0
    if render: #empty the folder with frames of animation
        for picpath in ['gv', 'png']:
            if os.path.exists(picpath):
                filelist = os.listdir(picpath)
                for filez in filelist:
                    os.remove(picpath + '\\' + filez)
            else:
                os.mkdir(picpath)
    progress = tqdm(desc="Running (symmetric) strategy iteration...",leave=False)
    while startt or len(impr0)>0 or len(impr1)>0: #main loop of (symmetric) strategy improvement
        progress.update()
        startt=False
        iters+=1
        if render:
            #render new image
            G.label = "Iteration "+str(iters-1)
            with open('gv/pic'+str(iters-1)+'.gv', 'w') as filez:
                write_dot(G, filez, True)
            #reset colors of newly switched edges
            for e in strat0:
                e._in_strategy = 1
            for e in strat1:
                e._in_strategy = 1
        #update strategies
        for v in G.vertices:
            for e in v.incidence:
                if e.tail==v and v.player==False and e in impr0:
                    for ee in v.incidence:
                        if ee.tail==v and ee in strat0:
                            strat0.remove(ee)
                            strat0.add(e)
                            ee._in_strategy = 0
                            e._in_strategy = 2
                            break
                elif e.tail == v and v.player == True and e in impr1:
                    for ee in v.incidence:
                        if ee.tail==v and ee in strat1:
                            strat1.remove(ee)
                            strat1.add(e)
                            ee._in_strategy = 0
                            e._in_strategy = 2
                            break
        #update valuations
        if mode == 'symmetric' or mode == 'even':
            valuation(G, strat0, False)
        if mode == 'symmetric' or mode == 'odd':
            valuation(G, strat1, True)
        successors = {}
        for e in strat0:
            successors[e.tail] = e.head
        for e in strat1:
            successors[e.tail] = e.head
        if print_iterations:
            print('Iteration', iters)
            if mode == 'symmetric' or mode == 'even':
                print('Even player\'s strategy: ', {(ey.tail.label,ey.head.label) for ey in strat0})
            if mode == 'symmetric' or mode == 'odd':
                print('Odd player\'s strategy:', {(ey.tail.label,ey.head.label) for ey in strat1})
        impr0 = set()
        impr1 = set()
        for e in G.edges: #check for every edge if it is an improving move
            if e.tail.player==False and (mode == 'symmetric' or mode == 'even'): #player 0 controlled node at tail
                if e not in strat0:
                    h=e.head.valuation0[0]
                    t=e.tail.valuation0[0]
                    if t*pow(-1,t)<h*pow(-1,h):
                        impr0.add(e)
                    elif t==h:
                        if e.tail.label>t:
                            othervalue=[list(e.head.valuation0[1]), e.head.valuation0[2] + 1]
                            othervalue[0].append(e.tail.label)
                            othervalue[0].sort()
                            othervalue[0] = othervalue[0][::-1]
                        else:
                            othervalue = [list(e.head.valuation0[1]), e.head.valuation0[2] + 1]
                        if distance_greater(othervalue, e.tail.valuation0[1:3],t):
                            impr0.add(e)
            elif e.tail.player==True and (mode == 'symmetric' or mode == 'odd'): #player 1 controlled node at the tail.
                if e not in strat1:
                    h=e.head.valuation1[0]
                    t=e.tail.valuation1[0]
                    if t*pow(-1,t)>h*pow(-1,h):
                        impr1.add(e)
                    elif t==h:
                        if e.tail.label>t:
                            othervalue=[list(e.head.valuation1[1]), e.head.valuation1[2] + 1]
                            othervalue[0].append(e.tail.label)
                            othervalue[0].sort()
                            othervalue[0] = othervalue[0][::-1]
                        else:
                            othervalue = [list(e.head.valuation1[1]), e.head.valuation1[2] + 1]
                        if distance_greater(e.tail.valuation1[1:3], othervalue,t):
                            impr1.add(e)
        impr0, impr1 = select_edges(G, impr0,impr1, mode, imp_rule, successors)
        G.label = "Iteration " + str(iters)
    if render:
        for i in range(5): #add 5 extra frames with optimal solution
            with open('gv/pic' + str(iters+i) + '.gv', 'w') as filez:
                write_dot(G, filez, True)
            # reset colors of newly switched edges
            for e in strat0:
                e._in_strategy = 1
            for e in strat1:
                e._in_strategy = 1
        scalefactor = len(G.vertices) / s
        images = []
        for ii in tqdm(range(iters + 5), desc="Rendering animation...", position=0, leave=True):
            src2 = Source.from_file('gv\\pic' + str(ii) + '.gv')
            g = Digraph()
            source_lines = str(src2).splitlines()
            source_lines.pop(0)
            source_lines.pop(-1)
            g.body += source_lines
            g.graph_attr['splines'] = 'true'
            g.graph_attr['sep'] = '1'
            g.graph_attr['scale'] = str(scalefactor)
            g.render('png\\pic' + str(ii) + '.gv', format='png', cleanup=True, quiet=True, engine="neato", view=False).replace('\\',                                                                                                   '/')
            images.append(imageio.imread('png\\pic' + str(ii) + '.gv.png'))
        print('Saving animation as GIF (this should take about half as long as the rendering)...')
        imageio.mimsave('animation.gif', images, duration=1)
    print('(symmetric) strategy improvement finished in', iters, ' iterations.')
    return G, strat0, strat1




