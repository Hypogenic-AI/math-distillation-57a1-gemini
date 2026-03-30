# Outline: Distilling 22 Million Implications: A Compact Guide to Magma Equational Theories

## 1. Title & Abstract
- **Title**: Distilling 22 Million Implications: A Compact Guide to Magma Equational Theories
- **Abstract**: 
    - **Context**: The Equational Theories Project (ETP) has mapped 22 million implications across 4,694 magma laws.
    - **Gap**: This vast knowledge is inaccessible to resource-constrained systems like LLMs or for quick human reference.
    - **Approach**: We distill this dataset into a 10KB "cheatsheet" using strongly connected components (SCCs), syntactic heuristics, and algebraic duality.
    - **Results**: Identified 1,415 SCCs; compressed the hierarchy into a 9.1KB guide covering over 50% of laws; established variable-preservation heuristics with absorption-law exceptions.
    - **Significance**: Enables accurate determination of equational implications without full graph storage.

## 2. Introduction
- **Hook**: Scale of modern collaborative mathematics (Terence Tao's ETP).
- **Background**: Equational theories as the bedrock of algebra; the complexity of magmas.
- **Gap**: The 22M edge graph is too large for prompt-based LLM reasoning.
- **Contribution**:
    - SCC-based clustering of 4,694 laws into 1,415 equivalence classes.
    - Formalization of syntactic heuristics (variable distribution, term depth).
    - Design and validation of a 10KB hierarchical cheatsheet.
    - Duality-based reasoning to double information density.
- **Organization**: Preliminaries, SCC structure, Heuristics, Distillation Algorithm, Discussion.

## 3. Preliminaries
- **Definitions**: 
    - Magma $(M, \diamond)$.
    - Equational Law $E: t_1 = t_2$.
    - Entailment $E \models E'$.
    - Duality $E^*$: mirror image of the operation.
- **Notation**: E1-E4694 (ETP numbering).
- **Prerequisites**: Duality Theorem ($E \models E' \iff E^* \models E'^*$).

## 4. Main Results: Structural Decomposition
- **Strongly Connected Components**:
    - Theorem: The implication graph admits a directed acyclic graph (DAG) of SCCs.
    - Data: 1,415 SCCs found. 
    - Largest SCCs: Trivial law (1,500 members), Constant law (400 members).
- **Hierarchy of Strength**:
    - Defining law strength by its out-degree in the sample graph.
    - Top 40 SCCs represent the "core" of the theory space.

## 5. Main Results: Syntactic Heuristics
- **Variable Preservation**:
    - Lemma: If $E \models E'$, then $\text{Var}(E') \subseteq \text{Var}(E)$ for non-degenerate theories.
    - Exception: Absorption laws ($x \diamond (x \diamond y) = x$) and Constant laws ($x \diamond y = z \diamond w$).
- **Term Depth Bounds**:
    - Correlation between law order (complexity) and implication depth.

## 6. Main Results: The Distillation Algorithm
- **Clustering Strategy**: Grouping laws by semantic equivalence.
- **Compression**: Representing SCCs by their "strongest" or most concise member.
- **Cheatsheet Design**:
    - Level 1: Core Definitions (Trivial, Constant).
    - Level 2: Syntactic Rules (Variables, Duality).
    - Level 3: The Top-40 SCC DAG.
    - Level 4: Special Cases (e.g., E14 $\implies$ Commutativity).

## 7. Discussion
- **Size vs. Accuracy**: The 10KB bottleneck.
- **LLM Reasoning**: How syntactic rules complement statistical prediction.
- **Limits of Distillation**: Where the cheatsheet fails (hard implications needing long proofs).

## 8. Conclusion
- **Summary**: Successfully distilled 22M edges into 9.1KB.
- **Future Work**: Huffman coding for rules; latent space coordinates.

## 9. References
- Bolan et al. (2025) - ETP Foundation.
- Berlioz & Melliès (2026) - Latent Space.
- Axelrod et al. (2026) - Twitch/Abstractions.
- Piepenbrock et al. (2021) - Learning Proofs.
