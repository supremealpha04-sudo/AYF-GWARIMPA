import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import { ChevronLeft, ChevronRight, Plus, X } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

const Calendar = () => {
  const { user } = useAuth();
  const [events, setEvents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [newEvent, setNewEvent] = useState({
    title: '',
    description: '',
    event_date: '',
    event_level: 'archdeaconry',
    parish_id: '',
    is_recurring: false,
    recurrence_pattern: 'weekly'
  });

  const isAdmin = ['admin', 'gen_president', 'gen_sec'].includes(user?.role);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const currentDate = new Date();
      const response = await api.get('/calendar/events', {
        params: {
          month: currentDate.getMonth() + 1,
          year: currentDate.getFullYear()
        }
      });
      setEvents(response.data);
    } catch (error) {
      console.error('Error fetching events:', error);
      toast.error('Failed to load events');
    }
  };

  const handleDateClick = (info) => {
    if (!isAdmin) return;
    setNewEvent({ ...newEvent, event_date: info.dateStr });
    setShowModal(true);
  };

  const handleEventClick = (info) => {
    setSelectedEvent(info.event);
    // Show event details modal
    toast.info(`${info.event.title}\n${info.event.extendedProps.description || ''}`);
  };

  const handleCreateEvent = async () => {
    try {
      await api.post('/calendar/events', newEvent);
      toast.success('Event created successfully');
      setShowModal(false);
      fetchEvents();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create event');
    }
  };

  const getEventColor = (eventLevel) => {
    switch (eventLevel) {
      case 'archdeaconry': return '#3B82F6';
      case 'diocese': return '#8B5CF6';
      case 'parish': return '#10B981';
      default: return '#6B7280';
    }
  };

  const calendarEvents = events.map(event => ({
    id: event.id,
    title: event.display_text || event.title,
    start: event.event_date,
    color: getEventColor(event.event_level),
    extendedProps: {
      description: event.description,
      level: event.event_level
    }
  }));

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Yearly Plan Calendar</h1>
            <p className="text-gray-600 mt-1">View all events and activities for the year</p>
          </div>
          {isAdmin && (
            <button
              onClick={() => setShowModal(true)}
              className="btn-primary flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              Add Event
            </button>
          )}
        </div>

        <FullCalendar
          plugins={[dayGridPlugin, interactionPlugin]}
          initialView="dayGridMonth"
          events={calendarEvents}
          dateClick={handleDateClick}
          eventClick={handleEventClick}
          headerToolbar={{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek'
          }}
          buttonText={{
            today: 'Today',
            month: 'Month',
            week: 'Week'
          }}
          height="auto"
          aspectRatio={1.5}
          locale="en"
        />
      </motion.div>

      {/* Event Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white rounded-2xl max-w-md w-full p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-800">Create Event</h2>
              <button onClick={() => setShowModal(false)} className="p-1 hover:bg-gray-100 rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4">
              <input
                type="text"
                placeholder="Event Title"
                value={newEvent.title}
                onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                className="input-field"
              />
              
              <textarea
                placeholder="Description"
                value={newEvent.description}
                onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
                className="input-field"
                rows="3"
              />
              
              <input
                type="date"
                value={newEvent.event_date}
                onChange={(e) => setNewEvent({ ...newEvent, event_date: e.target.value })}
                className="input-field"
              />
              
              <select
                value={newEvent.event_level}
                onChange={(e) => setNewEvent({ ...newEvent, event_level: e.target.value })}
                className="input-field"
              >
                <option value="archdeaconry">Archdeaconry</option>
                <option value="diocese">Diocese</option>
                <option value="parish">Parish</option>
              </select>

              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={newEvent.is_recurring}
                  onChange={(e) => setNewEvent({ ...newEvent, is_recurring: e.target.checked })}
                />
                <span>Recurring Event</span>
              </label>

              {newEvent.is_recurring && (
                <select
                  value={newEvent.recurrence_pattern}
                  onChange={(e) => setNewEvent({ ...newEvent, recurrence_pattern: e.target.value })}
                  className="input-field"
                >
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                </select>
              )}

              <button onClick={handleCreateEvent} className="btn-primary w-full">
                Create Event
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default Calendar;
