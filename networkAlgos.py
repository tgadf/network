from networkx import algorithms as algos
from networkx import linalg
from networkx import convert_matrix
from pandas import DataFrame


def runAlgos(algosToRun, g):
    from types import GeneratorType
    results = {}
    for algo in algosToRun:
        name = algo.__name__

        try:
            results[name] = algo(g)
        except:
            results[name] = None

        if isinstance(results[name], GeneratorType):
            results[name] = len([1 for _ in results[name]])
            try:
                results[name] = len([1 for _ in algo])
            except:
                pass
            
    return results


def getHeuristics():
    algosToRun = []
    #algosToRun.append(algos.all_pairs_node_connectivity)  # not needed
    algosToRun.append(algos.node_connectivity)
    #algosToRun.append(algos.k_components)
    algosToRun.append(algos.average_clustering)
    return algosToRun

def getAssortativity():
    algosToRun = []
    algosToRun.append(algos.degree_assortativity_coefficient)
    algosToRun.append(algos.degree_pearson_correlation_coefficient)
    algosToRun.append(algos.average_neighbor_degree)
    #algosToRun.append(algos.average_degree_connectivity)
    algosToRun.append(algos.k_nearest_neighbors)
    #algosToRun.append(algos.degree_mixing_matrix)
    #algosToRun.append(algos.degree_mixing_dict)
    return algosToRun

def getBipartite():
    algosToRun = []
    algosToRun.append(algos.is_bipartite)
    #algosToRun.append(algos.bipartite.sets)
    return algosToRun

def getBridges():
    algosToRun = []
    algosToRun.append(algos.bridges)
    algosToRun.append(algos.has_bridges)    
    return algosToRun

def getCentrality():
    algosToRun = []
    algosToRun.append(algos.degree_centrality)
    algosToRun.append(algos.in_degree_centrality)
    algosToRun.append(algos.out_degree_centrality)
    algosToRun.append(algos.eigenvector_centrality)
    algosToRun.append(algos.eigenvector_centrality_numpy)
    algosToRun.append(algos.katz_centrality)
    algosToRun.append(algos.katz_centrality_numpy)
    algosToRun.append(algos.closeness_centrality)
    algosToRun.append(algos.current_flow_closeness_centrality)
    algosToRun.append(algos.information_centrality)
    algosToRun.append(algos.betweenness_centrality)
    algosToRun.append(algos.edge_betweenness_centrality)
    #algosToRun.append(algos.betweenness_centrality_subset)
    #algosToRun.append(algos.edge_betweenness_centrality_subset)
    algosToRun.append(algos.current_flow_betweenness_centrality)
    #algosToRun.append(algos.edge_current_flow_betweenness_centrality)
    algosToRun.append(algos.approximate_current_flow_betweenness_centrality)
    #algosToRun.append(algos.current_flow_betweenness_centrality_subset)
    #algosToRun.append(algos.edge_current_flow_betweenness_centrality_subset)
    algosToRun.append(algos.communicability_betweenness_centrality)
    algosToRun.append(algos.load_centrality)
    #algosToRun.append(algos.edge_load_centrality) # not needed
    algosToRun.append(algos.subgraph_centrality)
    algosToRun.append(algos.subgraph_centrality_exp)
    algosToRun.append(algos.estrada_index)
    algosToRun.append(algos.harmonic_centrality)
    algosToRun.append(algos.local_reaching_centrality)
    algosToRun.append(algos.global_reaching_centrality)
    algosToRun.append(algos.percolation_centrality)
    algosToRun.append(algos.second_order_centrality)
    return algosToRun

def getChains():
    algosToRun = []
    algosToRun.append(algos.chain_decomposition)
    return algosToRun

def getChordal():
    algosToRun = []
    algosToRun.append(algos.is_chordal)
    algosToRun.append(algos.chordal_graph_cliques)
    algosToRun.append(algos.chordal_graph_treewidth)
    algosToRun.append(algos.find_induced_nodes)
    return algosToRun

def getCliques():
    algosToRun = []
    algosToRun.append(algos.enumerate_all_cliques)
    algosToRun.append(algos.find_cliques)
    #algosToRun.append(algos.make_max_clique_graph)
    #algosToRun.append(algos.make_clique_bipartite)
    algosToRun.append(algos.graph_clique_number)
    algosToRun.append(algos.graph_number_of_cliques)
    algosToRun.append(algos.node_clique_number)
    algosToRun.append(algos.number_of_cliques)
    algosToRun.append(algos.cliques_containing_node)
    return algosToRun

