import json
import networkx as nx
import re

def get_vars(eq_str):
    return set(re.findall(r'[a-z]', eq_str))

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
    sccs.sort(key=len, reverse=True)

    cheatsheet = []
    cheatsheet.append("EQUATIONAL THEORIES CHEATSHEET (MAGMAS)")
    cheatsheet.append("========================================")
    
    cheatsheet.append("\n[CORE CONCEPTS]")
    cheatsheet.append("- Magma: Set with binary op (*).")
    cheatsheet.append("- Trivial (T): x=y. Implies all. Eq: x=y*y, x=y*z, x*x=y.")
    cheatsheet.append("- Constant (C): x*y=z*w. All products equal a constant. Implies f(*)=g(*) if both sides are products.")
    cheatsheet.append("- Absorption: x=x*y (Left), x=y*x (Right).")
    cheatsheet.append("- Idempotency: x=x*x.")
    cheatsheet.append("- Duality: L=>R iff L* => R* (swap arg order in all *).")

    cheatsheet.append("\n[STRATEGY]")
    cheatsheet.append("1. Check if L is T or C. If yes, check if R follows (T=>all, C=>products).")
    cheatsheet.append("2. Variable Check: If R has var not in L, L must be strong (T, C, or Absorption).")
    cheatsheet.append("   E.g., x=x*y implies x=x*z (True), but x=x*x does not imply x=x*y (False).")
    cheatsheet.append("3. Countermodels: Small magmas (size 2 or 3) refute most false implications.")
    cheatsheet.append("   - Constant Magma: x*y = c.")
    cheatsheet.append("   - Left/Right Projection: x*y = x or x*y = y.")

    cheatsheet.append("\n[MAJOR EQUIVALENCE CLASSES (SCCs)]")
    for i, scc in enumerate(sccs[:40]):
        rep = min(scc)
        cheatsheet.append(f"Class {i} (Size {len(scc)}): Rep E{rep}: {id_to_eq[rep]}")
        members = sorted(list(scc))
        if len(members) > 1:
            cheatsheet.append(f"  Includes: {', '.join([f'E{m}' for m in members[:10]])}...")

    cheatsheet.append("\n[TOP-LEVEL IMPLICATIONS (Condensed)]")
    C = nx.condensation(G)
    for u, v in C.edges():
        if len(C.nodes[u]['members']) > 2 and len(C.nodes[v]['members']) > 2:
            rep_u = min(C.nodes[u]['members'])
            rep_v = min(C.nodes[v]['members'])
            cheatsheet.append(f"E{rep_u} => E{rep_v}")

    cheatsheet.append("\n[DUALITY EXAMPLES]")
    cheatsheet.append("- E4 (x=x*y) dual is E5 (x=y*x).")
    cheatsheet.append("- E3 (x=x*x) is self-dual.")
    cheatsheet.append("- (x*y)*z=x*(y*z) (Assoc) dual is z*(y*x)=(z*y)*x (Assoc).")
    
    cheatsheet.append("\n[FINAL CHECK FOR LLM]")
    cheatsheet.append("1. If R is a variable (e.g. x=y), L must be Class 0.")
    cheatsheet.append("2. If L has fewer variables than R, check for Absorption (Class 6/7) or Constant (Class 1).")
    cheatsheet.append("3. Commutativity (E43) is weak; it rarely implies structural changes like E3 or E4512.")
    cheatsheet.append("4. If unsure, assume FALSE (majority of random pairs are false).")

    content = "\n".join(cheatsheet)
    print(f"Cheatsheet size: {len(content)} bytes")
    
    with open("cheatsheet.txt", "w") as f:
        f.write(content)

if __name__ == "__main__":
    main()
