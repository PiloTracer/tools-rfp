# UNKNOWNS - planning registry

**Updated:** 2025-07-17 · **Maintained by:** plan-foundation / plan-master

| ID | Question / blocker | Blocks | Owner | Status |
|----|-------------------|--------|-------|--------|
| U1 | What is the ceiling on RFP document page count for reasonable processing time? | Document pipeline design | eng | Open |
| U2 | What embedding + chunking strategy works best for RFP-style structured docs? | RAG pipeline | eng | Open |
| U3 | How much fine-tuning vs RAG is needed for domain-specific RFP terminology? | LLM strategy | eng | Open |
| U4 | What's an acceptable per-RFP processing cost at V1 scale? | Model tier assignment | product | Open |
| U5 | What file size / page limits should the uploader enforce? | Upload UX | product | Open |
| U6 | CI platform choice | Pipeline design | eng | Open |
| U7 | What concurrent user count for V1? | Scaling architecture | eng | Open |
| U8 | SOC2/GDPR compliance requirement at launch or deferred? | Compliance ADR | legal/product | Open |
| U9 | V1 scope too large for timeline — which features to cut? | Feature prioritization | product | Open |
| U10 | Baseline win rate / cost / volume metrics for success measurement | Success criteria | product | Open |

| U11 | Optimal chunk size and overlap for KB entries | RAG pipeline quality | eng | Open |
| U12 | Embedding model selection (text-embedding-3-small vs ada vs local) | RAG quality, cost | eng | Open |
| U13 | Confidence scoring formula: pure retrieval overlap or combined with LLM logprobs | Draft quality signals | eng | Open |
| U14 | Max KB entry count per retrieval query | RAG performance | eng | Open |
| U15 | Should per-question generation stream results to the UI? | UX design | product | Open |
| U16 | Accessibility standards (WCAG level) and responsive breakpoints for frontend | UX scope | eng/product | Open |

## Review log

| Date | Reviewer | Action |
|------|----------|--------|
| 2025-07-17 | plan-foundation | Initial populate from greenfield P0 |