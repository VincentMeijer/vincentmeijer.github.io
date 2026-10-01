---
name: paper-figures
description: Make journal-quality scientific figures in matplotlib in a quiet, annotated, colour-blind-safe house style (STIX serif type, Okabe-Ito colours used by meaning, open axes, direct labels instead of legends, light shaded event bands, vector PDF output). Use whenever creating or restyling a figure for a paper, preprint, thesis, poster or talk, when asked to "make this plot look publication-ready", or when recreating published figures.
---

# Paper figures

A matplotlib style plus a short set of rules, derived from the figures in Schwartz &
Johnston (2026), *The Great Oxidation from a minimal ocean–atmosphere model*. The
measurements behind every number here are in `references/analysis.md`.

Why those figures look good: **every mark explains itself where it sits.** Colour has
meaning, text sits next to what it describes and takes its colour, ink is spent on data
rather than frames, and the type matches the page. The style file handles the defaults;
the rules below are what you have to do by hand.

## Setup

```python
import sys; sys.path.insert(0, "<path-to-this-skill>/scripts")
import paperfig as pf
pf.use()                                   # loads scripts/paper.mplstyle
fig, axs = pf.figure("double", height=3.0, nrows=2, sharex=True)
```

`pf.C` is the palette, `pf.WIDTHS` the column widths. Helpers: `note`, `label_line`,
`shade`, `band`, `bound`, `refline`, `halo`, `panel_labels`, `colorbar`, `save`.

## Rules

### 1. Make it at its printed size
Choose the journal width first (`single` 85 mm, `double` 178 mm) and never let LaTeX
rescale it (`\includegraphics` at `width=` equal to the figure width). Text is then
7 pt for labels, 6–6.5 pt for ticks and notes, ~8 pt bold for panel letters. Lines are
1.1 pt for the primary data, 0.5–0.7 pt for everything else. These only look right at
1:1 scale.

### 2. Colour is a vocabulary, not decoration
Use the Okabe–Ito palette and give each colour **one meaning for the whole paper**,
then write that meaning down in the first figure caption or key. In the reference paper:
blue = the model, vermillion = rock-record constraints, orange = prescribed inputs,
green = isotope-derived, pink = literature values, sky blue (light, α≈0.28) = glaciation
intervals, grey = ranges and context. For a typical observation/modelling paper:

| role | colour |
|---|---|
| main result (your model / your retrieval) | `blue` `#0072B2` |
| observations / ground truth / hard bounds | `vermillion` `#D55E00` |
| comparison, baseline, prescribed input | `orange` `#E69F00` |
| third quantity / derived product | `green` `#009E73` |
| literature values | `pink` `#CC79A7` |
| shaded events or regimes | `sky` `#56B4E9` at α 0.2–0.3 |
| ranges, uncertainty, context | `range` `#D9D9D9` fill, `grey` `#6E6E6E` text |

Never rely on colour alone where a second cue is cheap: add a line style (solid model,
dashed threshold, dotted floor/alternative) or a marker shape. Sequential maps: `cividis`,
`viridis`, or a single-hue ramp from the palette colour; diverging: `RdBu_r` centred on 0.

### 3. Label directly; keep legends for symbol types only
Write the name of a curve next to the curve in the curve's colour (`pf.label_line`,
`pf.note`). Where text can't sit beside the mark, use a thin (0.5 pt) leader line in the
same colour (`pf.note(..., xy=target)`). Annotations say *what the reader should see*
("the sawtooth is the four glacial cycles", "fails the paleosol floor"), not just the
name. A legend is acceptable for a set of marker *types* that recur across panels;
then it is one frameless row above the panels.

### 4. Text hierarchy by colour, not by boxes
Primary text `ink` `#222222` (not pure black); secondary explanation `grey` `#6E6E6E`;
annotations of a series in that series' colour. No text boxes, no bold except panel
letters. Use mathtext for symbols and units (`r"$p\mathrm{CO_2}$"`, `r"Tmol C yr$^{-1}$"`),
units in parentheses in the axis label.

### 5. Minimal frame
Left and bottom spines only, ticks out, minor ticks on, no grid (use a few thin
reference lines instead), no background colour. Stacked panels share the x-axis, sit
close (`hspace` small), and only the bottom one carries x tick labels. Reverse an axis
when the field reads that way (geologic age decreasing to the right).

### 6. Show ranges and bounds explicitly
- Uncertainty or published ranges: flat light-grey `band` beneath the data, no edge.
- One-sided limits: triangles pointing the allowed direction (`pf.bound`) or arrows.
- Thresholds: thin dashed `refline` with an inline label at its left end.
- Values off the plot or at a floor: a dotted line along the edge plus a note saying so.
- Events/regimes spanning stacked panels: the same light `shade` bands on every panel,
  labelled once (e.g. "G1…G4") at the top or bottom of one panel.

### 7. Panel letters
Lowercase bold, inside the top-right corner of each panel (`pf.panel_labels`), or
top-left if the data occupy the right. Captions refer to "(a)", "(b)".

### 8. Output
Vector PDF with TrueType fonts embedded (`pdf.fonttype 42`, already set), PNG at 600 dpi
for previews. Rasterize only dense artists (`scatter(..., rasterized=True)` with
>~5 000 points, `imshow`, `pcolormesh`), so text and lines stay vector.

### 9. Maps and imagery
Thin coastlines/borders in `grey` (0.3–0.4 pt), no graticule frame clutter, slim
colourbar without outline (`pf.colorbar`). Labels drawn on imagery get a white `halo`.
Scale bars or lat/lon ticks in 6 pt.

## Checklist before saving
- [ ] Width equals a journal column width; nothing will be rescaled.
- [ ] Every colour has a declared meaning, used consistently across all figures.
- [ ] Each series is identified by text next to it (or a single symbol-key row).
- [ ] Annotations say what to notice, in the colour of what they describe.
- [ ] Ranges, bounds and thresholds are drawn, not just described in the caption.
- [ ] Only left/bottom spines; minor ticks; no grid; no chart junk; no titles inside
      the figure (the caption is the title).
- [ ] Tested in greyscale / for colour-blindness when colour carries the message.
- [ ] Saved as PDF (vector, fonts embedded) and PNG preview.

## Recreating someone's published figure
Prefer the original arrays. If you only have the PDF: vector figures can be recovered
exactly with PyMuPDF (`page.get_drawings()` gives path coordinates; map PDF points to
data using two labelled ticks per axis); raster panels (satellite images, photographs)
can be extracted with `page.get_images()` / `pdfimages` and re-framed with new axes and
annotations. Say in the output which values were recovered from vectors, which were
digitised, and which panels reuse original imagery.