def getClustering():
    algosToRun = []
    algosToRun.append(algos.triangles)
    algosToRun.append(algos.transitivity)
    algosToRun.append(algos.clustering)
    algosToRun.append(algos.average_clustering)
    algosToRun.append(algos.square_clustering)
    algosToRun.append(algos.generalized_degree)
    return algosToRun

def getCommunicability():
    algosToRun = []
    algosToRun.append(algos.communicability)
    return algosToRun

def getCommunities():
    algosToRun = []
    #algosToRun.append(algos.community.kernighan_lin_bisection) # Not sure what to do with it
    algosToRun.append(algos.community.k_clique_communities)
    #algosToRun.append(algos.community.greedy_modularity_communities) # Not sure what to do with it
    #algosToRun.append(algos.community.asyn_lpa_communities) ?
    algosToRun.append(algos.community.label_propagation_communities)
    algosToRun.append(algos.community.asyn_fluidc)
    algosToRun.append(algos.community.girvan_newman)
    return algosToRun
    
def getConnected():
    algosToRun = []
    algosToRun.append(algos.is_connected)
    algosToRun.append(algos.number_connected_components)
    algosToRun.append(algos.is_strongly_connected)
    algosToRun.append(algos.number_strongly_connected_components)
    algosToRun.append(algos.is_weakly_connected)
    algosToRun.append(algos.number_weakly_connected_components)
    algosToRun.append(algos.is_attracting_component)
    algosToRun.append(algos.number_attracting_components)
    algosToRun.append(algos.is_biconnected)
    algosToRun.append(algos.articulation_points)
    algosToRun.append(algos.is_semiconnected)
    return algosToRun

def getCore():
    algosToRun = []
    algosToRun.append(algos.core_number)
    algosToRun.append(algos.k_core)
    algosToRun.append(algos.k_shell)
    algosToRun.append(algos.k_crust)
    algosToRun.append(algos.k_corona)
    return algosToRun

def getCover():
    algosToRun = []
    algosToRun.append(algos.min_edge_cover)
    algosToRun.append(algos.is_edge_cover)
    return algosToRun

def getCycles():
    algosToRun = []
    algosToRun.append(algos.cycle_basis)
    algosToRun.append(algos.simple_cycles)
    algosToRun.append(algos.find_cycle)
    algosToRun.append(algos.minimum_cycle_basis)
    return algosToRun

def getDAG():
    algosToRun = []
    #algosToRun.append(algos.topological_sort)
    #algosToRun.append(algos.all_topological_sorts)
    #algosToRun.append(algos.lexicographical_topological_sort)
    algosToRun.append(algos.is_directed_acyclic_graph)
    algosToRun.append(algos.is_aperiodic)
    algosToRun.append(algos.transitive_closure)
    algosToRun.append(algos.transitive_reduction)
    algosToRun.append(algos.antichains)
    algosToRun.append(algos.dag_longest_path)
    algosToRun.append(algos.dag_longest_path_length)
    algosToRun.append(algos.dag_to_branching)
    return algosToRun

def getDistance():
    algosToRun = []
    algosToRun.append(algos.center)
    algosToRun.append(algos.diameter)
    algosToRun.append(algos.eccentricity)
    algosToRun.append(algos.extrema_bounding)
    algosToRun.append(algos.periphery)
    algosToRun.append(algos.radius)
    return algosToRun

def getIntersection():
    algosToRun = []
    algosToRun.append(algos.is_distance_regular)
    algosToRun.append(algos.is_strongly_regular)
    algosToRun.append(algos.intersection_array)
    return algosToRun

def getDominating():
    algosToRun = []
    algosToRun.append(algos.dominating_set)
    return algosToRun

def getEfficiency():
    algosToRun = []
    algosToRun.append(algos.local_efficiency)
    algosToRun.append(algos.global_efficiency)
    return algosToRun

def getEulerian():
    algosToRun = []
    algosToRun.append(algos.is_eulerian)
    return algosToRun

