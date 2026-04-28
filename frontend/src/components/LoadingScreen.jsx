import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const LoadingScreen = ({ onComplete }) => {
  const [step, setStep] = useState(0);
  const words = ['FELLOWSHIP!', 'FELLOWSHIP!!', 'FELLOWSHIP!!!'];

  useEffect(() => {
    const timer = setInterval(() => {
      setStep((prev) => {
        if (prev + 1 >= words.length) {
          clearInterval(timer);
          setTimeout(onComplete, 500);
          return prev;
        }
        return prev + 1;
      });
    }, 400);

    return () => clearInterval(timer);
  }, [onComplete, words.length]);

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900 via-purple-900 to-pink-900">
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl animate-blob"></div>
          <div className="absolute top-0 -right-4 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-2000"></div>
          <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl animate-blob animation-delay-4000"></div>
        </div>
      </div>

      {/* Content */}
      <div className="relative z-10 text-center">
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ duration: 0.6, type: 'spring' }}
          className="mb-8"
        >
          <img 
            src="/logo.png" 
            alt="AYF Logo" 
            className="w-32 h-32 mx-auto rounded-full shadow-2xl border-4 border-white"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/128?text=AYF';
            }}
          />
        </motion.div>

        <AnimatePresence mode="wait">
          <motion.h1
            key={step}
            initial={{ opacity: 0, y: 20, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.8 }}
            transition={{ duration: 0.3, type: 'spring' }}
            className="text-5xl md:text-7xl font-bold text-white font-poppins tracking-wider"
          >
            {words[step]}
          </motion.h1>
        </AnimatePresence>

        <motion.div
          initial={{ width: 0 }}
          animate={{ width: '100%' }}
          transition={{ duration: 1.2, repeat: Infinity }}
          className="h-1 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 mt-8 rounded-full mx-auto"
          style={{ maxWidth: '200px' }}
        />
        
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-white/70 mt-4 text-sm"
        >
          AYF Gwarimpa Archdeaconry
        </motion.p>
      </div>
    </div>
  );
};

export default LoadingScreen;
