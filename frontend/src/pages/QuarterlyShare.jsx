import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Download, Send, Eye, Calendar, FileText, Share2, ChevronRight } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

const QuarterlyShare = () => {
  const { user } = useAuth();
  const [shares, setShares] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedShare, setSelectedShare] = useState(null);

  const isPresident = user?.role === 'parish_president';
  const isAdmin = ['admin', 'gen_president', 'gen_sec'].includes(user?.role);

  useEffect(() => {
    fetchShares();
  }, []);

  const fetchShares = async () => {
    try {
      const response = await api.get('/quarterly/shares');
      setShares(response.data);
    } catch (error) {
      console.error('Error fetching shares:', error);
      toast.error('Failed to load quarterly shares');
    } finally {
      setLoading(false);
    }
  };

  const handleForward = async (shareId) => {
    try {
      await api.post(`/quarterly/share/${shareId}/forward`);
      toast.success('Forwarded to parish group successfully');
      fetchShares();
    } catch (error) {
      toast.error('Failed to forward share');
    }
  };

  const handleDownload = (fileUrl, fileName) => {
    window.open(fileUrl, '_blank');
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
        <h1 className="text-2xl font-bold text-gray-800">Quarterly Shares</h1>
        <p className="text-gray-600 mt-1">
          {isPresident 
            ? "View and forward quarterly allocations to your parish group" 
            : "View quarterly shares forwarded by your parish president"}
        </p>
      </motion.div>

      {/* Shares Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {shares.length === 0 ? (
          <div className="glass-card p-12 text-center col-span-2">
            <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No quarterly shares available</p>
          </div>
        ) : (
          shares.map((share, idx) => (
            <motion.div
              key={share.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="glass-card p-6 hover:shadow-xl transition-all duration-300"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 flex items-center justify-center">
                    <Calendar className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-800 text-lg">{share.title}</h3>
                    <p className="text-sm text-gray-500">Q{share.quarter} {share.year}</p>
                  </div>
                </div>
                {isPresident && !share.forwarded && (
                  <button
                    onClick={() => handleForward(share.id)}
                    className="bg-green-500 text-white p-2 rounded-lg hover:bg-green-600 transition-colors"
                    title="Forward to parish group"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                )}
              </div>

              <p className="text-gray-700 mb-4">{share.description}</p>

              {share.file_url && (
                <button
                  onClick={() => handleDownload(share.file_url, share.file_name)}
                  className="flex items-center gap-2 text-blue-600 hover:text-blue-800 mb-4"
                >
                  <Download className="w-4 h-4" />
                  Download Attachment
                </button>
              )}

              <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <Calendar className="w-4 h-4" />
                  {format(new Date(share.created_at), 'MMMM dd, yyyy')}
                </div>
                {share.forwarded_at && (
                  <div className="flex items-center gap-1 text-sm text-green-600">
                    <Share2 className="w-4 h-4" />
                    Forwarded to parish
                  </div>
                )}
              </div>
            </motion.div>
          ))
        )}
      </div>

      {/* Info Card for Parish Presidents */}
      {isPresident && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-blue-50 border border-blue-200 rounded-xl p-4"
        >
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
              <Eye className="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <h4 className="font-semibold text-blue-800">Parish President Access</h4>
              <p className="text-sm text-blue-700 mt-1">
                As a Parish President, you can view all quarterly shares from the archdeaconry.
                Use the send button to forward any share to your parish group for members to see.
              </p>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default QuarterlyShare;
