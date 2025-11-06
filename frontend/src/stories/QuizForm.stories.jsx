import React from 'react';
import QuizForm from '../components/QuizForm';

export default { title: 'Components/QuizForm', component: QuizForm };

export const LoadingState = () => <div style={{padding:'2rem'}}>Loading simulated (no interception)</div>;

// Static perfect score representation (avoids network + internal state complexity for screenshots)
export const PerfectScoreStatic = () => (
	<div style={{padding:'2rem', maxWidth:600}}>
		<div className="quiz-form" aria-label="Canonical quiz form">
			<div className="quiz-result" aria-live="polite">
				<p className="score">Score: 3/3</p>
				<p className="perfect" role="status">Perfect Score ✓</p>
			</div>
		</div>
	</div>
);

// Static unanswered required example
export const ValidationHints = () => (
	<div style={{padding:'2rem', maxWidth:600}}>
		<div className="quiz-form" aria-label="Canonical quiz form">
			<div className="quiz-q">
				<label htmlFor="q-q1">What team owns SSO?</label>
				<input id="q-q1" value="" readOnly aria-required="true" />
				<span className="q-hint" role="note">Required</span>
			</div>
			<div className="quiz-actions">
				<button className="btn" disabled aria-label="Submit quiz">Submit</button>
			</div>
		</div>
	</div>
);

// For isolated visual snapshot we mock with static questions by overriding fetch logic if needed in future.
