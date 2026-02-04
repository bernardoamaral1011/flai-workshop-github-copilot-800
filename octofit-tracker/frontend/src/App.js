import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Users from './components/Users';
import Teams from './components/Teams';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation Bar */}
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img src="/octofitapp-small.png" alt="OctoFit Logo" className="navbar-logo" />
              OctoFit Tracker
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <div className="container-fluid">
          <Routes>
            <Route path="/" element={
              <div className="welcome-section">
                <h1>🏋️ Welcome to OctoFit Tracker</h1>
                <p className="lead">Track your fitness activities, compete with teams, and reach your goals!</p>
                <div className="mt-4">
                  <Link to="/leaderboard" className="btn btn-primary btn-lg me-2 mb-2">🏆 View Leaderboard</Link>
                  <Link to="/activities" className="btn btn-secondary btn-lg mb-2">📊 Track Activities</Link>
                </div>
                <hr className="my-4" />
                <div className="row mt-4">
                  <div className="col-md-4 mb-3">
                    <Link to="/users" className="text-decoration-none">
                      <div className="card text-center clickable-card">
                        <div className="card-body">
                          <h5 className="card-title">👥 Users</h5>
                          <p className="card-text">View all registered users and their stats</p>
                          <span className="btn btn-sm btn-primary">Browse Users</span>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-4 mb-3">
                    <Link to="/teams" className="text-decoration-none">
                      <div className="card text-center clickable-card">
                        <div className="card-body">
                          <h5 className="card-title">🤝 Teams</h5>
                          <p className="card-text">Check out teams and their performance</p>
                          <span className="btn btn-sm btn-primary">View Teams</span>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-4 mb-3">
                    <Link to="/leaderboard" className="text-decoration-none">
                      <div className="card text-center clickable-card">
                        <div className="card-body">
                          <h5 className="card-title">🏆 Leaderboard</h5>
                          <p className="card-text">See who's leading the fitness race</p>
                          <span className="btn btn-sm btn-primary">View Rankings</span>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            } />
            <Route path="/users" element={<Users />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/workouts" element={<Workouts />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
