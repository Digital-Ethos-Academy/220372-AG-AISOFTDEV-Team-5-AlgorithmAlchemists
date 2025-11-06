---
applyTo: "frontend/src/**/*.js,frontend/src/**/*.jsx,frontend/src/**/*.ts,frontend/src/**/*.tsx"
description: "React/TypeScript component, accessibility, and visual regression rules"
---
# React / Frontend Instructions

## Components
- Use functional components only; hooks for state and side-effects.
- Co-locate component CSS; prefer className BEM-like naming.
- No implicit any (for TS code); define interfaces for props & complex data structures.

## Accessibility
- Provide `aria-label` or descriptive text for interactive elements (buttons, links, form inputs).
- Maintain color contrast ≥ 4.5:1; do not rely solely on color for status.
- Skip link must remain functional (`.skip-link`).

## State & Data Fetching
- Implement `useTenant` context when tenant feature added; refetch dependent pages on change.
- Avoid prop drilling beyond two levels; use context.

## Visual Regression
- Snapshot additions require rationale in commit message.
- Update baseline only when intentional layout change or token update.
- Use minimal deterministic mocks; avoid dynamic timestamps in UI during snapshot.

## Testing
- Add accessibility test (`jest-axe` or existing harness) for new components with interactive behavior.
- Visual snapshot tests: limit to canonical pages (overview, metrics, quiz, recommendation, roles).

## Performance
- Re-render triggers: ensure stable dependency arrays for hooks.
- Large lists: prefer windowing if > 200 items (future optimization; not premature now).

## Security
- Never expose internal tokens in client bundle; use env-sourced proxy or backend headers.

## Prohibited
- Direct DOM manipulation (use refs sparingly for focus management only).
- Global mutable singletons for transient UI state (use context/providers).
