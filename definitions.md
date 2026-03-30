## Definitions and Notation

- A **magma** is a pair `(M, *)` where `M` is a non-empty set and `* : M x M -> M` is a binary operation.
- A **term** is built from variables (`x,y,z,...`) using `*` and parentheses.
- An **equation** is an identity `s = t` between two terms.
- For a magma `A`, `A |= s=t` means for every variable assignment into `A`, terms `s,t` evaluate equally.
- **Implication**: `E1 |= E2` iff every magma satisfying `E1` also satisfies `E2`.
- **Countermodel** to implication `E1 => E2`: a magma `A` such that `A |= E1` and `A !|= E2`.

### Stage-1 Decision Mapping
Given `(E1,E2)`, output:
- `false` if a countermodel is found.
- `true` otherwise (possibly justified by bounded derivation evidence).

This matches the competition Stage 1 boolean output contract.
