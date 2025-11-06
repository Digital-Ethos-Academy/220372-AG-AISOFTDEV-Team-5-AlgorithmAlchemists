import React from 'react';
import { Routes, Route } from 'react-router-dom';
import OverviewPage from './pages/OverviewPage';
import OrgPage from './pages/OrgPage';
import RolesPage from './pages/RolesPage';
import QuizPage from './pages/QuizPage';
import RecommendationPage from './pages/RecommendationPage';
import MetricsPage from './pages/MetricsPage';
import RuntimeMetricsPage from './pages/RuntimeMetricsPage';
import NavBar from './components/NavBar';
import PageShell from './components/PageShell';

export default function App(){
  return (
    <div className="app dark-theme">
      <NavBar />
      <main aria-label="Main content">
        <Routes>
          <Route path="/" element={<PageShell title="Overview"><OverviewPage/></PageShell>} />
          <Route path="/org" element={<PageShell title="Org Explorer"><OrgPage/></PageShell>} />
          <Route path="/roles" element={<PageShell title="Roles Lookup"><RolesPage/></PageShell>} />
          <Route path="/quiz" element={<PageShell title="Quiz"><QuizPage/></PageShell>} />
          <Route path="/recommendation" element={<PageShell title="Recommendation"><RecommendationPage/></PageShell>} />
          <Route path="/metrics" element={<PageShell title="Metrics"><MetricsPage/></PageShell>} />
          <Route path="/runtime" element={<PageShell title="Runtime Metrics"><RuntimeMetricsPage/></PageShell>} />
        </Routes>
      </main>
    </div>
  );
}
