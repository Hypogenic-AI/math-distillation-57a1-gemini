#!/usr/bin/env python3
"""Stage-1 equational implication solver for magma laws.

Decision policy:
1) Search finite countermodels up to bounded order; if found => false.
2) Attempt bounded equational derivation; if found => true.
3) Otherwise return true (required strict boolean output), flagged as heuristic.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

Term = Tuple


@dataclass(frozen=True)
class Equation:
    left: Term
    right: Term


def var(name: str) -> Term:
    return ("var", name)


def mul(a: Term, b: Term) -> Term:
    return ("mul", a, b)


def split_mul(term: Term) -> Tuple[Term, Term]:
    return term[1], term[2]


def term_to_str(term: Term) -> str:
    if term[0] == "var":
        return term[1]
    a, b = split_mul(term)
    return f"({term_to_str(a)} * {term_to_str(b)})"


class Parser:
    def __init__(self, text: str):
        self.text = text.replace(" ", "")
        self.i = 0

    def peek(self) -> str:
        return self.text[self.i] if self.i < len(self.text) else ""

    def consume(self, ch: str) -> None:
        if self.peek() != ch:
            raise ValueError(f"Expected '{ch}' at {self.i} in {self.text!r}")
        self.i += 1

    def parse_var(self) -> Term:
        if not self.peek().isalpha():
            raise ValueError(f"Expected variable at {self.i} in {self.text!r}")
        ch = self.peek()
        self.i += 1
        return var(ch)

    def parse_factor(self) -> Term:
        if self.peek() == "(":
            self.consume("(")
            t = self.parse_term()
            self.consume(")")
            return t
        return self.parse_var()

    def parse_term(self) -> Term:
        t = self.parse_factor()
        while self.peek() == "*":
            self.consume("*")
            r = self.parse_factor()
            t = mul(t, r)
        return t


def parse_equation(text: str) -> Equation:
    if "=" not in text:
        raise ValueError(f"Equation must contain '=': {text!r}")
    lhs, rhs = text.split("=", 1)
    p1, p2 = Parser(lhs), Parser(rhs)
    lterm = p1.parse_term()
    rterm = p2.parse_term()
    if p1.i != len(p1.text) or p2.i != len(p2.text):
        raise ValueError(f"Unparsed suffix in equation: {text!r}")
    return Equation(lterm, rterm)


def vars_in_term(term: Term) -> Set[str]:
    if term[0] == "var":
        return {term[1]}
    a, b = split_mul(term)
    return vars_in_term(a) | vars_in_term(b)


def vars_in_equation(eq: Equation) -> List[str]:
    return sorted(vars_in_term(eq.left) | vars_in_term(eq.right))


def term_depth(term: Term) -> int:
    if term[0] == "var":
        return 0
    a, b = split_mul(term)
    return 1 + max(term_depth(a), term_depth(b))


def eval_term(term: Term, table: Sequence[int], n: int, env: Dict[str, int]) -> int:
    if term[0] == "var":
        return env[term[1]]
    a, b = split_mul(term)
    va = eval_term(a, table, n, env)
    vb = eval_term(b, table, n, env)
    return table[va * n + vb]


def equation_holds(eq: Equation, table: Sequence[int], n: int) -> bool:
    vlist = vars_in_equation(eq)
    for values in itertools.product(range(n), repeat=len(vlist)):
        env = dict(zip(vlist, values))
        if eval_term(eq.left, table, n, env) != eval_term(eq.right, table, n, env):
            return False
    return True


def find_countermodel(eq1: Equation, eq2: Equation, max_order: int = 3) -> Optional[Dict[str, object]]:
    for n in range(1, max_order + 1):
        for table in itertools.product(range(n), repeat=n * n):
            if equation_holds(eq1, table, n) and not equation_holds(eq2, table, n):
                grid = [list(table[i * n : (i + 1) * n]) for i in range(n)]
                return {
                    "order": n,
                    "table": grid,
                }
    return None


def generate_terms(variables: Sequence[str], max_depth: int) -> List[Term]:
    by_depth: List[Set[Term]] = [set(var(v) for v in variables)]
    all_terms: Set[Term] = set(by_depth[0])
    for d in range(1, max_depth + 1):
        cur: Set[Term] = set()
        prior = set().union(*by_depth[:d])
        for a in prior:
            for b in prior:
                cur.add(mul(a, b))
        by_depth.append(cur)
        all_terms.update(cur)
    return sorted(all_terms, key=term_to_str)


def substitute(term: Term, sigma: Dict[str, Term]) -> Term:
    if term[0] == "var":
        return sigma[term[1]]
    a, b = split_mul(term)
    return mul(substitute(a, sigma), substitute(b, sigma))


class UnionFind:
    def __init__(self, elems: Iterable[Term]):
        self.parent = {e: e for e in elems}

    def find(self, x: Term) -> Term:
        p = self.parent[x]
        if p != x:
            self.parent[x] = self.find(p)
        return self.parent[x]

    def union(self, a: Term, b: Term) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[rb] = ra
        return True


def derivable(eq1: Equation, eq2: Equation, max_depth: int = 2, sub_limit: int = 8) -> bool:
    all_vars = sorted(set(vars_in_equation(eq1) + vars_in_equation(eq2)))
    e1_depth = max(term_depth(eq1.left), term_depth(eq1.right))
    required_depth = max(max_depth, e1_depth, term_depth(eq2.left), term_depth(eq2.right))
    universe = generate_terms(all_vars, required_depth)
    uf = UnionFind(universe)

    e1_vars = vars_in_equation(eq1)
    local_pool = [t for t in universe if term_depth(t) == 0]
    sub_pool = local_pool[: min(sub_limit, len(local_pool))]

    for choice in itertools.product(sub_pool, repeat=len(e1_vars)):
        sigma = dict(zip(e1_vars, choice))
        lsub = substitute(eq1.left, sigma)
        rsub = substitute(eq1.right, sigma)
        if lsub in uf.parent and rsub in uf.parent:
            uf.union(lsub, rsub)

    return uf.find(eq2.left) == uf.find(eq2.right)


def solve_implication(
    e1: str,
    e2: str,
    max_order: int = 3,
    max_depth: int = 2,
    sub_limit: int = 8,
) -> Dict[str, object]:
    eq1, eq2 = parse_equation(e1), parse_equation(e2)
    cex = find_countermodel(eq1, eq2, max_order=max_order)
    if cex is not None:
        return {
            "e1": e1,
            "e2": e2,
            "answer": False,
            "mode": "countermodel",
            "countermodel": cex,
        }

    if derivable(eq1, eq2, max_depth=max_depth, sub_limit=sub_limit):
        return {
            "e1": e1,
            "e2": e2,
            "answer": True,
            "mode": "bounded_derivation",
        }

    return {
        "e1": e1,
        "e2": e2,
        "answer": True,
        "mode": "no_countermodel_up_to_bound",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--e1", required=True, help="Equation 1, e.g. 'x = x*y'")
    ap.add_argument("--e2", required=True, help="Equation 2, e.g. 'x = x*x'")
    ap.add_argument("--max-order", type=int, default=3)
    ap.add_argument("--max-depth", type=int, default=2)
    ap.add_argument("--sub-limit", type=int, default=8)
    args = ap.parse_args()

    out = solve_implication(
        args.e1,
        args.e2,
        max_order=args.max_order,
        max_depth=args.max_depth,
        sub_limit=args.sub_limit,
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
