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
  { to: '/runtime', label: 'Runtime' },
  { to: '/admin', label: 'Admin' }
];

export function NavBar(){
  const [tenant,setTenant] = React.useState(()=> localStorage.getItem('tenantId') || 'default');
  const changeTenant = (e)=>{
    const val = e.target.value;
    setTenant(val);
    localStorage.setItem('tenantId', val);
    // soft refresh to allow pages to re-fetch with new header
    window.dispatchEvent(new Event('tenant-changed'));
  };
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
      <div style={{marginLeft:'auto', display:'flex', alignItems:'center', gap:'0.5rem'}}>
        <label htmlFor="tenant-select" style={{fontSize:'0.75rem'}}>Tenant</label>
        <select id="tenant-select" value={tenant} onChange={changeTenant} aria-label="Select tenant context">
          <option value="default">default</option>
          <option value="tenantA">tenantA</option>
          <option value="tenantB">tenantB</option>
        </select>
      </div>
    </nav>
  );
}
export default NavBar;
