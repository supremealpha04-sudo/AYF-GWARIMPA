import { io } from 'socket.io-client';

const SOCKET_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class SocketService {
  constructor() {
    this.socket = null;
  }

  connect(token) {
    this.socket = io(SOCKET_URL, {
      auth: { token },
      transports: ['websocket'],
    });

    this.socket.on('connect', () => {
      console.log('Socket connected');
    });

    this.socket.on('disconnect', () => {
      console.log('Socket disconnected');
    });

    return this.socket;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  joinRoom(roomId) {
    if (this.socket) {
      this.socket.emit('join', { room: roomId });
    }
  }

  leaveRoom(roomId) {
    if (this.socket) {
      this.socket.emit('leave', { room: roomId });
    }
  }

  sendMessage(roomId, message) {
    if (this.socket) {
      this.socket.emit('message', { room: roomId, message });
    }
  }

  onMessage(callback) {
    if (this.socket) {
      this.socket.on('message', callback);
    }
  }

  onTyping(callback) {
    if (this.socket) {
      this.socket.on('typing', callback);
    }
  }
}

export default new SocketService();
