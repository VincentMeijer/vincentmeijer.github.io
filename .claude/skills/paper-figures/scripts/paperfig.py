"""Helpers for the paper-figures style (see ../SKILL.md).

    import sys; sys.path.insert(0, "<skill>/scripts")
    import paperfig as pf
    pf.use()
    fig, axs = pf.figure("double", height=3.2, nrows=2, sharex=True)
    ...
    pf.panel_labels(axs)
    pf.save(fig, "fig3")          # writes fig3.pdf + fig3.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects

STYLE = Path(__file__).with_name("paper.mplstyle")

# Okabe-Ito, plus the two neutrals the reference paper uses for text.
C = dict(
    blue="#0072B2",       # the model / primary result
    vermillion="#D55E00", # observations, hard constraints, bounds
    orange="#E69F00",     # prescribed inputs, secondary observations
    green="#009E73",      # third series / derived quantity
    pink="#CC79A7",       # fourth series / literature values
    sky="#56B4E9",        # shaded intervals (events, regimes)
    yellow="#F0E442",     # use sparingly: poor contrast on white
    ink="#222222",        # primary text, axes
    grey="#6E6E6E",       # secondary annotations, reference lines
    range="#D9D9D9",      # published / uncertainty ranges (fill)
    rangeline="#BCBCBC",  # range edges, faint guides
    paper="#FFFFFF",
)
CYCLE = [C[k] for k in ("blue", "vermillion", "orange", "green", "pink", "sky")]

# Journal column widths in inches (final printed size).
WIDTHS = dict(
    single=3.35,      # 85 mm: AGU / Copernicus / IOP single column
    onehalf=4.9,      # 125 mm
    double=7.0,       # 178 mm: IOP (ERL), AGU, Elsevier full width
    copernicus2=6.89, # 175 mm: Copernicus (ACP, AMT, GMD, ...) full width
)


def use(**overrides):
    """Activate the style. Keyword overrides go to rcParams."""
    plt.style.use(str(STYLE))
    if overrides:
        mpl.rcParams.update(overrides)


def figure(width="double", height=None, nrows=1, ncols=1, aspect=0.62, **kw):
    """Figure at final print size. width: key of WIDTHS or inches."""
    w = WIDTHS.get(width, width) if isinstance(width, str) else width
    h = height if height is not None else w * aspect * nrows / max(ncols, 1) ** 0.5
    kw.setdefault("constrained_layout", True)
    fig, axs = plt.subplots(nrows, ncols, figsize=(w, h), **kw)
    if kw.get("constrained_layout"):
        fig.get_layout_engine().set(w_pad=0.02, h_pad=0.02, hspace=0.04, wspace=0.04)
    return fig, axs


def panel_labels(axs, loc="upper right", start="a", dx=0.0, dy=0.0, **kw):
    """Bold lowercase panel letters inside the axes corner (reference style)."""
    axs = np.atleast_1d(axs).ravel()
    x, ha = (1.0, "right") if "right" in loc else (0.0, "left")
    y, va = (1.0, "top") if "upper" in loc else (0.0, "bottom")
    style = dict(fontweight="bold", fontsize=mpl.rcParams["font.size"] + 1, color=C["ink"])
    style.update(kw)
    for i, ax in enumerate(axs):
        ax.text(x + dx, y + dy, chr(ord(start) + i), transform=ax.transAxes,
                ha=ha, va=va, **style)


def note(ax, x, y, text, color=None, xy=None, ha="left", va="center",
         coords="data", xycoords=None, lw=0.5, **kw):
    """Direct label in the series colour, optionally with a thin leader line to xy.

    This replaces most legends: say what a mark is, next to the mark.
    coords: "data" or "axes" for the text position; xycoords likewise for the
    leader target (defaults to coords).
    """
    color = color or C["ink"]

    def _tf(c):  # "data" | "axes" | any Transform (e.g. ccrs.PlateCarree()._as_mpl_transform(ax))
        return ax.transAxes if c == "axes" else ax.transData if c == "data" else c

    kw.setdefault("fontsize", mpl.rcParams["font.size"] - 0.5)
    if xy is None:
        return ax.text(x, y, text, color=color, ha=ha, va=va, transform=_tf(coords), **kw)
    xyc = xycoords or coords
    return ax.annotate(text, xy=xy, xytext=(x, y),
                       xycoords=_tf(xyc), textcoords=_tf(coords),
                       color=color, ha=ha, va=va,
                       arrowprops=dict(arrowstyle="-", color=color, lw=lw,
                                       shrinkA=1, shrinkB=1.5), **kw)


def label_line(ax, line, x, text=None, dy=0.0, ha="left", va="bottom", **kw):
    """Write a label on/next to a Line2D at data x, in the line's colour."""
    xd, yd = line.get_data()
    y = np.interp(x, xd, yd) if xd[0] < xd[-1] else np.interp(x, xd[::-1], yd[::-1])
    return note(ax, x, y + dy, text or line.get_label(), color=line.get_color(),
                ha=ha, va=va, **kw)


def shade(ax, intervals, color=None, alpha=0.28, labels=None,
          label_y=0.98, label_color=None, **kw):
    """Light vertical bands marking events/regimes; draws beneath data.

    Repeat on every stacked panel so the bands read as one through the figure.
    """
    color = color or C["sky"]
    for i, (a, b) in enumerate(intervals):
        ax.axvspan(a, b, color=color, alpha=alpha, lw=0, zorder=0)
        if labels:
            ax.text((a + b) / 2, label_y, labels[i], transform=ax.get_xaxis_transform(),
                    ha="center", va="top", color=label_color or C["grey"], fontsize=mpl.rcParams["font.size"] - 1)


