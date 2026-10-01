# What the reference figures are made of

Source: M. D. Schwartz & D. T. Johnston, *The Great Oxidation from a minimal
ocean–atmosphere model* (preprint, 2026), Figs. 1–7. Measured from the PDF with
`pdffonts` and PyMuPDF (`page.get_drawings()`, `page.get_text("dict")`).

## Toolchain
- Paper typeset in pdfTeX (Computer Modern body text).
- Figures are **vector matplotlib PDFs**: text is embedded **STIXGeneral** Regular/Italic/Bold
  (matplotlib's bundled STIX, i.e. `font.family: STIXGeneral`, `mathtext.fontset: stix`).
  Times-like serif type whose math matches the text, so symbols such as ν, pO₂, t× look
  the same in figure and caption.
- Only one raster object in the whole paper (the 1 689-point scatter in Fig. 4a,
  rasterized at ~170 dpi with an alpha mask); everything else is vector.

## Colour (stroke/fill counts per page)
Okabe–Ito throughout: `#0072B2` blue, `#D55E00` vermillion, `#E69F00` orange,
`#009E73` green, `#CC79A7` pink, `#56B4E9` sky blue. Neutrals: text `#222222`,
secondary text `#6E6E6E`, ranges `#BCBCBC`/`#CFCFCF`/`#DDDDDD`/`#E3E3E3`, plus
brown `#6B4F35`/`#8B6C4F` for one extra category in the schematic.
Meanings are fixed across the paper: blue = model, vermillion = rock-record bounds,
orange = prescribed, green = isotope/carbon, pink = published value at a stated
position, sky blue α 0.28 = model glaciations (same bands on every age axis).
Text annotations are coloured like the series they describe (text colour counts on
Fig. 3 page: #222222 ×41, #D55E00 ×32, #0072B2 ×19).

## Line weights (pt at printed size)
- Primary model curves ≈ 1.07–1.16
- Axes spines/ticks ≈ 0.7–0.8; minor ticks ≈ 0.45–0.55
- Leader lines, range edges, error bars ≈ 0.35–0.55
- Range bars in Fig. 2 drawn as 4.3 pt thick light-grey lines (`#BCBCBC`, `#CFCFCF`)
- Dashes: ≈ [3.3, 1.4] dashed, [0.7, 1.2] dotted, [4.5, 1.1, 0.7, 1.1] dash-dot

## Type sizes (as printed; figures inserted at ~1:1)
Tick labels ≈ 6–7 pt, axis labels 7–8 pt, annotations 5–6 pt, symbol-key 5 pt,
panel letters bold ≈ 8 pt. Hierarchy comes from colour and size, never from boxes.

## Layout habits
- Open axes (left + bottom), ticks outward, minor ticks on, no grids.
- Stacked panels with a shared, reversed age axis and tight spacing.
- Panel letters bold lowercase inside the top-right corner.
- Legends replaced by direct labels with thin leader lines; a single frameless key row
  is used only for marker *types* (★ fixed by record, ◆ prescribed, ■ assumption, ▼
  published range, ● published value, ○ present-day steady state).
- Constraints drawn as one-sided triangles/arrows, ranges as grey bars/bands,
  thresholds as dashed lines with inline labels, floors as dotted lines with a note.
- Annotations are full sentences about what to see ("the sawtooth is the four glacial
  cycles", "level set by two input schedules (fails the paleosol floor)").
- Magnified insets for narrow intervals (Fig. 2 ν strip, Fig. 6 insets).

## Why it works
1. One meaning per colour, consistent across seven figures → the reader learns the
   code once.
2. Labels at the data → no eye travel between legend and curve.
3. Low-ink frame + light context (grey ranges, pale bands) → data are the darkest,
   most saturated things on the page.
4. Type and math identical in style to the caption → figure feels part of the text.
5. Colour-blind-safe palette with redundant line styles and markers.
6. Vector output at print size → crisp at any zoom, nothing scaled.