def getFlow():
    algosToRun = []
    algosToRun.append(algos.maximum_flow)
    algosToRun.append(algos.maximum_flow_value)
    #algosToRun.append(algos.edmonds_karp)
    #algosToRun.append(algos.shortest_augmenting_path)
    #algosToRun.append(algos.preflow_push)
    #algosToRun.append(algos.dinitz)
    #algosToRun.append(algos.boykov_kolmogorov)
    algosToRun.append(algos.gomory_hu_tree)
    #algosToRun.append(algos.build_residual_network)
    algosToRun.append(algos.network_simplex)
    algosToRun.append(algos.min_cost_flow_cost)
    algosToRun.append(algos.min_cost_flow)
    algosToRun.append(algos.cost_of_flow)
    algosToRun.append(algos.capacity_scaling)
    return algosToRun

def getHierachy():
    algosToRun = []
    algosToRun.append(algos.flow_hierarchy)
    return algosToRun

def getIsolates():
    algosToRun = []
    algosToRun.append(algos.isolates)
    algosToRun.append(algos.number_of_isolates)
    return algosToRun

def getLinkAnalysis():
    algosToRun = []
    algosToRun.append(algos.pagerank)
    #algosToRun.append(algos.google_matrix) # Underlying transition matrix for page rank
    algosToRun.append(algos.hits)
    #algosToRun.append(algos.hub_matrix) # Underlying matrix for Hub (in HITS)
    #algosToRun.append(algos.authority_matrix) # Underlying matrix for Authority (in HITS)
    return algosToRun

def getLinkPrediction():
    algosToRun = []
    algosToRun.append(algos.resource_allocation_index)
    algosToRun.append(algos.jaccard_coefficient)
    algosToRun.append(algos.adamic_adar_index)
    algosToRun.append(algos.preferential_attachment)
    #algosToRun.append(algos.cn_soundarajan_hopcroft)
    #algosToRun.append(algos.ra_index_soundarajan_hopcroft)
    #algosToRun.append(algos.within_inter_cluster)
    return algosToRun    

def getLowestCommonAncester():
    algosToRun = []
    algosToRun.append(algos.all_pairs_lowest_common_ancestor)
    algosToRun.append(algos.tree_all_pairs_lowest_common_ancestor)
    algosToRun.append(algos.lowest_common_ancestor)
    return algosToRun

def getMatching():
    algosToRun = []
    algosToRun.append(algos.maximal_matching)
    algosToRun.append(algos.max_weight_matching)
    return algosToRun

def getMIS():
    algosToRun = []
    algosToRun.append(algos.maximal_independent_set)
    return algosToRun

def getReciprocity():
    algosToRun = []
    algosToRun.append(algos.reciprocity)
    algosToRun.append(algos.overall_reciprocity)
    return algosToRun

def getRichClub():
    algosToRun = []
    algosToRun.append(algos.rich_club_coefficient)
    return algosToRun

def getShortestPath():
    algosToRun = []
    algosToRun.append(algos.shortest_path)
    algosToRun.append(algos.all_shortest_paths)
    algosToRun.append(algos.shortest_path_length)
    algosToRun.append(algos.average_shortest_path_length)
    return algosToRun

def getSMetric():
    algosToRun = []
    algosToRun.append(algos.s_metric)
    return algosToRun

def getStructural():
    algosToRun = []
    algosToRun.append(algos.constraint)
    algosToRun.append(algos.effective_size)
    return algosToRun

def getTree():
    algosToRun = []
    algosToRun.append(algos.is_tree)
    algosToRun.append(algos.is_forest)
    algosToRun.append(algos.is_arborescence)
    algosToRun.append(algos.is_branching)
    #algosToRun.append(algos.branching_weight)
    #algosToRun.append(algos.greedy_branching)
    ## Return graphs
    #algosToRun.append(algos.maximum_branching)
    #algosToRun.append(algos.minimum_branching)
    #algosToRun.append(algos.maximum_spanning_arborescence)
    #algosToRun.append(algos.minimum_spanning_arborescence)
    #algosToRun.append(algos.Edmonds)
    return algosToRun

def getTriadic():
    algosToRun = []
    algosToRun.append(algos.triadic_census)
    return algosToRun

def getVitality():
    algosToRun = []
    algosToRun.append(algos.closeness_vitality)
    return algosToRun

def getWiener():
    algosToRun = []
    algosToRun.append(algos.wiener_index)
    return algosToRun

def getSpectrum():
    algosToRun = []
    algosToRun.append(linalg.laplacian_spectrum)
    algosToRun.append(linalg.adjacency_spectrum)
    algosToRun.append(linalg.modularity_spectrum)
    algosToRun.append(linalg.algebraic_connectivity)
    #algosToRun.append(linalg.fiedler_vector) ?
    algosToRun.append(linalg.spectral_ordering)
    return algosToRun

