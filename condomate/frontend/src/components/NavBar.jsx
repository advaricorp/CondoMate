import React from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext'; // Import useAuth

function NavBar() {
  const { isAuthenticated, isAdmin, user, logout } = useAuth(); // Use auth state and logout function
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login'); // Redirect to login after logout
  };

  // Use brand colors and slightly larger text
  const activeClassName = "bg-brand-blue-pastel text-brand-gray-dark px-3 py-2 rounded-md text-base font-medium";
  const inactiveClassName = "text-gray-100 hover:bg-brand-gray-light hover:text-brand-gray-dark px-3 py-2 rounded-md text-base font-medium transition-colors duration-150";
  const logoutButtonClassName = "bg-brand-red-light text-brand-gray-dark hover:bg-opacity-80 px-3 py-2 rounded-md text-base font-medium transition-colors duration-150 cursor-pointer"; // Added cursor-pointer

  return (
    <nav className="bg-brand-gray-dark shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to={isAuthenticated ? "/dashboard" : "/login"} className="text-white font-bold text-xl">
              CondoMate
            </Link>
             {/* Optional: Show Condo ID if available */}
             {isAuthenticated && user?.condominium_id && (
               <span className="ml-4 text-xs text-gray-400">(Condo: {user.condominium_id})</span>
             )}
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {isAuthenticated ? (
                <>
                  <NavLink
                    to="/dashboard"
                    className={({ isActive }) => isActive ? activeClassName : inactiveClassName}
                  >
                    Dashboard
                  </NavLink>
                  <NavLink
                    to="/payments"
                    className={({ isActive }) => isActive ? activeClassName : inactiveClassName}
                  >
                    Pagos
                  </NavLink>
                  <NavLink
                    to="/calendar"
                    className={({ isActive }) => isActive ? activeClassName : inactiveClassName}
                  >
                    Calendario
                  </NavLink>
                  <NavLink
                    to="/documents"
                    className={({ isActive }) => isActive ? activeClassName : inactiveClassName}
                  >
                    Documentos
                  </NavLink>
                  {isAdmin && (
                     <NavLink
                       to="/admin"
                       className={({ isActive }) => isActive ? activeClassName : inactiveClassName}
                     >
                       Admin
                     </NavLink>
                  )}
                  <button onClick={handleLogout} className={logoutButtonClassName}>Logout</button>
                </>
              ) : (
                <NavLink
                  to="/login"
                  className={({ isActive }) => isActive ? activeClassName : inactiveClassName}
                >
                  Login
                </NavLink>
              )}
            </div>
          </div>
          {/* Mobile menu button (optional) */}
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
