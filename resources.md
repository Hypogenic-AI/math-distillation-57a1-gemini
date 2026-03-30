# Resources Catalog: Mathematics Distillation Challenge

## Summary
This document catalogs all papers, datasets, and computational tools gathered for the Mathematics Distillation Challenge.

## Papers
Total papers cataloged: 5

| Title | Authors | Year | File | Key Results |
|-------|---------|------|------|-------------|
| The Equational Theories Project | Bolan et al. | 2025 | papers/2512.07087_Equational_Theories_Project.pdf | Foundational project with 22M implications. |
| The latent space of equational theories | Berlioz et al. | 2026 | papers/2601.20759_latent_space_equational_theories.pdf | Statistical organization of equations. |
| Twitch: Learning Abstractions | Axelrod et al. | 2026 | papers/2603.06849_learning_abstractions_...pdf | Pattern discovery for proofs. |
| Learning Equational Thm Proving | Piepenbrock et al. | 2021 | papers/2102.05547_learning_equational_...pdf | Imitation learning for proofs. |
| Mace4 Manual | McCune | 2003 | papers/cs_0310055_mace4_manual.pdf | Guide to the counterexample finder. |

## Prior Results Catalog

| Result | Description | Relevance |
|--------|-------------|-----------|
| Duality ($E^*$) | Every law $E$ has a dual. $E_1 \models E_2 \iff E_1^* \models E_2^*$ | Distillation symmetry |
| Stone Pairing | Feature mapping from finite models to theories | Statistical distillation |
| 3SIL (Imitation Learning) | Training on proof trajectories | Expert distillation |
| Twitch Abstractions | Discovered recurring term patterns | Symbolic distillation |

## Computational Tools

| Tool | Purpose | Location |
|------|---------|----------|
| teorth/equational_theories | Main ETP project | code/equational_theories/ |
| Twitch | Pattern discovery (from 2603.06849) | (Academic project) |
| Mace4 | Finite model finder | (Tool discussed in ETP) |
| Vampire / Prover9 | High-performance ATPs | (Informed by paper results) |
| Equation Explorer | Implication graph browser | [Online](https://teorth.github.io/equational_theories/) |

## Recommended strategy
1.  **Extract Patterns**: Use the "Twitch" concept to find common patterns in the 22M implications.
2.  **Map Latent Space**: Use the "Stone pairing" concept from Berlioz to identify clusters.
3.  **Syntactic Pruning**: Use the variable rules identified in the ETP paper (Section 10).
