import React from 'react';
import RolesSearchPanel from '../components/RolesSearchPanel';

export default { title: 'Components/RolesSearchPanel', component: RolesSearchPanel };

export const EmptyInitial = () => <div style={{padding:'2rem', maxWidth:700}}><RolesSearchPanel /></div>;

const sampleResults = [
	{ id: 'role-1', name: 'Senior Data Engineer', match: 92, gaps: ['LLM orchestration'], needs: ['Vector DB expertise'] },
	{ id: 'role-2', name: 'AI Product Manager', match: 81, gaps: ['Prompt eval framework'], needs: ['Hallucination metrics'] }
];

export const WithResults = () => (
	<div style={{padding:'2rem', maxWidth:700}}>
		<RolesSearchPanel initialQuery="ai" initialResults={sampleResults} />
	</div>
);

export const NoResults = () => (
	<div style={{padding:'2rem', maxWidth:700}}>
		<RolesSearchPanel initialQuery="quantum" initialResults={[]} />
	</div>
);

// Static visual variants allow Playwright screenshot capture without backend dependency.
