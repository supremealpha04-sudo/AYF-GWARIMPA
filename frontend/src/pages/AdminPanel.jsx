import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, Shield, Calendar, FileText, Mail, CheckCircle, XCircle, Plus } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import toast from 'react-hot-toast';

const AdminPanel = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('users');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showRoleModal, setShowRoleModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [newRole, setNewRole] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await api.get('/admin/users');
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
      toast.error('Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleRoleChange = async () => {
    if (!selectedUser || !newRole) return;

    try {
      await api.put(`/admin/users/${selectedUser.id}/role`, { role: newRole });
      toast.success(`Role updated to ${newRole}`);
      fetchUsers();
      setShowRoleModal(false);
      setSelectedUser(null);
      setNewRole('');
    } catch (error) {
      toast.error('Failed to update role');
    }
  };

  const handleActivateUser = async (userId, currentStatus) => {
    try {
      await api.put(`/admin/users/${userId}/activate`);
      toast.success(`User ${currentStatus ? 'deactivated' : 'activated'}`);
      fetchUsers();
    } catch (error) {
      toast.error('Failed to update user status');
    }
  };

  const RoleBadge = ({ role }) => {
    const colors = {
      admin: 'bg-red-100 text-red-700',
      gen_president: 'bg-purple-100 text-purple-700',
      gen_sec: 'bg-blue-100 text-blue-700',
      parish_president: 'bg-gold-100 text-gold-700',
      parish_sec: 'bg-green-100 text-green-700',
      provost: 'bg-indigo-100 text-indigo-700',
      pro: 'bg-pink-100 text-pink-700',
      vice_president: 'bg-orange-100 text-orange-700',
      member: 'bg-gray-100 text-gray-700'
    };
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[role] || 'bg-gray-100 text-gray-700'}`}>
        {role?.replace('_', ' ').toUpperCase()}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <h1 className="text-2xl font-bold text-gray-800">Admin Panel</h1>
        <p className="text-gray-600 mt-1">Manage users, events, and platform settings</p>
      </motion.div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-gray-200">
        {['users', 'events', 'analytics'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === tab
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Users Tab */}
      {activeTab === 'users' && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-card overflow-hidden"
        >
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Parish</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-white text-xs font-bold">
                          {user.full_name?.charAt(0)}
                        </div>
                        <span className="font-medium text-gray-900">{user.full_name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">{user.email}</td>
                    <td className="px-6 py-4 text-sm text-gray-600">{user.parish?.name || 'N/A'}</td>
                    <td className="px-6 py-4">
                      <RoleBadge role={user.role} />
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center gap-1 text-sm ${user.is_active ? 'text-green-600' : 'text-red-600'}`}>
                        {user.is_active ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
                        {user.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex gap-2">
                        <button
                          onClick={() => {
                            setSelectedUser(user);
                            setShowRoleModal(true);
                          }}
                          className="text-blue-600 hover:text-blue-800 text-sm"
                        >
                          Change Role
                        </button>
                        <button
                          onClick={() => handleActivateUser(user.id, user.is_active)}
                          className={`text-sm ${user.is_active ? 'text-red-600 hover:text-red-800' : 'text-green-600 hover:text-green-800'}`}
                        >
                          {user.is_active ? 'Deactivate' : 'Activate'}
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}

      {/* Role Change Modal */}
      {showRoleModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Change Role</h2>
            <p className="text-gray-600 mb-4">User: <strong>{selectedUser?.full_name}</strong></p>
            <select
              value={newRole}
              onChange={(e) => setNewRole(e.target.value)}
              className="input-field mb-4"
            >
              <option value="">Select role...</option>
              <option value="admin">Admin</option>
              <option value="gen_president">Gen President</option>
              <option value="gen_sec">Gen Secretary</option>
              <option value="parish_president">Parish President</option>
              <option value="parish_sec">Parish Secretary</option>
              <option value="provost">Provost</option>
              <option value="pro">PRO</option>
              <option value="vice_president">Vice President</option>
              <option value="member">Member</option>
            </select>
            <div className="flex gap-3">
              <button onClick={handleRoleChange} className="btn-primary flex-1">Update</button>
              <button onClick={() => setShowRoleModal(false)} className="btn-outline flex-1">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;
