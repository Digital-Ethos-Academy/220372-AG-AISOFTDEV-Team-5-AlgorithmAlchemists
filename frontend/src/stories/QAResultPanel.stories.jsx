import React from 'react';
import QAResultPanel from '../components/QAResultPanel';

export default { title: 'Components/QAResultPanel', component: QAResultPanel };

const Template = (args) => <div style={{padding:'2rem', maxWidth:700}}><QAResultPanel {...args} /></div>;

export const HighConfidence = Template.bind({});
HighConfidence.args = { state: { question: 'Who owns SSO integration?', answer: 'Identity & Access Team', confidence: 0.93 } };

export const LowConfidenceFallback = Template.bind({});
LowConfidenceFallback.args = { state: { question: 'What is the SLA for third-party risk intake?', answer: 'Not found in canonical facts.', confidence: 0.42, fallback: { escalation_action: 'Consult Mentor' } } };

export const EscalatedNoAnswer = Template.bind({});
EscalatedNoAnswer.args = { state: { question: 'Which policy defines data residency guarantees?', answer: '—', confidence: 0.38, fallback: { escalation_action: 'Escalate to Governance Lead' } } };
