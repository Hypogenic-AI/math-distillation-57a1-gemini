import json
import os
import networkx as nx

def main():
    with open("code/equational_theories/data/equations.txt", "r") as f:
        equations = [line.strip().replace("◇", "*") for line in f]
    
    id_to_eq = {i+1: eq for i, eq in enumerate(equations)}

    with open("code/equational_theories/full_entries.json", "r") as f:
        data = json.load(f)

    G = nx.DiGraph()
    G.add_nodes_from(range(1, 4695))

    for entry in data:
        variant = entry.get("variant", {})
        if "implication" in variant:
            lhs_str = variant["implication"]["lhs"]
            rhs_str = variant["implication"]["rhs"]
            if "Equation" in lhs_str and "Equation" in rhs_str:
                lhs = int(lhs_str.replace("Equation", ""))
                rhs = int(rhs_str.replace("Equation", ""))
                if lhs <= 4694 and rhs <= 4694:
                    G.add_edge(lhs, rhs)
    
    sccs = list(nx.strongly_connected_components(G))
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    print(f"Number of SCCs: {len(sccs)}")
    
    # Sort SCCs by size
    sccs.sort(key=len, reverse=True)
    for i, scc in enumerate(sccs[:10]):
        if len(scc) > 1:
            print(f"SCC {i} (size {len(scc)}): {[f'E{eid}' for eid in list(scc)[:5]]}...")
        else:
            eid = list(scc)[0]
            # print(f"Singleton E{eid}: {id_to_eq[eid]}")

    # Build condensation graph (DAG)
    C = nx.condensation(G)
    print(f"Condensation graph has {C.number_of_nodes()} nodes and {C.number_of_edges()} edges.")
    
    # Save the most important parts for the cheatsheet
    # We want to identify the "top" of the DAG (strongest laws)
    top_nodes = [n for n, d in C.in_degree() if d == 0]
    print(f"Number of 'maximal' laws: {len(top_nodes)}")
    
    for n in top_nodes[:10]:
        scc_members = C.nodes[n]['members']
        rep_eid = list(scc_members)[0]
        print(f"Maximal SCC node {n} (rep E{rep_eid}: {id_to_eq[rep_eid]})")

if __name__ == "__main__":
    main()
