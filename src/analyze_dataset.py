import json
import os
import re

def parse_term(term_str):
    # Simplistic parser for magma terms
    return term_str.replace(" ", "").replace("◇", "*")

def get_vars(term_str):
    return set(re.findall(r'[a-z]', term_str))

def get_dual(eq_str):
    # Dual of a magma equation is swapping LHS and RHS of each '*'
    # This is a bit complex to do with regex for nested terms.
    # Actually, the dual is defined by swapping the order of arguments in every multiplication.
    # (x * y)* becomes (y* * x*)
    # But since it's a magma, we just need to flip the trees.
    
    def flip(t):
        t = t.strip()
        if "*" not in t:
            return t
        # Find the main '*'
        depth = 0
        for i in range(len(t)):
            if t[i] == '(': depth += 1
            elif t[i] == ')': depth -= 1
            elif t[i] == '*' and depth == 0:
                left = t[:i]
                right = t[i+1:]
                return f"({flip(right)} * {flip(left)})"
        # If wrapped in parens
        if t.startswith("(") and t.endswith(")"):
            return flip(t[1:-1])
        return t

    if "=" not in eq_str: return eq_str
    lhs, rhs = eq_str.split("=")
    return f"{flip(lhs)} = {flip(rhs)}"

def main():
    with open("code/equational_theories/data/equations.txt", "r") as f:
        equations = [line.strip().replace("◇", "*") for line in f]
    
    # Map from Eq text to ID (1-indexed)
    eq_to_id = {eq: i+1 for i, eq in enumerate(equations)}
    id_to_eq = {i+1: eq for i, eq in enumerate(equations)}

    # Ground truth from full_entries.json
    with open("code/equational_theories/full_entries.json", "r") as f:
        data = json.load(f)

    implications = []
    refutations = []
    
    for entry in data:
        variant = entry.get("variant", {})
        if "implication" in variant:
            lhs_str = variant["implication"]["lhs"]
            rhs_str = variant["implication"]["rhs"]
            if "Equation" in lhs_str and "Equation" in rhs_str:
                lhs = int(lhs_str.replace("Equation", ""))
                rhs = int(rhs_str.replace("Equation", ""))
                if lhs <= 4694 and rhs <= 4694:
                    implications.append((lhs, rhs))
        elif "facts" in variant:
            # Some entries list multiple facts
            satisfied = variant["facts"].get("satisfied", [])
            refuted = variant["facts"].get("refuted", [])
            # This format is different, it usually means "Law X satisfies/refutes Law Y"
            # But the 'full_entries.json' structure is actually quite complex.
            pass

    print(f"Loaded {len(equations)} equations.")
    print(f"Loaded {len(implications)} explicit implications.")

    # Calculate "Strength" (how many things it implies)
    strength = {}
    for lhs, rhs in implications:
        strength[lhs] = strength.get(lhs, 0) + 1

    top_strong = sorted(strength.items(), key=lambda x: x[1], reverse=True)[:20]
    print("\nTop 20 Strongest Equations:")
    for eid, s in top_strong:
        print(f"E{eid}: {id_to_eq[eid]} (Implies {s})")

    # Analyze syntactic rules
    false_positives = 0
    for lhs_id, rhs_id in implications:
        l_eq = id_to_eq[lhs_id]
        r_eq = id_to_eq[rhs_id]
        
        l_vars = get_vars(l_eq)
        r_vars = get_vars(r_eq)
        
        # Rule: RHS variables must be a subset of LHS variables?
        # Actually, if LHS implies RHS, any variable in RHS must be "fixed" or "irrelevant".
        # Example: x = y implies x = x*x. LHS vars {x, y}, RHS vars {x}. (True)
        # Example: x = x*x implies x = x*y. LHS vars {x}, RHS vars {x, y}. (False)
        if not r_vars.issubset(l_vars):
            # If this happens, it's a very strong law (like x=y or x=z*w)
            pass

    # Save summary for cheatsheet construction
    summary = {
        "top_strong": [{"id": eid, "eq": id_to_eq[eid], "strength": s} for eid, s in top_strong],
        "implications_count": len(implications)
    }
    with open("results/data_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
