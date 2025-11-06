import React from 'react';
import { NavLink } from 'react-router-dom';
import './navbar.css';

const links = [
  { to: '/', label: 'Overview' },
  { to: '/org', label: 'Org' },
  { to: '/roles', label: 'Roles' },
  { to: '/quiz', label: 'Quiz' },
  { to: '/qa', label: 'Q&A' },
  { to: '/recommendation', label: 'Recommendation' },
  { to: '/metrics', label: 'Metrics' },
  { to: '/runtime', label: 'Runtime' }
];

export function NavBar(){
  return (
    <nav className="nav-bar" aria-label="Primary navigation">
      <div className="nav-logo" aria-label="Application name">POI Compass</div>
      <ul className="nav-items" role="menubar">
        {links.map(l => (
          <li key={l.to} role="none">
            <NavLink role="menuitem" to={l.to} className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>
              {l.label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
export default NavBar;
