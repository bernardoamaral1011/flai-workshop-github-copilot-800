import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;

  useEffect(() => {
    console.log('Leaderboard Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard Component - Raw data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard Component - Processed leaderboard:', leaderboardData);
        
        setLeaderboard(leaderboardData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return <div className="loading-spinner"><div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="error-message"><strong>Error:</strong> {error}</div>;

  return (
    <div className="main-content">
      <h2 className="page-header">🏆 Leaderboard</h2>
      <div className="table-wrapper">
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th className="text-center">Rank</th>
                <th>User</th>
                <th>Team</th>
                <th className="text-center">Total Points</th>
                <th>Type</th>
                <th>Last Updated</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => (
                <tr key={entry.id}>
                  <td className="text-center">
                    {index < 3 ? (
                      <span className="rank-badge">{entry.rank}</span>
                    ) : (
                      <strong>{entry.rank}</strong>
                    )}
                  </td>
                  <td><strong>{entry.name || 'N/A'}</strong></td>
                  <td>
                    {entry.team ? (
                      <span className="badge bg-info">{entry.team}</span>
                    ) : (
                      <span className="text-muted">No team</span>
                    )}
                  </td>
                  <td className="text-center">
                    <span className="badge bg-primary stats-badge">{entry.points}</span>
                  </td>
                  <td>
                    <span className={`badge ${entry.type === 'individual' ? 'bg-success' : 'bg-warning'}`}>
                      {entry.type}
                    </span>
                  </td>
                  <td>{new Date(entry.last_updated).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
