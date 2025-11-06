import React from 'react';
import PageShell from '../components/PageShell';
import MetricsCard from '../components/MetricsCard';
import ScoreBar from '../components/ScoreBar';

export default {
  title: 'Layout/PageShell',
  component: PageShell,
  parameters: { layout: 'fullscreen' }
};

const Template = (args) => <PageShell {...args} />;

export const OverviewExample = Template.bind({});
OverviewExample.args = {
  title: 'Project Overview',
  children: (
    <>
      <div style={{display:'grid', gap:'1rem', gridTemplateColumns:'repeat(auto-fit,minmax(180px,1fr))'}}>
        <MetricsCard title="Teams" value={12} description="Active" />
        <MetricsCard title="Facts" value={45} description="Canonical" />
        <MetricsCard title="Compression" value="64.3%" tone="success" description="Target ≥60%" />
        <MetricsCard title="Quiz Accuracy" value="100%" tone="success" />
      </div>
      <ScoreBar label="Confidence Coverage" value={92} />
    </>
  )
};
