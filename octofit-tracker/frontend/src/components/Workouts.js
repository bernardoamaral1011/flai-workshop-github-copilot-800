import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts Component - Raw data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts Component - Processed workouts:', workoutsData);
        
        setWorkouts(workoutsData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return <div className="loading-spinner"><div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="error-message"><strong>Error:</strong> {error}</div>;

  return (
    <div className="main-content">
      <h2 className="page-header">💪 Personalized Workouts</h2>
      <div className="row">
        {workouts.map((workout) => (
          <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">{workout.name}</h5>
                <p className="card-text text-muted mb-3">{workout.description}</p>
                <div className="mb-2">
                  <span className="badge bg-secondary me-2">📂 {workout.category || 'General'}</span>
                  <span className={`badge ${workout.difficulty === 'Easy' ? 'bg-success' : workout.difficulty === 'Medium' ? 'bg-warning' : 'bg-danger'}`}>
                    {workout.difficulty}
                  </span>
                </div>
                <hr />
                <div className="d-flex justify-content-between">
                  <div>
                    <small className="text-muted">Duration</small>
                    <div><strong>{workout.duration} min</strong></div>
                  </div>
                  <div>
                    <small className="text-muted">Exercises</small>
                    <div><strong>{workout.exercises && Array.isArray(workout.exercises) ? workout.exercises.length : 0}</strong></div>
                  </div>
                </div>
              </div>
              <div className="card-footer bg-transparent border-top-0">
                <button className="btn btn-primary btn-sm w-100">Start Workout</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Workouts;
