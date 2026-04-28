import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import { HelmetProvider } from 'react-helmet-async'
import LoadingScreen from './components/LoadingScreen'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Calendar from './pages/Calendar'
import Feed from './pages/Feed'
import Chat from './pages/Chat'
import Profile from './pages/Profile'
import AdminPanel from './pages/AdminPanel'
import QuarterlyShare from './pages/QuarterlyShare'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

const AppRoutes = () => {
  const { user, loading } = useAuth()

  if (loading) {
    return <LoadingScreen onComplete={() => {}} />
  }

  return (
    <Routes>
      <Route path="/login" element={!user ? <Login /> : <Navigate to="/" />} />
      <Route path="/" element={user ? <Layout /> : <Navigate to="/login" />}>
        <Route index element={<Dashboard />} />
        <Route path="calendar" element={<Calendar />} />
        <Route path="feed" element={<Feed />} />
        <Route path="chat" element={<Chat />} />
        <Route path="profile" element={<Profile />} />
        <Route path="quarterly" element={<QuarterlyShare />} />
        <Route path="admin/*" element={user?.role === 'admin' ? <AdminPanel /> : <Navigate to="/" />} />
      </Route>
    </Routes>
  )
}

function App() {
  const [showLoading, setShowLoading] = useState(true)

  return (
    <HelmetProvider>
      <QueryClientProvider client={queryClient}>
        <Router>
          <AuthProvider>
            <AppRoutes />
            <Toaster 
              position="top-right" 
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#363636',
                  color: '#fff',
                },
                success: {
                  duration: 3000,
                  iconTheme: {
                    primary: '#10B981',
                    secondary: '#fff',
                  },
                },
                error: {
                  duration: 4000,
                  iconTheme: {
                    primary: '#EF4444',
                    secondary: '#fff',
                  },
                },
              }} 
            />
          </AuthProvider>
        </Router>
      </QueryClientProvider>
    </HelmetProvider>
  )
}

export default App
