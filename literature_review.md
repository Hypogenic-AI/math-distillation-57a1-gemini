# Literature Review: Mathematics Distillation Challenge (Equational Theories)

## Research Area Overview
The **Equational Theories Project (ETP)**, led by Terence Tao, is a massive collaborative effort to map the implication graph between 4,694 simple equational laws on magmas. The primary result is a graph with over 22 million edges (implications). The current challenge focuses on **Mathematics Distillation**: reducing this knowledge into a 10KB "cheatsheet" to guide small LLMs in solving implication problems.

## Key Definitions
- **Magma**: A set $M$ with a binary operation $\diamond: M \times M \to M$.
- **Equational Law**: An identity $t_1 = t_2$ involving variables and $\diamond$.
- **Entailment ($E \models E'$)**: Every magma satisfying $E$ also satisfies $E'$.
- **Order of a law**: Complexity measure (number of $\diamond$ operations).

## Key Papers

### 1. The Equational Theories Project: Advancing Collaborative Mathematical Research at Scale (arXiv:2512.07087)
- **Authors**: Bolan et al. (2025)
- **Contribution**: The foundational ETP paper. Formalized the 22M implications in Lean 4. Discusses the use of CNNs for implication prediction (99.7% accuracy) and the numbering system (E1-E4694).

### 2. The latent space of equational theories (arXiv:2601.20759)
- **Authors**: Berlioz and Melliès (2026)
- **Contribution**: Defines a **latent space** for equational theories based on their behavior on finite magmas. Discovers that reasoning "flows" in an oriented way in this space.
- **Relevance**: Suggests a statistical/geometric approach to distillation. A cheatsheet could potentially encode coordinates or clusters in this latent space.

### 3. Twitch: Learning Abstractions for Equational Theorem Proving (arXiv:2603.06849)
- **Authors**: Axelrod et al. (2026)
- **Contribution**: Introduces **Twitch**, a tool that discovers recurring term patterns (abstractions) from proofs.
- **Relevance**: Useful for identifying the "interesting shapes" of equations that indicate certain properties (e.g., associativity-like behavior).

### 4. Learning Equational Theorem Proving (arXiv:2102.05547)
- **Authors**: Piepenbrock et al. (2021)
- **Contribution**: Uses **3SIL** (Imitation Learning) to solve equational proofs. Outperforms hand-engineered provers like *Waldmeister*.
- **Relevance**: Demonstrates that imitation learning on proof steps is a viable way to "distill" theorem proving expertise into a neural model.

## Known Results (Prerequisite Theorems)
- **Duality**: $E_1 \models E_2 \iff E_1^* \models E_2^*$. This effectively doubles the training data and should be part of any cheatsheet.
- **Trivial/Singleton Bounds**: E1 (weakest) and E2 (strongest) define the boundaries of the implication graph.
- **Constant Law (E46)**: $x \diamond y = z \diamond w$ is extremely strong and implies almost everything.

## Proof Techniques in the Literature
- **Equational Reasoning**: Rewriting terms using substitution.
- **Finite Model Finding**: Using **Mace4** to find counterexamples.
- **Stone Pairing**: A technique for mapping theories to feature spaces (Berlioz & Melliès).

## Gaps and Opportunities
- **10KB Bottleneck**: Most neural models (CNNs) for this task are 700KB+. Distilling this into 10KB of natural language or compressed rules is the primary research gap.
- **Syntactic vs Semantic**: Berlioz shows that semantic behavior on finite magmas is a strong proxy for formal implication.

## Recommendations for Cheatsheet Strategy
1.  **Rule of Thumb for Variables**: "If $E'$ has variables not in $E$, it is likely false unless $E$ is a constant or singleton law."
2.  **Cluster Descriptions**: Use the latent space findings to group equations into clusters (e.g., "Associative-like", "Idempotent-like").
3.  **Pattern Recognition**: Include the "Twitch" abstractions—common term patterns that imply certain structural properties.
