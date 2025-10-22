import { Outlet, Link } from 'react-router-dom';
import './Layout.css'; // Assuming a CSS file for layout styling

const Layout = () => {
  return (
    <div className="app-layout">
      <header className="app-header">
        <nav className="navbar">
          <Link to="/" className="nav-brand">AI Data Analyst</Link>
          <ul className="nav-links">
            <li><Link to="/">Home</Link></li>
            <li><Link to="/upload">Upload</Link></li>
            <li><Link to="/analyze">Analyze</Link></li>
          </ul>
        </nav>
      </header>
      <main className="app-content">
        <Outlet />
      </main>
      <footer className="app-footer">
        <p>&copy; 2025 AI Data Analyst. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Layout;