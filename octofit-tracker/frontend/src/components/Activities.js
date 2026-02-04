import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

  useEffect(() => {
    console.log('Activities Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities Component - Raw data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Activities Component - Processed activities:', activitiesData);
        
        setActivities(activitiesData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Activities Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return <div className="loading-spinner"><div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="error-message"><strong>Error:</strong> {error}</div>;

  return (
    <div className="main-content">
      <h2 className="page-header">📊 Activities</h2>
      <div className="table-wrapper">
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>User</th>
                <th>Activity Type</th>
                <th className="text-center">Duration (min)</th>
                <th className="text-center">Distance (km)</th>
                <th className="text-center">Calories</th>
                <th className="text-center">Points</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((activity) => (
                <tr key={activity.id}>
                  <td><strong>{activity.user_name || 'N/A'}</strong></td>
                  <td><span className="badge bg-secondary">{activity.activity_type}</span></td>
                  <td className="text-center">{activity.duration}</td>
                  <td className="text-center">{activity.distance || 'N/A'}</td>
                  <td className="text-center">{activity.calories}</td>
                  <td className="text-center">
                    <span className="badge bg-primary stats-badge">{activity.points}</span>
                  </td>
                  <td>{new Date(activity.date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Activities;