def hband(ax, lo, hi, color=None, alpha=0.28, **kw):
    """Horizontal shaded band (e.g. a flight-level range or regime in y)."""
    return ax.axhspan(lo, hi, color=color or C["sky"], alpha=alpha, lw=0, zorder=0, **kw)


def scalebar(ax, length, label, loc=(0.95, 0.06), color="white", lw=1.5, **kw):
    """Scale bar for imagery in data units; loc = right end in axes fraction."""
    x1 = ax.transData.inverted().transform(ax.transAxes.transform(loc))
    x0 = x1[0] - length
    ax.plot([x0, x1[0]], [x1[1]] * 2, color=color, lw=lw, solid_capstyle="butt", zorder=5)
    t = ax.text((x0 + x1[0]) / 2, x1[1], label, color=color, ha="center", va="bottom",
                fontsize=mpl.rcParams["font.size"] - 1, zorder=5, **kw)
    return halo(t, color="#222222" if color == "white" else "white")


def band(ax, x, lo, hi, color=None, alpha=1.0, **kw):
    """Range/uncertainty band: flat light grey by default, no edge."""
    return ax.fill_between(x, lo, hi, color=color or C["range"], alpha=alpha, lw=0,
                           zorder=kw.pop("zorder", 0.5), **kw)


def bound(ax, x, y, direction="down", color=None, size=3.0, **kw):
    """One-sided bound marker (triangle pointing the allowed way)."""
    m = {"down": "v", "up": "^", "left": "<", "right": ">"}[direction]
    return ax.plot(x, y, m, color=color or C["vermillion"], ms=size, mew=0,
                   ls="none", **kw)


def refline(ax, value, axis="y", color=None, ls="--", lw=0.7, text=None,
            text_pos=0.01, **kw):
    """Thin dashed reference/threshold line with an optional inline label."""
    color = color or C["grey"]
    if axis == "y":
        ax.axhline(value, color=color, ls=ls, lw=lw, zorder=1, **kw)
        if text:
            ax.text(text_pos, value, text, color=color, transform=ax.get_yaxis_transform(),
                    ha="left", va="bottom", fontsize=mpl.rcParams["font.size"] - 1)
    else:
        ax.axvline(value, color=color, ls=ls, lw=lw, zorder=1, **kw)
        if text:
            ax.text(value, 1 - text_pos, text, color=color, transform=ax.get_xaxis_transform(),
                    ha="left", va="top", rotation=90, fontsize=mpl.rcParams["font.size"] - 1)


def halo(artist, width=2.0, color="white"):
    """Outline so text stays legible over data or imagery. White on light
    backgrounds; on dark satellite scenes use white text with color="#222222"."""
    artist.set_path_effects([patheffects.withStroke(linewidth=width, foreground=color)])
    return artist


def legend_row(fig_or_ax, handles, labels, ncol=None, y=1.0, **kw):
    """A single frameless key row above the panels (used only for marker types)."""
    ncol = ncol or len(handles)
    tgt = fig_or_ax
    return tgt.legend(handles, labels, ncol=ncol, loc="lower center",
                      bbox_to_anchor=(0.5, y), frameon=False, **kw)


def despine(ax, left=False, bottom=False):
    """Remove further spines, e.g. for strip/axis-only rows."""
    if left:
        ax.spines["left"].set_visible(False); ax.tick_params(left=False, which="both")
    if bottom:
        ax.spines["bottom"].set_visible(False); ax.tick_params(bottom=False, which="both")


def colorbar(fig, mappable, ax=None, label="", cax=None, side="right",
             width=0.025, pad=0.015, **kw):
    """Slim colourbar, ticks out, no outline box.

    Placed as an inset of `ax` (works with fixed-aspect map axes and any layout),
    or drawn into an explicit `cax`. side: "right" or "bottom".
    """
    if cax is None:
        if side == "right":
            cax = ax.inset_axes([1 + pad, 0, width, 1])
        else:
            cax = ax.inset_axes([0, -pad - width * 3 - 0.08, 1, width * 1.6])
            kw.setdefault("orientation", "horizontal")
    cb = fig.colorbar(mappable, cax=cax, **kw)
    cb.outline.set_visible(False)
    cb.ax.tick_params(width=0.5, length=2, which="major")
    cb.ax.minorticks_off()
    if label:
        cb.set_label(label)
    return cb


def cmap(color, name=None, light="#FFFFFF", n=256):
    """Single-hue sequential colormap from white (or `light`) to a palette colour."""
    from matplotlib.colors import LinearSegmentedColormap
    c = C.get(color, color)
    return LinearSegmentedColormap.from_list(name or f"to_{color}", [light, c], N=n)


def twin(ax, color):
    """Secondary y-axis for a second quantity. Its spine, ticks and label take the
    series colour so the pairing is unambiguous; use only when the two series share
    x and their relation is the point (e.g. coverage vs. traffic)."""
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(color)
    ax2.tick_params(axis="y", colors=color, which="both")
    ax2.yaxis.label.set_color(color)
    return ax2


def save(fig, stem, formats=("pdf", "png"), **kw):
    """Save vector PDF (journal) + PNG preview at the exact figure size (no tight
    bbox, so the printed width stays the journal width). Rasterize dense artists via
    artist.set_rasterized(True) before calling."""
    for f in formats:
        fig.savefig(f"{stem}.{f}", **kw)
    return [f"{stem}.{f}" for f in formats]
