import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Mic, X, Image, Video, File } from 'lucide-react';
import { useVoiceRecorder } from 'react-voice-recorder';
import EmojiPicker from 'emoji-picker-react';
import toast from 'react-hot-toast';

const ChatInterface = ({ messages, onSendMessage, currentUserId, otherUser }) => {
  const [newMessage, setNewMessage] = useState('');
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!newMessage.trim()) return;
    await onSendMessage(newMessage);
    setNewMessage('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      // Handle file upload
      toast.success('File upload coming soon');
    }
  };

  const onEmojiClick = (emojiData) => {
    setNewMessage(prev => prev + emojiData.emoji);
    setShowEmojiPicker(false);
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 rounded-xl overflow-hidden">
      {/* Chat Header */}
      {otherUser && (
        <div className="bg-white p-4 border-b flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-white font-bold">
            {otherUser.full_name?.charAt(0)}
          </div>
          <div>
            <h3 className="font-semibold text-gray-800">{otherUser.full_name}</h3>
            <p className="text-xs text-gray-500">{otherUser.role?.replace('_', ' ')}</p>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.sender_id === currentUserId ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`chat-bubble ${msg.sender_id === currentUserId ? 'chat-bubble-sent' : 'chat-bubble-received'}`}>
              {msg.voice_note_url && (
                <audio controls className="w-48 h-8">
                  <source src={msg.voice_note_url} type="audio/mpeg" />
                </audio>
              )}
              {msg.file_url && msg.file_type === 'image' && (
                <img src={msg.file_url} alt="Shared" className="max-w-xs rounded-lg" />
              )}
              {msg.message && <p className="whitespace-pre-wrap">{msg.message}</p>}
              <p className="text-xs opacity-70 mt-1">
                {new Date(msg.created_at).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white p-4 border-t">
        <div className="flex items-center gap-2">
          <button
            onClick={() => fileInputRef.current?.click()}
            className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
          >
            <Paperclip className="w-5 h-5" />
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept="image/*,video/*,application/pdf"
            className="hidden"
          />
          
          <button
            onClick={() => setIsRecording(!isRecording)}
            className={`p-2 transition-colors ${isRecording ? 'text-red-500' : 'text-gray-500'}`}
          >
            <Mic className="w-5 h-5" />
          </button>

          <div className="relative flex-1">
            <textarea
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type a message..."
              className="w-full px-4 py-2 rounded-xl border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none resize-none"
              rows="1"
            />
            <button
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
              className="absolute right-2 bottom-2 text-gray-400 hover:text-gray-600"
            >
              😊
            </button>
          </div>

          <button
            onClick={handleSend}
            disabled={!newMessage.trim()}
            className="btn-primary p-3"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>

        {showEmojiPicker && (
          <div className="absolute bottom-20 right-4 z-50">
            <EmojiPicker onEmojiClick={onEmojiClick} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;
