import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Phone, MapPin, Calendar, Edit2, Save, X, Camera } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState(null);
  const [parishMembers, setParishMembers] = useState([]);
  const [editForm, setEditForm] = useState({
    full_name: '',
    phone: '',
    avatar_url: ''
  });

  useEffect(() => {
    fetchProfile();
    fetchParishMembers();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await api.get('/profile/me');
      setProfile(response.data);
      setEditForm({
        full_name: response.data.full_name || '',
        phone: response.data.phone || '',
        avatar_url: response.data.avatar_url || ''
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
      toast.error('Failed to load profile');
    }
  };

  const fetchParishMembers = async () => {
    try {
      const response = await api.get('/profile/parish-members');
      setParishMembers(response.data);
    } catch (error) {
      console.error('Error fetching members:', error);
    }
  };

  const handleUpdateProfile = async () => {
    try {
      const response = await api.put('/profile/me', editForm);
      setProfile(response.data);
      updateUser(response.data);
      setIsEditing(false);
      toast.success('Profile updated successfully');
    } catch (error) {
      toast.error('Failed to update profile');
    }
  };

  const handleAvatarUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/profile/me/avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setEditForm({ ...editForm, avatar_url: response.data.avatar_url });
      toast.success('Avatar updated');
    } catch (error) {
      toast.error('Failed to upload avatar');
    }
  };

  if (!profile) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Profile Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex flex-col md:flex-row items-center gap-6">
          {/* Avatar */}
          <div className="relative">
            <div className="w-32 h-32 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-white text-4xl font-bold overflow-hidden">
              {editForm.avatar_url ? (
                <img src={editForm.avatar_url} alt="Avatar" className="w-full h-full object-cover" />
              ) : (
                profile.full_name?.charAt(0) || 'U'
              )}
            </div>
            {isEditing && (
              <label className="absolute bottom-0 right-0 bg-blue-600 p-2 rounded-full cursor-pointer hover:bg-blue-700 transition-colors">
                <Camera className="w-4 h-4 text-white" />
                <input type="file" accept="image/*" onChange={handleAvatarUpload} className="hidden" />
              </label>
            )}
          </div>

          {/* Info */}
          <div className="flex-1 text-center md:text-left">
            {isEditing ? (
              <input
                type="text"
                value={editForm.full_name}
                onChange={(e) => setEditForm({ ...editForm, full_name: e.target.value })}
                className="text-2xl font-bold text-gray-800 input-field mb-2"
              />
            ) : (
              <h1 className="text-2xl font-bold text-gray-800">{profile.full_name}</h1>
            )}
            <p className="text-gray-600">{profile.role?.replace('_', ' ').toUpperCase()}</p>
            <p className="text-sm text-gray-500 mt-1">{profile.parish?.name}</p>
          </div>

          {/* Edit Button */}
          <div>
            {isEditing ? (
              <div className="flex gap-2">
                <button onClick={handleUpdateProfile} className="btn-primary p-2">
                  <Save className="w-5 h-5" />
                </button>
                <button onClick={() => setIsEditing(false)} className="btn-outline p-2">
                  <X className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <button onClick={() => setIsEditing(true)} className="btn-outline flex items-center gap-2">
                <Edit2 className="w-4 h-4" />
                Edit Profile
              </button>
            )}
          </div>
        </div>
      </motion.div>

      {/* Profile Details */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6"
      >
        <h2 className="text-xl font-bold text-gray-800 mb-4">Personal Information</h2>
        <div className="space-y-4">
          <div className="flex items-center gap-3 text-gray-700">
            <Mail className="w-5 h-5 text-gray-400" />
            <span>{profile.email}</span>
          </div>
          <div className="flex items-center gap-3 text-gray-700">
            <Phone className="w-5 h-5 text-gray-400" />
            {isEditing ? (
              <input
                type="tel"
                value={editForm.phone}
                onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
                className="input-field py-2"
                placeholder="Phone number"
              />
            ) : (
              <span>{profile.phone || 'Not provided'}</span>
            )}
          </div>
          <div className="flex items-center gap-3 text-gray-700">
            <Calendar className="w-5 h-5 text-gray-400" />
            <span>Joined {format(new Date(profile.created_at), 'MMMM dd, yyyy')}</span>
          </div>
        </div>
      </motion.div>

      {/* Parish Members */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="glass-card p-6"
      >
        <h2 className="text-xl font-bold text-gray-800 mb-4">Parish Members ({parishMembers.length})</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {parishMembers.map((member) => (
            <div key={member.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-white font-bold">
                {member.full_name?.charAt(0)}
              </div>
              <div className="flex-1">
                <p className="font-semibold text-gray-800">{member.full_name}</p>
                <p className="text-xs text-gray-500">{member.role?.replace('_', ' ')}</p>
              </div>
              {member.last_seen && (
                <p className="text-xs text-gray-400">
                  Last seen {formatDistanceToNow(new Date(member.last_seen), { addSuffix: true })}
                </p>
              )}
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Profile;
