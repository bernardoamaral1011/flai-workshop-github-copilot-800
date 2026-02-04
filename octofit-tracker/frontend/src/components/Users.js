import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({ name: '', email: '', team: '' });
  const [saveError, setSaveError] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
  const TEAMS_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Users Component - Fetching from:', API_URL);
    
    // Fetch users
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Users Component - Raw data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const usersData = data.results || data;
        console.log('Users Component - Processed users:', usersData);
        
        setUsers(usersData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Users Component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });

    // Fetch teams for dropdown
    fetch(TEAMS_URL)
      .then(response => response.json())
      .then(data => {
        const teamsData = data.results || data;
        setTeams(teamsData);
      })
      .catch(error => {
        console.error('Users Component - Error fetching teams:', error);
      });
  }, [API_URL, TEAMS_URL]);

  const handleEdit = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name,
      email: user.email,
      team: user.team || ''
    });
    setSaveError(null);
    setSaveSuccess(false);
  };

  const handleClose = () => {
    setEditingUser(null);
    setFormData({ name: '', email: '', team: '' });
    setSaveError(null);
    setSaveSuccess(false);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = async () => {
    setSaveError(null);
    setSaveSuccess(false);

    try {
      const response = await fetch(`${API_URL}${editingUser.id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error(`Failed to update user: ${response.status}`);
      }

      const updatedUser = await response.json();
      
      // Update the users list
      setUsers(users.map(u => u.id === editingUser.id ? updatedUser : u));
      setSaveSuccess(true);
      
      // Close modal after 1 second
      setTimeout(() => {
        handleClose();
      }, 1000);
    } catch (error) {
      console.error('Error updating user:', error);
      setSaveError(error.message);
    }
  };

  if (loading) return <div className="loading-spinner"><div className="spinner-border text-primary" role="status"><span className="visually-hidden">Loading...</span></div></div>;
  if (error) return <div className="error-message"><strong>Error:</strong> {error}</div>;

  return (
    <div className="main-content">
      <h2 className="page-header">👥 Users</h2>
      <div className="table-wrapper">
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Team</th>
                <th className="text-center">Total Points</th>
                <th>Joined Date</th>
                <th className="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td><strong>{user.name || 'N/A'}</strong></td>
                  <td>{user.email || 'N/A'}</td>
                  <td>
                    {user.team ? (
                      <span className="badge bg-info">{user.team}</span>
                    ) : (
                      <span className="text-muted">No team</span>
                    )}
                  </td>
                  <td className="text-center">
                    <span className="badge bg-primary stats-badge">{user.total_points}</span>
                  </td>
                  <td>{new Date(user.joined_date).toLocaleDateString()}</td>
                  <td className="text-center">
                    <button 
                      className="btn btn-sm btn-primary"
                      onClick={() => handleEdit(user)}
                    >
                      ✏️ Edit
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Edit User Modal */}
      {editingUser && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit User Details</h5>
                <button type="button" className="btn-close" onClick={handleClose}></button>
              </div>
              <div className="modal-body">
                {saveSuccess && (
                  <div className="alert alert-success">User updated successfully!</div>
                )}
                {saveError && (
                  <div className="alert alert-danger">Error: {saveError}</div>
                )}
                <form>
                  <div className="mb-3">
                    <label htmlFor="name" className="form-label">Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="team" className="form-label">Team</label>
                    <select
                      className="form-select"
                      id="team"
                      name="team"
                      value={formData.team}
                      onChange={handleChange}
                    >
                      <option value="">No Team</option>
                      {teams.map((team) => (
                        <option key={team.id} value={team.name}>
                          {team.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </form>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={handleClose}>
                  Cancel
                </button>
                <button type="button" className="btn btn-primary" onClick={handleSave}>
                  Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
