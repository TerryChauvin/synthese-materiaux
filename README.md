<p align="center"><b>English</b> · <a href="README.fr.md">Français</a></p>

# Materials Synthesis Routes Database

**A verifiable database of materials synthesis protocols, extracted from open-access papers by a multi-agent pipeline. Every value carries the verbatim quote that supports it.**

![Publications](https://img.shields.io/badge/publications_closed-268_%2F_500-blue)
![Routes](https://img.shields.io/badge/synthesis_routes-2942-green)
![Quotes](https://img.shields.io/badge/audited_quotes_found_verbatim-100%25-brightgreen)
![Licence](https://img.shields.io/badge/sources-Creative_Commons-lightgrey)

---

## Why this exists

The synthesis literature is huge but hard to reuse. Conditions are scattered across Methods, Results, tables, captions and supplementary files. Sample series are described in one sentence ("the same procedure was repeated at 150 and 180 °C"). Missing information, such as an unstated annealing atmosphere, is never flagged.

This database answers two questions for each paper:

1. **What exactly does the paper say** about every reagent, step, parameter and result, for every variant the authors compared?
2. **What does it leave out**, and what in it is inconsistent or doubtful for a trained reader?

The goal is that a chemist can **reproduce a material from the database alone** and see **how each synthesis variation tested by the authors changes the outcome**.

## What is inside

| | |
|---|---|
| Publications closed (all passes done) | 268 (250 in the five audited batches) |
| Synthesis routes | 2 942 (698 base routes, 2 244 branches) |
| Steps / reagents / parameters | 4 824 / 3 928 / 6 463 |
| Measured outcomes | 21 529 |
| Fidelity and science findings | 2 356 |
| Annotations (interpretations, kept apart from data) | 5 561 |

Figures as of 17 October 2026 (`synthese.db`, read-only queries on closed publications). The target is **500 publications**, built in audited batches of 50.

Material families covered: MOFs and ZIFs, metal nanoparticles, oxides, perovskites, zeolites and mesoporous silicas, chalcogenides and phosphides, carbons, electrode materials, ceramics, 2D materials, quantum dots.

## How a paper becomes data

Each publication goes through five passes, run by language-model agents with separate roles. No agent checks its own work.

```
 article (Europe PMC, CC licence) + supplementary files + figures
   │
   ▼
 1. Extraction ............ reads the full text, inventories every sample, writes routes,
   │                        branches, quotes, and what is NOT stated
   ▼
 2. Automatic check ....... every quote must be found verbatim in the text,
   │                        every number must appear in its quote
   ▼
 3. Fidelity critique ..... an independent second reader re-reads the article first,
   │                        then compares it with the extraction
 4. Science critique ...... stoichiometry, physical plausibility, consistency with the
   │                        founding literature, sourced web search
   ▼
 5. Corrections ........... applied by a separate agent, decided by the orchestrator,
                            each finding marked corrected or rejected with a reason
```

Every 50 papers, an **audit** re-checks every quote, runs physico-chemical sanity tests, re-reads a sample of values by hand, recomputes the stoichiometry of five routes, cross-compares syntheses of the same material across papers, and checks cited sources.

## Ground rules

- **The quote is the proof.** No value without an exact quote. Nothing invented, inferred or converted on the authors' behalf (SI conversion is stored in a separate column).
- **Absence is data.** What the paper does not state is recorded explicitly (`not_stated`), so a route is never silently "complete".
- **Every comparison counts.** All variants compared by the authors are captured as branches, including failed attempts.
- **Author errors are kept, not fixed.** Inconsistencies in a paper are flagged as reproducibility limits, never repaired in the data.
- **Interpretation is separate from data.** Annotations are typed and stored apart from extracted values.
- **A mistake seen twice becomes a written rule** in the extraction protocol.

## Measured quality (first 200 papers, batches 1 to 4)

| Check | Result |
|---|---|
| Quotes found verbatim in the source text | 37 478 / 37 478 (100 %) |
| Values re-read by hand against the paper | 3 593, of which 10 wrong, all in the 10 calibration papers |
| Error rate after calibration | 1 / 3 032 values (0.03 %, 95 % upper bound ≈ 0.16 %) |
| Fidelity findings | 1 770, median 8 per paper; none a mis-copied number since batch 2 |
| Science verdicts on routes | 434 consistent, 604 doubtful, 46 inconsistent, 82 unverifiable |

Batch 5 (papers 201–250, report `audits/palier_005_relecture.md`): 9 581 quotes found verbatim (100 %), 1 112 values re-read by hand with 0 wrong, 428 fidelity findings (median 8 per paper, 4 "wrong"), 0 blocking audit finding.

Most "doubtful" verdicts come from the papers themselves, not from the extraction. Typical examples: a reported cobalt content heavier than pure cobalt, a "HeNe laser at 532 nm", an aqueous dispersion "stirred at 350 °C". These are kept as written and flagged.

**Scope.** The database guarantees faithfulness to the source and makes explicit what is missing to reproduce a synthesis. It does not guarantee that a published protocol works.

## Using the database

`synthese.db` is a plain SQLite file. Open it with DB Browser for SQLite, DBeaver, or Python.

Full protocol of one branch, with quotes:

```sql
SELECT step_order, action, parameter, value_num, value_text, unit, quote
FROM v_route_complete
WHERE pmcid = 'PMC0000000' AND branch_label = 'ZnO-180'
ORDER BY step_order;
```

All hydrothermal syntheses between 150 and 200 °C:

```sql
SELECT DISTINCT pmcid, branch_label, material, value_num AS temp_C, quote
FROM v_route_complete
WHERE method LIKE '%hydrothermal%' AND parameter = 'temperature'
  AND unit = '°C' AND value_num BETWEEN 150 AND 200;
```

What a chemist must know before reproducing a route:

```sql
SELECT r.branch_label, a.text FROM annotations a
JOIN papers p ON p.id = a.paper_id LEFT JOIN synthesis_routes r ON r.id = a.route_id
WHERE p.pmcid = 'PMC0000000' AND a.type = 'limite_reproductibilite';
```

Human-readable sheets for each paper are in `fiches/`, and branch graphs in `graphes/`.

## Repository map

| Path | Content |
|---|---|
| `synthese.db` | the database |
| `extractions/` | one JSON per paper, the source of truth for the database |
| `critiques/` | fidelity and science critiques per paper |
| `journaux/` | short decision logs written by each agent |
| `audits/` | batch audit reports, token costs, sources to verify |
| `RUNBOOK.md`, `CRITIQUE.md`, `PLAUSIBILITE.md` | protocols given to the agents |
| `load.py`, `audit.py`, `critic_load.py` | automatic checks and loading |

## Full methodology

The complete method, written as a "Materials and Methods" section with all measurements, limits and threats to validity, is in French: **[README.fr.md](README.fr.md)**.

## Licence and sources

Source articles are open access under Creative Commons licences (CC BY, CC BY-NC, CC BY-NC-ND, CC BY-NC-SA). Some of them are non-commercial or no-derivatives. Each record keeps its paper's licence and URL, and the full text of those articles in `corpus/` remains under its original licence. Reuse of the data must respect each paper's licence.
