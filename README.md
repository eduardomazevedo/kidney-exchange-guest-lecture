# Vohra

Project files for the kidney exchange guest lecture.

## Structure

- `presentation/slides.qmd` — Quarto slide deck source
- `presentation/slides.html` — rendered presentation
- `presentation/outline.md` — original slide outline
- `research/deep-research-report.md` — research notes and source summary
- `research/notes.md` — misc notes and links
- `data/kidney_waitlist_flows.csv` — chart data extracted from the report
- `scripts/plot_kidney_waitlist_flows.py` — script that generates the waitlist chart
- `images/` — figures used in the talk

## Commands

Render the presentation:

```bash
quarto render presentation/slides.qmd
```

Rebuild the waitlist chart:

```bash
uv run python scripts/plot_kidney_waitlist_flows.py
```
