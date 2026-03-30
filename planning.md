# Research Planning: Mathematics Distillation Challenge

## Motivation & Novelty Assessment

### Why This Research Matters
Determining equational implications is a fundamental problem in universal algebra and automated theorem proving. The Equational Theories Project has generated a massive graph of 22M implications, but this knowledge is too large for efficient use in small language models or quick human reference. Distilling this into a 10KB "cheatsheet" is a significant step towards enabling compact, reliable mathematical reasoning in resource-constrained models.

### Gap in Existing Work
While high-performance automated theorem provers (ATPs) like Vampire or Prover9 can solve these problems, they are computationally heavy and not easily integrated into the prompt-based reasoning of LLMs. Current neural approaches (e.g., CNNs) for predicting implications are much larger than the 10KB limit. There is a missing link between the raw formal data of the ETP and a compact, human-interpretable (or LLM-interpretable) guide for reasoning.

### Our Novel Contribution
We propose a multi-layered cheatsheet that combines:
1.  **Syntactic Pruning Rules**: Formal rules about variable distribution and term depth that eliminate obvious non-implications.
2.  **Canonical Theory Clusters**: Grouping the 4,694 laws into clusters based on their semantic behavior (e.g., "constant-like", "idempotent-like") and defining implications between these clusters.
3.  **Critical Implication Graph**: A highly compressed version of the most influential edges in the implication graph.
4.  **Proof Heuristics**: Guidance on standard rewriting techniques (e.g., substitution strategies) for common magma identities.

### Experiment Justification
- **Experiment 1 (Syntactic Rule Extraction)**: We need to verify which syntactic rules (e.g., "variables in RHS must be in LHS") are 100% reliable for magmas.
- **Experiment 2 (Clustering & Mapping)**: We will test if clustering equations by their "strength" (number of implications) allows for a hierarchical cheatsheet.
- **Experiment 3 (Benchmark Validation)**: We will run the `implication_solver.py` on a sample of the 22M edges to identify "hard" cases where simple rules fail, and use these to refine the cheatsheet.

## Research Question
Can a 10KB cheatsheet of syntactic rules, theory clusters, and compressed implication subgraphs enable an LLM to accurately determine equational implications over magmas?

## Hypothesis Decomposition
1.  **H1 (Syntactic Sufficiency)**: A significant portion (~70%) of false implications can be identified by simple syntactic rules (variable check, depth bounds).
2.  **H2 (Cluster Implication)**: Grouping laws into semantic categories allows for broad-stroke reasoning that handles the majority of true implications.
3.  **H3 (Duality)**: Leveraging the duality of magma operations effectively halves the information needed in the cheatsheet.

## Proposed Methodology

### Approach
We will analyze the `full_entries.json` and `equations.txt` to extract the most informative patterns. We will use `implication_solver.py` to generate "hard" samples (where order-3 countermodels or 2-depth proofs are insufficient) and prioritize these for explicit inclusion in the cheatsheet.

### Experimental Steps
1.  **Data Extraction**: Map Equation IDs to text and build a local adjacency list of the implication graph.
2.  **Rule Mining**: Identify universal "negative" rules (if X then False) and "positive" rules (if Y then True).
3.  **Compression**: Use Huffman-like or semantic compression to fit the most valuable information into 10KB.
4.  **Validation**: Test the draft cheatsheet against a held-out set of implications.

## Timeline and Milestones
- Phase 1: Planning & Motivation (Now)
- Phase 2: Implementation - Rule Mining & Data Analysis (30 min)
- Phase 3: Analysis - Cheatsheet Construction (30 min)
- Phase 4: Validation & Refinement (30 min)
- Phase 5: Final Documentation (10 min)

## Success Criteria
- A cheatsheet under 10,240 bytes.
- Accuracy > 90% on a balanced set of magma implications (E1-E4694).
