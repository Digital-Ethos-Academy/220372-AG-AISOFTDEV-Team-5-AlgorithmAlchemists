import React from 'react';
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import PageShell from '../../components/PageShell';

expect.extend(toHaveNoViolations);

describe('Accessibility baseline', () => {
  it('PageShell has no obvious a11y violations', async () => {
    const { container } = render(<PageShell title="Overview" />);
    const results = await axe(container, { rules: { 'color-contrast': { enabled: true } } });
    expect(results).toHaveNoViolations();
  });
});