def runNetworkAlgorithms(g):
    algosToRun  = []
    algosToRun += getHeuristics()
    algosToRun += getAssortativity()
    algosToRun += getBipartite()
    algosToRun += getBridges()
    algosToRun += getCentrality()
    algosToRun += getChains()
    algosToRun += getChordal()
    algosToRun += getCliques()
    algosToRun += getClustering()
    algosToRun += getCommunicability()
    algosToRun += getCommunities()
    algosToRun += getConnected()
    algosToRun += getCore()
    algosToRun += getCover()
    algosToRun += getCycles()
    algosToRun += getDAG()
    algosToRun += getDistance()
    algosToRun += getIntersection()
    algosToRun += getDominating()
    algosToRun += getEfficiency()
    algosToRun += getEulerian()
    algosToRun += getFlow()
    algosToRun += getHierachy()
    algosToRun += getIsolates()
    algosToRun += getLinkAnalysis()
    algosToRun += getLinkPrediction()
    algosToRun += getLowestCommonAncester()
    algosToRun += getMatching()
    algosToRun += getMIS()
    algosToRun += getReciprocity()
    algosToRun += getRichClub()
    algosToRun += getShortestPath()
    algosToRun += getSMetric()
    algosToRun += getStructural()
    algosToRun += getTree()
    algosToRun += getTriadic()
    algosToRun += getVitality()
    algosToRun += getWiener()
    algosToRun += getSpectrum()
    
    
    noneAlgos = ["in_degree_centrality", "out_degree_centrality", "katz_centrality", "betweenness_centrality_subset", "edge_betweenness_centrality_subset", "current_flow_betweenness_centrality_subset", "edge_current_flow_betweenness_centrality_subset", "local_reaching_centrality", "percolation_centrality", "is_chordal", "chordal_graph_cliques", "chordal_graph_treewidth", "find_induced_nodes", "k_clique_communities", "asyn_fluidc", "is_strongly_connected", "number_strongly_connected_components", "is_weakly_connected", "number_weakly_connected_components", "is_attracting_component", "number_attracting_components", "is_semiconnected", "core_number", "k_core", "k_shell", "k_crust", "k_corona", "is_edge_cover", "simple_cycles", "is_aperiodic", "transitive_closure", "transitive_reduction", "antichains", "dag_longest_path", "dag_longest_path_length", "dag_to_branching", "intersection_array", "maximum_flow", "maximum_flow_value", "gomory_hu_tree", "network_simplex", "min_cost_flow_cost", "min_cost_flow", "cost_of_flow", "capacity_scaling", "flow_hierarchy", "all_pairs_lowest_common_ancestor", "tree_all_pairs_lowest_common_ancestor", "lowest_common_ancestor", "rich_club_coefficient", "all_shortest_paths", "s_metric", "is_arborescence", "is_branching", "triadic_census"]
    netAlgos  = ["node_connectivity", "k_components", "average_clustering", "degree_assortativity_coefficient", "degree_pearson_correlation_coefficient", "is_bipartite", "bridges", "has_bridges", "estrada_index", "global_reaching_centrality", "chain_decomposition", "enumerate_all_cliques", "find_cliques", "graph_clique_number", "graph_number_of_cliques", "transitivity", "kernighan_lin_bisection", "greedy_modularity_communities", "label_propagation_communities", "girvan_newman", "is_connected", "number_connected_components", "is_biconnected", "articulation_points", "min_edge_cover", "is_directed_acyclic_graph", "diameter", "extrema_bounding", "radius", "is_distance_regular", "is_strongly_regular", "local_efficiency", "global_efficiency", "is_eulerian", "isolates", "number_of_isolates", "resource_allocation_index", "jaccard_coefficient", "adamic_adar_index", "preferential_attachment", "reciprocity", "overall_reciprocity", "shortest_path_length", "average_shortest_path_length", "is_tree", "is_forest", "wiener_index", "laplacian_spectrum", "adjacency_spectrum", "modularity_spectrum", "algebraic_connectivity"]
    nodeAlgos = ["average_neighbor_degree", "degree_centrality", "eigenvector_centrality", "eigenvector_centrality_numpy", "katz_centrality_numpy", "closeness_centrality", "current_flow_closeness_centrality", "betweenness_centrality", "current_flow_betweenness_centrality", "approximate_current_flow_betweenness_centrality", "communicability_betweenness_centrality", "newman_betweenness_centrality", "subgraph_centrality", "subgraph_centrality_exp", "harmonic_centrality", "second_order_centrality", "node_clique_number", "number_of_cliques", "cliques_containing_node", "triangles", "clustering", "square_clustering", "generalized_degree", "communicability", "cycle_basis", "find_cycle", "minimum_cycle_basis", "center", "eccentricity", "periphery", "dominating_set", "pagerank", "maximal_matching", "max_weight_matching", "maximal_independent_set", "shortest_path", "constraint", "effective_size", "closeness_vitality", "spectral_ordering", "hub_score", "authority_score"]
    edgeAlgos = ["edge_betweenness_centrality", "edge_current_flow_betweenness_centrality"]
    
    
    results = {"Net": {}, "Nodes": {}, "Edges": {}}
    retval = runAlgos(algosToRun, g)
    for k in list(retval.keys()):
        v = retval[k]
        if isinstance(v, float):
            v = float(v)
        if isinstance(v, int):
            v = int(v)
        #if v is None:
        #    continue
            
        if not isinstance(v, dict):
            if k in ['cycle_basis', 'minimum_cycle_basis', 'find_cycle', 'center', 'periphery', 'dominating_set', 'maximal_independent_set']:
                x = {}
                for node in g.nodes():
                    x[node] = 0
                if v is not None:
                    for cycle in v:
                        for node in cycle:
                            x[node] += 1
                v = dict(x)
                retval[k] = v
                #print(k,'\t',type(v),'\t',len(v))
            elif k in ['laplacian_spectrum', 'adjacency_spectrum', 'modularity_spectrum']:
                v = float(max(v))
                retval[k] = v
                #print(k,'\t',type(v),'\t',v)            
            elif k in ['spectral_ordering']:
                x = {}
                for node in g.nodes():
                    x[node] = v.index(node)
                v = dict(x)
                retval[k] = v
                #print(k,'\t',type(v),'\t',v)            
            elif k in ['maximal_matching', 'max_weight_matching']:
                x = {}
                for node in g.nodes():
                    x[node] = 0
                for i,iset in enumerate(v):
                    for node in iset:
                        x[node] = i
                v = dict(x)
                retval[k] = v
                #print(k,'\t',type(v),'\t',len(v))
            elif k in ['min_edge_cover']:
                v = len(v)
                retval[k] = v
                #print(k,'\t',type(v),'\t',v)
            elif k in ['hits']:
                retval['hub_score'] = v[0]
                #print('hub_score','\t',type(v[0]),'\t',len(v[0]))
                retval['authority_score'] = v[1]
                #print('authority_score','\t',type(v[1]),'\t',len(v[1]))
                del retval[k]
            else:
                if v == False:
                    v = 0
                    #retval[k] = v
                if v == True:
                    v = 1
                    #retval[k] = v
                
                pass
                #print(k,'\t',type(v),'\t',v)
        else:
            if k in ['k_components']:
                v = {k2: len(v2[0]) for k2,v2 in v.items()}
                retval[k] = v
                #print(k,'\t',type(v),'\t',len(v))
            elif k in ['shortest_path']:                
                tmp = {}
                for k2, v2 in v.items():
                    tmpval = [len(v3) for k3,v3 in v2.items()]
                    tmp[k2] = sum(tmpval)/len(tmpval)
                v = tmp
                retval[k] = v
            else:
                #print(k,'\t',type(v),'\t',len(v))
                pass
                if False:
                    for k2,v2 in v.items():
                        try:
                            print('\t',k2,'\t',len(v2))
                        except:
                            print('\t',k2,'\t',v2)
                        
        if k in nodeAlgos:
            results["Nodes"][k] = retval[k]
        elif k in edgeAlgos:
            results["Edges"][k] = retval[k]
        elif k in netAlgos:
            results["Net"][k] = retval[k]
            
            
    df = DataFrame(results['Nodes'])
    df.index = list(g.nodes())
    results['Nodes'] = df
            
    df = DataFrame(results['Edges'])
    df.reset_index(drop=True)
    df.index = list(g.edges())
    results['Edges'] = df
        
    #df = DataFrame(results['Edges'])
    #df.index = list(g.edges())
    #results['Edges'] = df
            
    return results