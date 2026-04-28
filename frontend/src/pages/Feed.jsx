import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Heart, MessageCircle, Share2, Download, Send, MoreVertical, Image as ImageIcon, Video, File, X } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import toast from 'react-hot-toast';
import { formatDistanceToNow } from 'date-fns';

const Feed = () => {
  const { user } = useAuth();
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState({ content: '', post_type: 'announcement' });
  const [showCommentBox, setShowCommentBox] = useState(null);
  const [commentText, setCommentText] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedMedia, setSelectedMedia] = useState(null);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await api.get('/feed/posts');
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching posts:', error);
      toast.error('Failed to load posts');
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = async () => {
    if (!newPost.content.trim()) {
      toast.error('Please enter some content');
      return;
    }

    try {
      await api.post('/feed/posts', newPost);
      toast.success('Post created successfully');
      setNewPost({ content: '', post_type: 'announcement' });
      fetchPosts();
    } catch (error) {
      toast.error('Failed to create post');
    }
  };

  const handleLike = async (postId) => {
    try {
      await api.post(`/feed/posts/${postId}/like`);
      fetchPosts(); // Refresh to update like status
    } catch (error) {
      toast.error('Failed to like post');
    }
  };

  const handleComment = async (postId) => {
    if (!commentText.trim()) return;

    try {
      await api.post(`/feed/posts/${postId}/comment`, { comment: commentText });
      toast.success('Comment added');
      setCommentText('');
      setShowCommentBox(null);
      fetchPosts();
    } catch (error) {
      toast.error('Failed to add comment');
    }
  };

  const handleShare = async (postId) => {
    try {
      await api.post(`/feed/posts/${postId}/share`);
      toast.success('Post shared');
      fetchPosts();
    } catch (error) {
      toast.error('Failed to share');
    }
  };

  const handleDownload = async (mediaUrl) => {
    window.open(mediaUrl, '_blank');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Create Post */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-4"
      >
        <div className="flex gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-white font-bold">
            {user?.full_name?.charAt(0)}
          </div>
          <div className="flex-1">
            <textarea
              placeholder={`What's on your mind, ${user?.full_name?.split(' ')[0]}?`}
              value={newPost.content}
              onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
              className="w-full p-3 rounded-xl border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none resize-none"
              rows="3"
            />
            <div className="flex items-center justify-between mt-3">
              <select
                value={newPost.post_type}
                onChange={(e) => setNewPost({ ...newPost, post_type: e.target.value })}
                className="px-3 py-1 rounded-lg border border-gray-200 text-sm"
              >
                <option value="announcement">📢 Announcement</option>
                <option value="event">🎉 Event</option>
                <option value="notice">📋 Notice</option>
                <option value="testimony">🙏 Testimony</option>
              </select>
              <button onClick={handleCreatePost} className="btn-primary px-6 py-2 text-sm">
                Post
              </button>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Posts Feed */}
      <AnimatePresence>
        {posts.map((post, idx) => (
          <motion.div
            key={post.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ delay: idx * 0.05 }}
            className="glass-card p-4"
          >
            {/* Post Header */}
            <div className="flex items-start justify-between">
              <div className="flex gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-white font-bold">
                  {post.author?.full_name?.charAt(0)}
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800">{post.author?.full_name}</h3>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs text-gray-500">{post.author?.role?.replace('_', ' ')}</span>
                    <span className="text-xs text-gray-400">•</span>
                    <span className="text-xs text-gray-500">{formatDistanceToNow(new Date(post.created_at), { addSuffix: true })}</span>
                  </div>
                </div>
              </div>
              <button className="text-gray-400 hover:text-gray-600">
                <MoreVertical className="w-5 h-5" />
              </button>
            </div>

            {/* Post Content */}
            <div className="mt-3">
              {post.title && <h2 className="text-lg font-bold text-gray-800 mb-2">{post.title}</h2>}
              <p className="text-gray-700 whitespace-pre-wrap">{post.content}</p>
            </div>

            {/* Media Gallery */}
            {post.media_urls && post.media_urls.length > 0 && (
              <div className={`mt-3 grid gap-2 ${post.media_urls.length === 1 ? 'grid-cols-1' : 'grid-cols-2'}`}>
                {post.media_urls.map((url, idx) => (
                  <div key={idx} className="relative group cursor-pointer" onClick={() => setSelectedMedia(url)}>
                    {post.media_types?.[idx]?.startsWith('image') ? (
                      <img src={url} alt={`Media ${idx + 1}`} className="rounded-lg w-full h-64 object-cover" />
                    ) : post.media_types?.[idx]?.startsWith('video') ? (
                      <video src={url} className="rounded-lg w-full h-64 object-cover" />
                    ) : (
                      <div className="bg-gray-100 rounded-lg p-4 text-center">
                        <File className="w-12 h-12 text-gray-400 mx-auto" />
                        <p className="text-sm text-gray-500 mt-2">Document</p>
                      </div>
                    )}
                    <button
                      onClick={() => handleDownload(url)}
                      className="absolute top-2 right-2 bg-black/50 p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Download className="w-4 h-4 text-white" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Post Stats */}
            <div className="flex items-center gap-6 mt-4 pt-3 border-t border-gray-100">
              <button
                onClick={() => handleLike(post.id)}
                className={`flex items-center gap-2 text-sm transition-colors ${
                  post.user_liked ? 'text-red-500' : 'text-gray-500 hover:text-red-500'
                }`}
              >
                <Heart className={`w-5 h-5 ${post.user_liked ? 'fill-current' : ''}`} />
                <span>{post.likes?.[0]?.count || 0}</span>
              </button>
              
              <button
                onClick={() => setShowCommentBox(showCommentBox === post.id ? null : post.id)}
                className="flex items-center gap-2 text-sm text-gray-500 hover:text-blue-500 transition-colors"
              >
                <MessageCircle className="w-5 h-5" />
                <span>{post.comments?.[0]?.count || 0}</span>
              </button>
              
              <button
                onClick={() => handleShare(post.id)}
                className="flex items-center gap-2 text-sm text-gray-500 hover:text-green-500 transition-colors"
              >
                <Share2 className="w-5 h-5" />
                <span>{post.share_count || 0}</span>
              </button>
            </div>

            {/* Comments Section */}
            {showCommentBox === post.id && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-4 pt-3 border-t border-gray-100"
              >
                {/* Existing Comments */}
                {post.recent_comments?.map((comment) => (
                  <div key={comment.id} className="flex gap-2 mb-3">
                    <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-xs font-bold">
                      {comment.user?.full_name?.charAt(0)}
                    </div>
                    <div className="flex-1 bg-gray-50 rounded-lg p-2">
                      <p className="text-sm font-semibold">{comment.user?.full_name}</p>
                      <p className="text-sm text-gray-700">{comment.comment}</p>
                      <p className="text-xs text-gray-400 mt-1">{formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}</p>
                    </div>
                  </div>
                ))}
                
                {/* Add Comment */}
                <div className="flex gap-2 mt-3">
                  <input
                    type="text"
                    placeholder="Write a comment..."
                    value={commentText}
                    onChange={(e) => setCommentText(e.target.value)}
                    className="flex-1 px-3 py-2 rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-sm"
                  />
                  <button
                    onClick={() => handleComment(post.id)}
                    className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </AnimatePresence>

      {/* Media Modal */}
      {selectedMedia && (
        <div className="fixed inset-0 bg-black/90 flex items-center justify-center z-50 p-4" onClick={() => setSelectedMedia(null)}>
          <button className="absolute top-4 right-4 text-white p-2 hover:bg-white/10 rounded-full" onClick={() => setSelectedMedia(null)}>
            <X className="w-6 h-6" />
          </button>
          {selectedMedia.match(/\.(jpg|jpeg|png|gif)$/i) ? (
            <img src={selectedMedia} alt="Full size" className="max-w-full max-h-full object-contain" />
          ) : selectedMedia.match(/\.(mp4|webm)$/i) ? (
            <video src={selectedMedia} controls autoPlay className="max-w-full max-h-full" />
          ) : (
            <iframe src={selectedMedia} className="w-full h-full" />
          )}
        </div>
      )}
    </div>
  );
};

export default Feed;
