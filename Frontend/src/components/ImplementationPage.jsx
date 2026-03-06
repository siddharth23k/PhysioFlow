import React, { useState, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Box, Button, Typography, Card, CardContent, CircularProgress, IconButton,
} from '@mui/material';
import { ArrowBack, PlayArrow, Stop, Feedback, Repeat, Search, VolumeUp } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { startCamera, stopCamera } from '../utils/ImplementationPage';

const ImplementationPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { exerciseName, exerciseDescription } = location.state || {};

  const [cameraActive, setCameraActive] = useState(false);
  const [sessionEnded, setSessionEnded] = useState(false);
  const [feedbackText, setFeedbackText] = useState('Groq AI will guide you here...');
  const videoRef = useRef(null);

  const handleOpenCamera = async () => {
    setCameraActive(true);
    await startCamera(videoRef);
    setFeedbackText('Groq AI is analyzing your posture...');
  };

  const handleEndSession = async () => {
    await stopCamera(videoRef);
    setCameraActive(false);
    setSessionEnded(true);
    setFeedbackText('Session ended. Generating report...');
  };

  const handleRepeat = () => {
    setSessionEnded(false);
    handleOpenCamera();
  };

  return (
    <Box
      sx={{
        px: 2,
        py: 3,
        maxWidth: '100%',
        overflowX: 'hidden',
        scrollBehavior: 'smooth',
      }}
    >
      <IconButton onClick={() => navigate(-1)}>
        <ArrowBack />
      </IconButton>

      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
        <Typography variant="h4" fontWeight="bold" mb={1}>
          {exerciseName}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" mb={3}>
          {exerciseDescription}
        </Typography>
      </motion.div>

      <motion.div initial={{ y: 30, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
        <Card sx={{ mb: 3, p: 2 }}>
          <CardContent>
            <Typography variant="body1" mb={1}>
              Welcome! To begin your exercise with Groq AI:
            </Typography>
            <ul style={{ paddingLeft: '20px' }}>
              <li>Ensure you're in a well-lit area.</li>
              <li>Position your full body within the camera frame.</li>
              <li>Wear comfortable clothing for accurate detection.</li>
              <li>Follow Groq AI’s live posture feedback and audio cues.</li>
            </ul>
            {!cameraActive ? (
              <Button
                variant="contained"
                startIcon={<PlayArrow />}
                onClick={handleOpenCamera}
                sx={{ mt: 2 }}
              >
                Open Camera
              </Button>
            ) : (
              <Button
                variant="contained"
                color="error"
                startIcon={<Stop />}
                onClick={handleEndSession}
                sx={{ mt: 2 }}
              >
                End Session
              </Button>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {cameraActive && (
        <motion.div animate={{ y: [50, 0], opacity: [0, 1] }}>
          <Box display="flex" flexDirection="column" alignItems="center" mb={3}>
            <video
              ref={videoRef}
              autoPlay
              muted
              playsInline
              style={{
                width: '100%',
                maxWidth: '600px',
                borderRadius: '16px',
                boxShadow: '0 4px 20px rgba(0,0,0,0.2)',
              }}
            />
            <Box
              mt={2}
              p={2}
              width="100%"
              maxWidth="600px"
              bgcolor="background.paper"
              borderRadius="12px"
              boxShadow={3}
              position="relative"
            >
              <Typography variant="body2">{feedbackText}</Typography>
              <VolumeUp sx={{ position: 'absolute', right: 16, top: 16, animation: 'pulse 2s infinite' }} />
            </Box>
          </Box>
        </motion.div>
      )}

      {sessionEnded && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}>
          <Card sx={{ mb: 3, p: 2 }}>
            <Typography variant="h6">Your Report</Typography>
            <Typography variant="body2" color="text.secondary" mt={1}>
              You were mostly correct in your form. Focus on correcting your shoulder posture.
              We recommend 2 more sets of this exercise today and then follow up with hamstring stretches.
            </Typography>
            <Button variant="outlined" sx={{ mt: 2 }}>
              Download Report as PDF
            </Button>
          </Card>
          <Box display="flex" gap={2} flexWrap="wrap" mb={3}>
            <Button
              variant="contained"
              startIcon={<Repeat />}
              onClick={handleRepeat}
            >
              Repeat Exercise
            </Button>
            <Button
              variant="contained"
              color="secondary"
              startIcon={<Search />}
              onClick={() => navigate('/exercises')}
            >
              Search Other Exercises
            </Button>
          </Box>
        </motion.div>
      )}

      <Box textAlign="center" mt={4}>
        <Button
          startIcon={<Feedback />}
          onClick={() => window.open('https://forms.gle/feedback-link', '_blank')}
        >
          Give Feedback
        </Button>
      </Box>
    </Box>
  );
};

export default ImplementationPage;
