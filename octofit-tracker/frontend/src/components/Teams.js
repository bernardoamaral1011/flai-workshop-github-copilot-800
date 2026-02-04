import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Teams Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams Component - Raw data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams Component - Processed teams:', teamsData);
        
        setTeams(teamsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return <div className="loading-spinner"><div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="error-message"><strong>Error:</strong> {error}</div>;

  return (
    <div className="main-content">
      <h2 className="page-header">🤝 Teams</h2>
      <div className="table-wrapper">
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Team Name</th>
                <th>Description</th>
                <th className="text-center">Members</th>
                <th className="text-center">Total Points</th>
                <th>Created Date</th>
              </tr>
            </thead>
            <tbody>
              {teams.map((team) => (
                <tr key={team.id}>
                  <td><strong>{team.name}</strong></td>
                  <td>{team.description}</td>
                  <td className="text-center">
                    <span className="badge bg-info stats-badge">
                      {team.members && Array.isArray(team.members) ? team.members.length : 0}
                    </span>
                  </td>
                  <td className="text-center">
                    <span className="badge bg-success stats-badge">{team.total_points}</span>
                  </td>
                  <td>{new Date(team.created_date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Teams;
