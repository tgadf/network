from networkx import algorithms as algos
from networkx import linalg
from networkx import convert_matrix
from pandas import DataFrame
from types import GeneratorType

class networkAlgos():
    def __init__(self, g=None):
        self.g = g
    
    
    def compute(self, g=None, level=3, debug=False):
        if debug:
            print("Computing Network Algorithms")
        if not any([g, self.g]):
            print("There is no network to compute features for each algorithm")
            return
        else:
            if g is None:
                g = self.g

        self.nodeList = list(g.nodes())
        self.edgeList = list(g.edges())
        results = self.runNetworkAlgorithms(g, level=level, debug=debug)
        return results
    

    def runAlgos(self, algosToRun, g, debug=False, verydebug=False):
        if debug:
            print("Running network algorithms")
        results = {}
        for algo in algosToRun:
            name = algo.__name__
            if verydebug:
                print("  Running {0} algorithm".format(name))

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


    def getHeuristics(self):
        algosToRun = []
        #algosToRun.append(algos.all_pairs_node_connectivity)  # not needed
        algosToRun.append(algos.node_connectivity)
        #algosToRun.append(algos.k_components)
        algosToRun.append(algos.average_clustering)
        return algosToRun

    def getAssortativity(self):
        algosToRun = []
        algosToRun.append(algos.degree_assortativity_coefficient)
        algosToRun.append(algos.degree_pearson_correlation_coefficient)
        algosToRun.append(algos.average_neighbor_degree)
        #algosToRun.append(algos.average_degree_connectivity)
        algosToRun.append(algos.k_nearest_neighbors)
        #algosToRun.append(algos.degree_mixing_matrix)
        #algosToRun.append(algos.degree_mixing_dict)
        return algosToRun

    def getBipartite(self):
        algosToRun = []
        algosToRun.append(algos.is_bipartite)
        #algosToRun.append(algos.bipartite.sets)
        return algosToRun

    def getBridges(self):
        algosToRun = []
        algosToRun.append(algos.bridges)
        algosToRun.append(algos.has_bridges)    
        return algosToRun

    def getCentrality(self):
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
        #algosToRun.append(algos.percolation_centrality)
        #algosToRun.append(algos.second_order_centrality)
        return algosToRun

    def getChains(self):
        algosToRun = []
        algosToRun.append(algos.chain_decomposition)
        return algosToRun

    def getChordal(self):
        algosToRun = []
        algosToRun.append(algos.is_chordal)
        algosToRun.append(algos.chordal_graph_cliques)
        algosToRun.append(algos.chordal_graph_treewidth)
        algosToRun.append(algos.find_induced_nodes)
        return algosToRun

    def getCliques(self):
        algosToRun = []
        algosToRun.append(algos.enumerate_all_cliques)
        algosToRun.append(algos.find_cliques)
        #algosToRun.append(algos.make_max_clique_graph)
        #algosToRun.append(algos.make_clique_bipartite)
        algosToRun.append(algos.graph_clique_number)
        algosToRun.append(algos.graph_number_of_cliques)
        algosToRun.append(algos.node_clique_number)
        algosToRun.append(algos.number_of_cliques)
        #algosToRun.append(algos.cliques_containing_node) # Use for further analysis, but too complex
        return algosToRun

    def getClustering(self):
        algosToRun = []
        algosToRun.append(algos.triangles)
        algosToRun.append(algos.transitivity)
        algosToRun.append(algos.clustering)
        algosToRun.append(algos.average_clustering)
        algosToRun.append(algos.square_clustering)
        #algosToRun.append(algos.generalized_degree) # Returns dictionary ?
        return algosToRun

    def getCommunicability(self):
        algosToRun = []
        algosToRun.append(algos.communicability)
        return algosToRun

    def getCommunities(self):
        algosToRun = []
        #algosToRun.append(algos.community.kernighan_lin_bisection) # Not sure what to do with it
        algosToRun.append(algos.community.k_clique_communities)
        #algosToRun.append(algos.community.greedy_modularity_communities) # Not sure what to do with it
        #algosToRun.append(algos.community.asyn_lpa_communities) ?
        algosToRun.append(algos.community.label_propagation_communities)
        algosToRun.append(algos.community.asyn_fluidc)
        algosToRun.append(algos.community.girvan_newman)
        return algosToRun

    def getConnected(self):
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

    def getCore(self):
        algosToRun = []
        algosToRun.append(algos.core_number)
        algosToRun.append(algos.k_core)
        algosToRun.append(algos.k_shell)
        algosToRun.append(algos.k_crust)
        algosToRun.append(algos.k_corona)
        return algosToRun

    def getCover(self):
        algosToRun = []
        algosToRun.append(algos.min_edge_cover)
        algosToRun.append(algos.is_edge_cover)
        return algosToRun

    def getCycles(self):
        algosToRun = []
        algosToRun.append(algos.cycle_basis)
        algosToRun.append(algos.simple_cycles)
        algosToRun.append(algos.find_cycle)
        algosToRun.append(algos.minimum_cycle_basis)
        return algosToRun

    def getDAG(self):
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

    def getDistance(self):
        algosToRun = []
        algosToRun.append(algos.center)
        algosToRun.append(algos.diameter)
        algosToRun.append(algos.eccentricity)
        algosToRun.append(algos.extrema_bounding)
        algosToRun.append(algos.periphery)
        algosToRun.append(algos.radius)
        return algosToRun

    def getIntersection(self):
        algosToRun = []
        algosToRun.append(algos.is_distance_regular)
        algosToRun.append(algos.is_strongly_regular)
        algosToRun.append(algos.intersection_array)
        return algosToRun

    def getDominating(self):
        algosToRun = []
        algosToRun.append(algos.dominating_set)
        return algosToRun

    def getEfficiency(self):
        algosToRun = []
        algosToRun.append(algos.local_efficiency)
        algosToRun.append(algos.global_efficiency)
        return algosToRun

    def getEulerian(self):
        algosToRun = []
        algosToRun.append(algos.is_eulerian)
        return algosToRun

    def getFlow(self):
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

    def getHierachy(self):
        algosToRun = []
        algosToRun.append(algos.flow_hierarchy)
        return algosToRun

    def getIsolates(self):
        algosToRun = []
        algosToRun.append(algos.isolates)
        algosToRun.append(algos.number_of_isolates)
        return algosToRun

    def getLinkAnalysis(self):
        algosToRun = []
        algosToRun.append(algos.pagerank)
        #algosToRun.append(algos.google_matrix) # Underlying transition matrix for page rank
        algosToRun.append(algos.hits)
        #algosToRun.append(algos.hub_matrix) # Underlying matrix for Hub (in HITS)
        #algosToRun.append(algos.authority_matrix) # Underlying matrix for Authority (in HITS)
        return algosToRun

    def getLinkPrediction(self):
        algosToRun = []
        algosToRun.append(algos.resource_allocation_index)
        algosToRun.append(algos.jaccard_coefficient)
        algosToRun.append(algos.adamic_adar_index)
        algosToRun.append(algos.preferential_attachment)
        #algosToRun.append(algos.cn_soundarajan_hopcroft)
        #algosToRun.append(algos.ra_index_soundarajan_hopcroft)
        #algosToRun.append(algos.within_inter_cluster)
        return algosToRun    

    def getLowestCommonAncester(self):
        algosToRun = []
        algosToRun.append(algos.all_pairs_lowest_common_ancestor)
        algosToRun.append(algos.tree_all_pairs_lowest_common_ancestor)
        algosToRun.append(algos.lowest_common_ancestor)
        return algosToRun

    def getMatching(self):
        algosToRun = []
        algosToRun.append(algos.maximal_matching)
        algosToRun.append(algos.max_weight_matching)
        return algosToRun

    def getMIS(self):
        algosToRun = []
        algosToRun.append(algos.maximal_independent_set)
        return algosToRun

    def getReciprocity(self):
        algosToRun = []
        algosToRun.append(algos.reciprocity)
        algosToRun.append(algos.overall_reciprocity)
        return algosToRun

    def getRichClub(self):
        algosToRun = []
        algosToRun.append(algos.rich_club_coefficient)
        return algosToRun

    def getShortestPath(self):
        algosToRun = []
        algosToRun.append(algos.shortest_path)
        algosToRun.append(algos.all_shortest_paths)
        algosToRun.append(algos.shortest_path_length)
        algosToRun.append(algos.average_shortest_path_length)
        return algosToRun

    def getSMetric(self):
        algosToRun = []
        algosToRun.append(algos.s_metric)
        return algosToRun

    def getStructural(self):
        algosToRun = []
        algosToRun.append(algos.constraint)
        algosToRun.append(algos.effective_size)
        return algosToRun

    def getTree(self):
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

    def getTriadic(self):
        algosToRun = []
        algosToRun.append(algos.triadic_census)
        return algosToRun

    def getVitality(self):
        algosToRun = []
        algosToRun.append(algos.closeness_vitality)
        return algosToRun

    def getWiener(self):
        algosToRun = []
        algosToRun.append(algos.wiener_index)
        return algosToRun

    def getSpectrum(self):
        algosToRun = []
        algosToRun.append(linalg.laplacian_spectrum)
        algosToRun.append(linalg.adjacency_spectrum)
        algosToRun.append(linalg.modularity_spectrum)
        algosToRun.append(linalg.algebraic_connectivity)
        #algosToRun.append(linalg.fiedler_vector) ?
        algosToRun.append(linalg.spectral_ordering)
        return algosToRun

    def runNetworkAlgorithms(self, g, level=3, debug=False):
        algosToRun  = []
        algosToRun += self.getHeuristics()
        algosToRun += self.getAssortativity()
        algosToRun += self.getBipartite()
        algosToRun += self.getBridges()
        algosToRun += self.getCentrality()
        algosToRun += self.getChains()
        algosToRun += self.getChordal()
        algosToRun += self.getCliques()
        algosToRun += self.getClustering()
        if level >= 3:
            algosToRun += self.getCommunicability()
        if level >= 2:
            algosToRun += self.getCommunities()
        algosToRun += self.getConnected()
        algosToRun += self.getCore()
        algosToRun += self.getCover()
        if level >= 3:
            algosToRun += self.getCycles()
        algosToRun += self.getDAG()
        algosToRun += self.getDistance()
        algosToRun += self.getIntersection()
        algosToRun += self.getDominating()
        algosToRun += self.getEfficiency()
        algosToRun += self.getEulerian()
        algosToRun += self.getFlow()
        algosToRun += self.getHierachy()
        algosToRun += self.getIsolates()
        algosToRun += self.getLinkAnalysis()
        algosToRun += self.getLinkPrediction()
        algosToRun += self.getLowestCommonAncester()
        algosToRun += self.getMatching()
        algosToRun += self.getMIS()
        algosToRun += self.getReciprocity()
        algosToRun += self.getRichClub()
        algosToRun += self.getShortestPath()
        algosToRun += self.getSMetric()
        if level >=2:
            algosToRun += self.getStructural()
        algosToRun += self.getTree()
        algosToRun += self.getTriadic()
        if level >=3:
            algosToRun += self.getVitality()
        algosToRun += self.getWiener()
        algosToRun += self.getSpectrum()


        noneAlgos = ["in_degree_centrality", "out_degree_centrality", "katz_centrality", "betweenness_centrality_subset", "edge_betweenness_centrality_subset", "current_flow_betweenness_centrality_subset", "edge_current_flow_betweenness_centrality_subset", "local_reaching_centrality", "is_chordal", "chordal_graph_cliques", "chordal_graph_treewidth", "find_induced_nodes", "k_clique_communities", "asyn_fluidc", "is_strongly_connected", "number_strongly_connected_components", "is_weakly_connected", "number_weakly_connected_components", "is_attracting_component", "number_attracting_components", "is_semiconnected", "core_number", "k_core", "k_shell", "k_crust", "k_corona", "is_edge_cover", "simple_cycles", "is_aperiodic", "transitive_closure", "transitive_reduction", "antichains", "dag_longest_path", "dag_longest_path_length", "dag_to_branching", "intersection_array", "maximum_flow", "maximum_flow_value", "gomory_hu_tree", "network_simplex", "min_cost_flow_cost", "min_cost_flow", "cost_of_flow", "capacity_scaling", "flow_hierarchy", "all_pairs_lowest_common_ancestor", "tree_all_pairs_lowest_common_ancestor", "lowest_common_ancestor", "rich_club_coefficient", "all_shortest_paths", "s_metric", "is_arborescence", "is_branching", "triadic_census"]
        netAlgos  = ["node_connectivity", "k_components", "average_clustering", "degree_assortativity_coefficient", "degree_pearson_correlation_coefficient", "is_bipartite", "bridges", "has_bridges", "estrada_index", "global_reaching_centrality", "chain_decomposition", "enumerate_all_cliques", "find_cliques", "graph_clique_number", "graph_number_of_cliques", "transitivity", "kernighan_lin_bisection", "greedy_modularity_communities", "label_propagation_communities", "girvan_newman", "is_connected", "number_connected_components", "is_biconnected", "articulation_points", "min_edge_cover", "is_directed_acyclic_graph", "diameter", "extrema_bounding", "radius", "is_distance_regular", "is_strongly_regular", "local_efficiency", "global_efficiency", "is_eulerian", "isolates", "number_of_isolates", "resource_allocation_index", "jaccard_coefficient", "adamic_adar_index", "preferential_attachment", "reciprocity", "overall_reciprocity", "shortest_path_length", "average_shortest_path_length", "is_tree", "is_forest", "wiener_index", "laplacian_spectrum", "adjacency_spectrum", "modularity_spectrum", "algebraic_connectivity"]
        nodeAlgos = ["average_neighbor_degree", "degree_centrality", "eigenvector_centrality", "eigenvector_centrality_numpy", "katz_centrality_numpy", "closeness_centrality", "current_flow_closeness_centrality", "betweenness_centrality", "current_flow_betweenness_centrality", "approximate_current_flow_betweenness_centrality", "communicability_betweenness_centrality", "newman_betweenness_centrality", "subgraph_centrality", "subgraph_centrality_exp", "harmonic_centrality", "node_clique_number", "number_of_cliques", "cliques_containing_node", "triangles", "clustering", "square_clustering", "generalized_degree", "communicability", "cycle_basis", "find_cycle", "minimum_cycle_basis", "center", "eccentricity", "periphery", "dominating_set", "pagerank", "maximal_matching", "max_weight_matching", "maximal_independent_set", "shortest_path", "constraint", "effective_size", "closeness_vitality", "spectral_ordering", "hub_score", "authority_score"]
        edgeAlgos = ["edge_betweenness_centrality", "edge_current_flow_betweenness_centrality"]


        results = {"Net": {}, "Nodes": {}, "Edges": {}}
        retval = self.runAlgos(algosToRun, g, debug=debug)
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
                    for node in self.nodeList:
                        x[node] = 0
                    if v is not None:
                        for cycle in v:
                            for node in cycle:
                                try:
                                    x[node] += 1
                                except:
                                    continue
                    v = dict(x)
                    retval[k] = v
                    #print(k,'\t',type(v),'\t',len(v))
                elif k in ['laplacian_spectrum', 'adjacency_spectrum', 'modularity_spectrum']:
                    v = float(max(v))
                    retval[k] = v
                    #print(k,'\t',type(v),'\t',v)            
                elif k in ['spectral_ordering']:
                    x = {}
                    for node in self.nodeList:
                        x[node] = v.index(node)
                    v = dict(x)
                    retval[k] = v
                    #print(k,'\t',type(v),'\t',v)            
                elif k in ['maximal_matching', 'max_weight_matching']:
                    x = {}
                    for node in self.nodeList:
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
                if k in ['cliques_containing_node']:
                    v = {k2: len(v2) for k2,v2 in v.items()}
                elif k in ['k_components']:
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


        if debug:
            print("Creating Algorithm Results DataFrame for Vertices")
        df = DataFrame(results['Nodes'])
        df.index = list(self.nodeList)
        results['Nodes'] = df
        
        if debug:
            print("Ranking Vertices")
        ranks = {}
        for col in df.columns:
            rank = [int(x) for x in df[col].rank()]
            ranks[col] = rank
        df = DataFrame(ranks)
        df.index = list(self.nodeList)
        results['NodeRanks'] = df
            

        if debug:
            print("Creating Algorithm Results DataFrame for Edges")
        df = DataFrame(results['Edges'])
        df.reset_index(drop=True)
        df.index = list(self.edgeList)
        results['Edges'] = df

        #df = DataFrame(results['Edges'])
        #df.index = list(g.edges())
        #results['Edges'] = df

        return results