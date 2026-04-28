import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calendar, MessageCircle, Users, Bell, TrendingUp, FileText, Share2, Clock, Heart, MessageSquare } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import { format, formatDistanceToNow } from 'date-fns';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    upcomingEvents: 0,
    unreadMessages: 0,
    parishMembers: 0,
    notifications: 0
  });
  const [recentEvents, setRecentEvents] = useState([]);
  const [recentFeed, setRecentFeed] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [eventsRes, feedRes, membersRes] = await Promise.all([
        api.get('/calendar/events', { params: { month: new Date().getMonth() + 1, year: new Date().getFullYear() } }),
        api.get('/feed/posts', { params: { limit: 5 } }),
        api.get('/profile/parish-members')
      ]);
      
      setRecentEvents(eventsRes.data.slice(0, 4));
      setRecentFeed(feedRes.data);
      setStats({
        upcomingEvents: eventsRes.data.length,
        unreadMessages: 12,
        parishMembers: membersRes.data?.length || 0,
        notifications: 3
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    { icon: Calendar, label: 'Upcoming Events', value: stats.upcomingEvents, color: 'from-blue-500 to-blue-600', link: '/calendar' },
    { icon: MessageCircle, label: 'Unread Messages', value: stats.unreadMessages, color: 'from-green-500 to-green-600', link: '/chat' },
    { icon: Users, label: 'Parish Members', value: stats.parishMembers, color: 'from-purple-500 to-purple-600', link: '/profile' },
    { icon: Bell, label: 'Notifications', value: stats.notifications, color: 'from-orange-500 to-orange-600', link: '#' }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Welcome Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <h1 className="text-3xl font-bold text-gray-800">
          Welcome back, {user?.full_name?.split(' ')[0]}! 👋
        </h1>
        <p className="text-gray-600 mt-2">
          Stay updated with AYF Gwarimpa Archdeaconry activities
        </p>
        <div className="mt-4 flex gap-2">
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
            user?.role === 'admin' ? 'bg-red-100 text-red-700' :
            user?.role === 'parish_president' ? 'bg-gold-100 text-gold-700' :
            'bg-blue-100 text-blue-700'
          }`}>
            {user?.role?.replace('_', ' ').toUpperCase()}
          </span>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700">
            {user?.parish?.name || 'Loading...'}
          </span>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card, idx) => (
          <Link to={card.link} key={idx}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className={`bg-gradient-to-r ${card.color} rounded-xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 cursor-pointer`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm opacity-90">{card.label}</p>
                  <p className="text-3xl font-bold mt-2">{card.value}</p>
                </div>
                <card.icon className="w-12 h-12 opacity-80" />
              </div>
            </motion.div>
          </Link>
        ))}
      </div>

      {/* Recent Events & Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upcoming Events */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-card p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-800">📅 Upcoming Events</h2>
            <Link to="/calendar" className="text-blue-600 text-sm hover:underline">View all →</Link>
          </div>
          <div className="space-y-3">
            {recentEvents.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No upcoming events</p>
            ) : (
              recentEvents.map((event, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex-1">
                    <p className="font-semibold text-gray-800">{event.display_text || event.title}</p>
                    <div className="flex items-center gap-4 mt-1">
                      <p className="text-sm text-gray-600 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {format(new Date(event.event_date), 'MMM dd, yyyy')}
                      </p>
                      <p className="text-xs text-gray-500">
                        {formatDistanceToNow(new Date(event.event_date), { addSuffix: true })}
                      </p>
                    </div>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                    event.event_level === 'archdeaconry' ? 'bg-blue-100 text-blue-700' :
                    event.event_level === 'diocese' ? 'bg-purple-100 text-purple-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {event.event_level === 'diocese' ? 'DIOCESE' : event.event_level.toUpperCase()}
                  </span>
                </div>
              ))
            )}
          </div>
        </motion.div>

        {/* Recent Feed */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="glass-card p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-800">📰 Recent Announcements</h2>
            <Link to="/feed" className="text-blue-600 text-sm hover:underline">View all →</Link>
          </div>
          <div className="space-y-3">
            {recentFeed.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No posts yet</p>
            ) : (
              recentFeed.map((post, idx) => (
                <div key={idx} className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <p className="font-semibold text-gray-800 line-clamp-2">{post.content.substring(0, 100)}...</p>
                  <div className="flex items-center gap-4 mt-2 text-sm text-gray-600">
                    <span className="flex items-center gap-1">
                      <Heart className="w-4 h-4" /> {post.likes?.[0]?.count || 0}
                    </span>
                    <span className="flex items-center gap-1">
                      <MessageSquare className="w-4 h-4" /> {post.comments?.[0]?.count || 0}
                    </span>
                    <span className="flex items-center gap-1">
                      <Share2 className="w-4 h-4" /> {post.share_count || 0}
                    </span>
                    <span className="text-xs text-gray-400">
                      {formatDistanceToNow(new Date(post.created_at), { addSuffix: true })}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Dashboard;
