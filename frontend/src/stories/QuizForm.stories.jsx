import React from 'react';
import QuizForm from '../components/QuizForm';

export default { title: 'Components/QuizForm', component: QuizForm };

export const LoadingState = () => <div style={{padding:'2rem'}}>Loading simulated (no interception)</div>;

// For isolated visual snapshot we mock with static questions by overriding fetch logic if needed in future.
