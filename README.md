# Equational Theories Distillation

Distilling the implication graph of 4,694 simple magma equational laws into a 10KB cheatsheet for LLM-based implication solving.

## Key Results
- **9.1KB Cheatsheet**: A structured prompt guide with SCCs, implications, and syntactic heuristics.
- **1,415 SCCs**: Grouped equivalent magma laws from the ETP dataset.
- **Hierarchy Mapping**: Identified core laws (Trivial, Constant, Absorption, Idempotency) and their implications.

## Files
- `cheatsheet.txt`: The final 9.1KB guidance file for the competition.
- `REPORT.md`: Detailed research report with methodology and findings.
- `src/`: Python scripts for data analysis, clustering, and cheatsheet generation.

## How to Reproduce
1.  Ensure `code/equational_theories/` is populated with the ETP dataset.
2.  Run `python3 src/generate_cheatsheet.py` to regenerate `cheatsheet.txt`.
