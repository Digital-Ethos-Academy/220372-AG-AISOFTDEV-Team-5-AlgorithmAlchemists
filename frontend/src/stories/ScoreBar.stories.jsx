import React from 'react';
import ScoreBar from '../components/ScoreBar';

export default { title: 'Components/ScoreBar', component: ScoreBar };

const Template = (args) => <div style={{padding:'2rem', maxWidth:400}}><ScoreBar {...args} /></div>;

export const High = Template.bind({});
High.args = { label: 'Confidence Coverage', value: 92 };

export const Medium = Template.bind({});
Medium.args = { label: 'Confidence Coverage', value: 68 };

export const Low = Template.bind({});
Low.args = { label: 'Confidence Coverage', value: 40 };
