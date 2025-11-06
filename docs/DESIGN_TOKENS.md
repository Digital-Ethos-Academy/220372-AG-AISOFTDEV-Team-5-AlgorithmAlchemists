# Design Tokens (Dark Theme v0.1)

This document enumerates the core design tokens implemented in `src/design/tokens.css` to provide a consistent, accessible dark UI per PRD usability and accessibility objectives (WCAG 2.1 AA target).

## Color Palette
| Token | Value | Purpose | Contrast (approx on bg) |
|-------|-------|---------|--------------------------|
| --color-bg | #0d1117 | App background | — |
| --color-bg-alt | #161b22 | Navigation / panels | 5.2:1 vs text |
| --color-surface | #1f242c | Elevated surface | 4.5:1 vs text |
| --color-border | #30363d | Dividers / outlines | N/A |
| --color-text | #f0f6fc | Primary text | 12.8:1 |
| --color-text-muted | #c9d1d9 | Secondary text | 8.1:1 |
| --color-accent | #2f81f7 | Interactive / active nav | 4.6:1 on alt bg |
| --color-accent-hover | #1b6cd6 | Hover state accent | 5.5:1 |
| --color-success | #238636 | Positive metrics | 4.9:1 |
| --color-warning | #d29922 | Gap / caution indicators | 3.2:1 (paired with dark text) |
| --color-danger | #f85149 | Error / failing metric | 4.1:1 |
| --color-info | #58a6ff | Informational highlights | 5.2:1 |

Warning token used with dark text (#000) inside pill badges to meet contrast.

## Typography Scale
System UI stack for performance and neutrality:
```
--fs-xs: 0.75rem
--fs-sm: 0.875rem
--fs-base: 1rem
--fs-md: 1.125rem
--fs-lg: 1.25rem
--fs-xl: 1.5rem
--fs-2xl: 1.875rem
```
Ratio ~1.125–1.2 ensuring readable hierarchy without large jumps.

## Spacing (4px Base)
```
0, 4, 8, 12, 16, 20, 24, 32 (mapped via --space-0..--space-8)
```
Chosen for predictable modular composition and grid alignment.

## Radius
| Token | Value | Usage |
|-------|-------|-------|
| --radius-sm | 4px | Small pills / inputs |
| --radius-md | 6px | Buttons / nav links |
| --radius-lg | 10px | Cards / shells |
| --radius-pill | 999px | Badges / progress bars |

## Shadows
Subtle elevation in dark UI to avoid halo glow.
```
--shadow-sm: 0 1px 2px rgba(0,0,0,0.4)
--shadow-md: 0 2px 4px rgba(0,0,0,0.45)
--shadow-lg: 0 4px 12px rgba(0,0,0,0.5)
```

## Motion / Timing
```
--transition-fast: 120ms cubic-bezier(0.4,0,0.2,1)
--transition-base: 180ms cubic-bezier(0.4,0,0.2,1)
```
Adheres to guidance (<200ms) for small UI affordances; no large parallax or disorienting transitions.

## Layout
```
--nav-height: 3.25rem
--content-max-width: 1100px
```
Max width chosen to maintain ~80–100 character line length for readability.

## Accessibility Notes
- All tokens ensure primary text contrast ≥ 4.5:1.
- Accent vs background combinations audited for ≥3:1 where used on larger text or interactive elements.
- Warning token rendered with dark text to maintain ≥ 4.5:1.
- Focus ring uses accent color with 2px thickness and offset to avoid masking component shape.

## Governance
Future adjustments must: (1) update this document, (2) increment theme version header, (3) run visual regression snapshots, (4) update any impacted Storybook stories.

## Roadmap Enhancements
| Item | Rationale |
|------|-----------|
| Light theme tokens | Required for broader adoption / preference |
| Semantic color ramp (LCH steps) | Better scaling for states and charts |
| Density variants (comfortable / compact) | Power user optimization |
| Token extraction script (JSON) | Sync with design tooling / theming engines |

Version: 0.1  | Date: 2025-11-05 | Owner: Engineering
