// src/components/HomePage.js
import * as React from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
// import Divider from '@mui/material/Divider';
import { useInView } from 'react-intersection-observer';
import { motion } from 'framer-motion';
import GitHubIcon from '@mui/icons-material/GitHub';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';

// Import navbar
import AppAppBar from './AppAppBar';

import imgFeature1 from '../assets/img-features/1.jpg';
import imgFeature2 from '../assets/img-features/2.jpg';
import imgFeature3 from '../assets/img-features/3.webp';
import { Divider, styled } from '@mui/material';

const GradientBackground = styled(Box)(({ theme }) => ({
  width: '100%',
  minHeight: '100vh',
  backgroundColor: '#f9f9f9', // Light background
  backgroundImage: `
    radial-gradient(circle at 70% 40%, rgba(255, 200, 100, 0.4), transparent 50%),
    radial-gradient(circle at 30% 70%, rgba(255, 100, 150, 0.3), transparent 50%),
    radial-gradient(circle at 90% 90%, rgba(100, 200, 255, 0.3), transparent 50%)
  `,
  backgroundRepeat: 'no-repeat',
  backgroundSize: 'cover',
  // paddingTop: theme.spacing(8),
  // paddingBottom: theme.spacing(8),
}));

// Hero section
function Hero() {
  // --- Dynamic Stick Figure: Moves Left and Right, 5+ Distinct Motions ---
  // Motions: jumping jack, squat, moonwalk (MJ, with lateral movement), side step, arm wave

  // Keyframes for dynamic motions (as before)
  const POSE_JJACK_CLOSED = [
    { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.44, y: 0.28 }, { x: 0.56, y: 0.28 },
    { x: 0.44, y: 0.41 }, { x: 0.56, y: 0.41 }, { x: 0.45, y: 0.55 }, { x: 0.55, y: 0.55 },
    { x: 0.5, y: 0.44 }, { x: 0.5, y: 0.6 }, { x: 0.47, y: 0.7 }, { x: 0.53, y: 0.7 },
    { x: 0.47, y: 0.88 }, { x: 0.53, y: 0.88 }, { x: 0.47, y: 0.98 }, { x: 0.53, y: 0.98 }
  ];
  const POSE_JJACK_OPEN = [
    { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.36, y: 0.20 }, { x: 0.64, y: 0.20 },
    { x: 0.32, y: 0.08 }, { x: 0.68, y: 0.08 }, { x: 0.35, y: 0.32 }, { x: 0.65, y: 0.32 },
    { x: 0.5, y: 0.44 }, { x: 0.5, y: 0.6 }, { x: 0.43, y: 0.8 }, { x: 0.57, y: 0.8 },
    { x: 0.39, y: 0.98 }, { x: 0.61, y: 0.98 }, { x: 0.39, y: 0.97 }, { x: 0.61, y: 0.97 }
  ];
  const POSE_SQUAT_UP = [
    { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.44, y: 0.28 }, { x: 0.56, y: 0.28 },
    { x: 0.44, y: 0.41 }, { x: 0.56, y: 0.41 }, { x: 0.45, y: 0.55 }, { x: 0.55, y: 0.55 },
    { x: 0.5, y: 0.44 }, { x: 0.5, y: 0.6 }, { x: 0.47, y: 0.7 }, { x: 0.53, y: 0.7 },
    { x: 0.47, y: 0.88 }, { x: 0.53, y: 0.88 }, { x: 0.47, y: 0.98 }, { x: 0.53, y: 0.98 }
  ];
  const POSE_SQUAT_DOWN = [
    { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.44, y: 0.28 }, { x: 0.56, y: 0.28 },
    { x: 0.42, y: 0.46 }, { x: 0.58, y: 0.46 }, { x: 0.40, y: 0.63 }, { x: 0.60, y: 0.63 },
    { x: 0.5, y: 0.48 }, { x: 0.5, y: 0.7 }, { x: 0.47, y: 0.8 }, { x: 0.53, y: 0.8 },
    { x: 0.45, y: 0.94 }, { x: 0.55, y: 0.94 }, { x: 0.45, y: 0.99 }, { x: 0.55, y: 0.99 }
  ];
  // Michael Jackson Moonwalk: 5 keyframes, will shift horizontally
  const MOONWALK = [
    // 1: Lean back, left foot forward, right foot flat
    [
      { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.48, y: 0.28 }, { x: 0.54, y: 0.28 },
      { x: 0.44, y: 0.38 }, { x: 0.56, y: 0.38 }, { x: 0.43, y: 0.56 }, { x: 0.57, y: 0.56 },
      { x: 0.5, y: 0.44 }, { x: 0.5, y: 0.6 }, { x: 0.47, y: 0.7 }, { x: 0.53, y: 0.7 },
      { x: 0.44, y: 0.88 }, { x: 0.53, y: 0.88 }, { x: 0.47, y: 0.98 }, { x: 0.53, y: 0.98 }
    ],
    // 2: Slide left foot back, right foot starts to lift
    [
      { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.49, y: 0.28 }, { x: 0.53, y: 0.28 },
      { x: 0.46, y: 0.38 }, { x: 0.54, y: 0.38 }, { x: 0.45, y: 0.56 }, { x: 0.55, y: 0.56 },
      { x: 0.5, y: 0.44 }, { x: 0.5, y: 0.6 }, { x: 0.49, y: 0.7 }, { x: 0.51, y: 0.7 },
      { x: 0.48, y: 0.88 }, { x: 0.52, y: 0.88 }, { x: 0.49, y: 0.98 }, { x: 0.51, y: 0.98 }
    ],
    // 3: Both feet together, upright
    [
      { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.5, y: 0.28 }, { x: 0.5, y: 0.28 },
      { x: 0.5, y: 0.38 }, { x: 0.5, y: 0.38 }, { x: 0.5, y: 0.56 }, { x: 0.5, y: 0.56 },
      { x: 0.5, y: 0.44 }, { x: 0.5, y: 0.6 }, { x: 0.5, y: 0.7 }, { x: 0.5, y: 0.7 },
      { x: 0.5, y: 0.88 }, { x: 0.5, y: 0.88 }, { x: 0.5, y: 0.98 }, { x: 0.5, y: 0.98 }
    ],
    // 4: Slide right foot back, left foot starts to lift
    [
      { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.51, y: 0.28 }, { x: 0.49, y: 0.28 },
      { x: 0.54, y: 0.38 }, { x: 0.46, y: 0.38 }, { x: 0.53, y: 0.56 }, { x: 0.47, y: 0.56 },
      { x: 0.5, y: 0.44 }, { x: 0.5, y: 0.6 }, { x: 0.51, y: 0.7 }, { x: 0.49, y: 0.7 },
      { x: 0.52, y: 0.88 }, { x: 0.48, y: 0.88 }, { x: 0.51, y: 0.98 }, { x: 0.49, y: 0.98 }
    ],
    // 5: Lean back, right foot forward, left foot flat
    [
      { x: 0.5, y: 0.13 }, { x: 0.5, y: 0.22 }, { x: 0.52, y: 0.28 }, { x: 0.48, y: 0.28 },
      { x: 0.56, y: 0.38 }, { x: 0.44, y: 0.38 }, { x: 0.57, y: 0.56 }, { x: 0.43, y: 0.56 },
      { x: 0.5, y: 0.44 }, { x: 0.5, y: 0.6 }, { x: 0.53, y: 0.7 }, { x: 0.47, y: 0.7 },
      { x: 0.53, y: 0.88 }, { x: 0.44, y: 0.88 }, { x: 0.53, y: 0.98 }, { x: 0.47, y: 0.98 }
    ],
  ];
  // Side step (left/right): arms swing, body shifts
  const POSE_SIDESTEP_CENTRE = POSE_JJACK_CLOSED.map(j => ({...j}));
  const POSE_SIDESTEP_LEFT = POSE_JJACK_CLOSED.map(j => ({...j, x: j.x - 0.08}));
  const POSE_SIDESTEP_RIGHT = POSE_JJACK_CLOSED.map(j => ({...j, x: j.x + 0.08}));
  POSE_SIDESTEP_LEFT[2].x -= 0.03; POSE_SIDESTEP_LEFT[3].x -= 0.03; // arms
  POSE_SIDESTEP_RIGHT[2].x += 0.03; POSE_SIDESTEP_RIGHT[3].x += 0.03;
  // Arm wave (right arm up, left arm up)
  const POSE_ARMWAVE_RIGHT = POSE_JJACK_CLOSED.map((j, i) => i===3 ? {...j, y: j.y-0.12} : j);
  const POSE_ARMWAVE_LEFT = POSE_JJACK_CLOSED.map((j, i) => i===2 ? {...j, y: j.y-0.12} : j);

  const BONES = [
    [0,1],[1,2],[1,3],[2,4],[3,5],[4,6],[5,7],[1,8],[8,9],[9,10],[9,11],[10,12],[11,13],[12,14],[13,15]
  ];

  // Animation phases: all dynamic, with horizontal movement for moonwalk and sidestep
  // Each phase: [poseA, poseB, duration(frames), xShiftA, xShiftB]
  const ANIMATION_PHASES = [
    [POSE_JJACK_CLOSED, POSE_JJACK_OPEN, 22, 0, 0],
    [POSE_JJACK_OPEN, POSE_JJACK_CLOSED, 22, 0, 0],
    [POSE_SQUAT_UP, POSE_SQUAT_DOWN, 18, 0, 0],
    [POSE_SQUAT_DOWN, POSE_SQUAT_UP, 18, 0, 0],
    // Moonwalk left
    [MOONWALK[0], MOONWALK[1], 14, 0, -0.06],
    [MOONWALK[1], MOONWALK[2], 14, -0.06, -0.12],
    [MOONWALK[2], MOONWALK[3], 14, -0.12, -0.18],
    [MOONWALK[3], MOONWALK[4], 14, -0.18, -0.24],
    [MOONWALK[4], MOONWALK[0], 14, -0.24, 0], // snap back to center
    // Sidestep right
    [POSE_SIDESTEP_CENTRE, POSE_SIDESTEP_RIGHT, 16, 0, 0.10],
    [POSE_SIDESTEP_RIGHT, POSE_SIDESTEP_CENTRE, 16, 0.10, 0],
    // Sidestep left
    [POSE_SIDESTEP_CENTRE, POSE_SIDESTEP_LEFT, 16, 0, -0.10],
    [POSE_SIDESTEP_LEFT, POSE_SIDESTEP_CENTRE, 16, -0.10, 0],
    // Arm wave right
    [POSE_JJACK_CLOSED, POSE_ARMWAVE_RIGHT, 14, 0, 0],
    [POSE_ARMWAVE_RIGHT, POSE_JJACK_CLOSED, 14, 0, 0],
    // Arm wave left
    [POSE_JJACK_CLOSED, POSE_ARMWAVE_LEFT, 14, 0, 0],
    [POSE_ARMWAVE_LEFT, POSE_JJACK_CLOSED, 14, 0, 0],
  ];

  const svgRef = React.useRef();
  const animationRef = React.useRef();
  const phaseIndexRef = React.useRef(0);
  const morphProgressRef = React.useRef(0);

  React.useEffect(() => {
    function animate() {
      const svg = svgRef.current;
      if (!svg) return;
      const [poseA, poseB, duration, xShiftA = 0, xShiftB = 0] = ANIMATION_PHASES[phaseIndexRef.current];
      let t = morphProgressRef.current / duration;
      const xShift = xShiftA * (1-t) + xShiftB * t;
      for (let i = 0; i < poseA.length; i++) {
        const x = (poseA[i].x * (1-t) + poseB[i].x * t) + xShift;
        const y = poseA[i].y * (1-t) + poseB[i].y * t;
        const size = 380;
        const cx = x * size + 60;
        const cy = y * size + 40;
        const dot = svg.querySelector(`#joint0_${i}`);
        if (dot) {
          dot.setAttribute('cx', cx);
          dot.setAttribute('cy', cy);
        }
      }
      // Bones
      for (let b = 0; b < BONES.length; b++) {
        const [i, j] = BONES[b];
        const x1 = (poseA[i].x * (1-t) + poseB[i].x * t) + xShift;
        const y1 = poseA[i].y * (1-t) + poseB[i].y * t;
        const x2 = (poseA[j].x * (1-t) + poseB[j].x * t) + xShift;
        const y2 = poseA[j].y * (1-t) + poseB[j].y * t;
        const size = 380;
        const x1p = x1 * size + 60;
        const y1p = y1 * size + 40;
        const x2p = x2 * size + 60;
        const y2p = y2 * size + 40;
        const line = svg.querySelector(`#bone0_${b}`);
        if (line) {
          line.setAttribute('x1', x1p);
          line.setAttribute('y1', y1p);
          line.setAttribute('x2', x2p);
          line.setAttribute('y2', y2p);
        }
      }
      // Head
      const head = svg.querySelector(`#head0`);
      if (head) {
        const x = (poseA[0].x * (1-t) + poseB[0].x * t) + xShift;
        const y = poseA[0].y * (1-t) + poseB[0].y * t;
        const size = 380;
        const cx = x * size + 60;
        const cy = y * size + 40;
        head.setAttribute('cx', cx);
        head.setAttribute('cy', cy);
      }
      morphProgressRef.current++;
      if (morphProgressRef.current >= duration) {
        morphProgressRef.current = 0;
        phaseIndexRef.current = (phaseIndexRef.current + 1) % ANIMATION_PHASES.length;
      }
      animationRef.current = requestAnimationFrame(animate);
    }
    animationRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationRef.current);
  }, []);

  // Render a single animated stick figure
  return (
    <Box
      id="home"
      sx={{
        // bgcolor: 'background.paper',
        pt: { xs: 14, sm: 16, md: 16, lg: 16 },
        pb: { xs: 8, md: 14 },
        minHeight: '65vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
        overflow: 'hidden',
        scrollMarginTop: { xs: 13, sm: 16 },
        '::before': {
          content: '""',
          position: 'absolute',
          inset: 0,
          zIndex: 0,
          pointerEvents: 'none',
          // background:
          //   'radial-gradient(circle at 20% 30%, rgba(44,90,233,0.07) 0%, transparent 70%),' +
          //   'radial-gradient(circle at 80% 70%, rgba(44,90,233,0.10) 0%, transparent 70%),' +
          //   'linear-gradient(120deg, rgba(232,240,254,0.7) 0%, rgba(248,249,250,0.7) 100%)',
          // opacity: 1,
          // transition: 'opacity 0.5s',
        },
        '::after': {
          content: '""',
          position: 'absolute',
          inset: 0,
          zIndex: 1,
          pointerEvents: 'none',
          // background:
          //   'repeating-linear-gradient(135deg, rgba(44,90,233,0.03) 0px, rgba(44,90,233,0.03) 2px, transparent 2px, transparent 16px)',
          // opacity: 0.6,
          // transition: 'opacity 0.5s',
        },
      }}
    >
      <Box sx={{ position: 'relative', zIndex: 2, width: '100%' }}>
        {/* Subtle dotted background accent */}
        <Box sx={{
          position: 'absolute',
          inset: 0,
          zIndex: 0,
          pointerEvents: 'none',
          // backgroundImage: 'radial-gradient(rgba(44,90,233,0.07) 1px, transparent 1px)',
          backgroundSize: '28px 28px',
        }} />
        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 2 }}>
          <Grid container alignItems="center" spacing={6}>
            <Grid item xs={12} md={6}>
              <Box sx={{ textAlign: { xs: 'center', md: 'left' } }}>
                <Typography
                  component="h1"
                  variant="h2"
                  // fontWeight={900}
                  sx={{
                    color: 'black',
                    mb: 0.5,
                    // fontSize: { xs: '2.6rem', md: '4.2rem' },
                    fontWeight: 'bold',
                    textShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)',
                    letterSpacing: 0.5,
                    lineHeight: 1.08,
                    display: 'inline-block',
                    textAlign: { xs: 'center', md: 'left' },
                    width: { xs: '100%', md: 'auto' }
                  }}
                >
                  PhysioFlow
                </Typography>
                <Typography
                  variant="h5"
                  color="text.secondary"
                  paragraph
                  align="left"
                  sx={{
                    mb: 4,
                    mt: 1,
                    maxWidth: 600,
                    mx: { xs: 'auto', md: 0 },
                    textAlign: { xs: 'center', md: 'left' },
                    display: 'block',
                  }}
                >
                  AI-Powered Physiotherapy Assistant with Real-Time Movement Analysis
                </Typography>
                <Stack
                  sx={{ pt: 2 }}
                  direction="row"
                  spacing={2}
                  justifyContent={{ xs: 'center', md: 'flex-start' }}
                >
                  <Button
                    variant="contained"
                    size="large"
                    sx={{
                      bgcolor: '#6e4670',
                      color: '#fff',
                      fontWeight: 700,
                      boxShadow: 3,
                      '&:hover': { bgcolor: '#c57196' }
                    }}
                  >
                    Try Now
                  </Button>
                  <Button
                    variant="outlined"
                    size="large"
                    sx={{
                      borderColor: '#6e4670',
                      color: '#6e4670',
                      fontWeight: 700,
                      '&:hover': { borderColor: '#c57196', color: '#c57196' }
                    }}
                  >
                    Learn More
                  </Button>
                </Stack>
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', justifyContent: { xs: 'center', md: 'flex-end' } }}>
                <Box display="flex" justifyContent="center" alignItems="center" gap={6}>
                  <Box sx={{ width: 520, height: 480, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <svg ref={svgRef} width="520" height="480" viewBox="0 0 520 480" fill="none" xmlns="http://www.w3.org/2000/svg">
                      {/* Bones */}
                      {BONES.map(([i, j], b) => (
                        <line key={`bone0_${b}`} id={`bone0_${b}`} x1={-1000} y1={-1000} x2={-1000} y2={-1000} stroke="#2c5ae9" strokeWidth={10} strokeLinecap="round" opacity={0.22 + b*0.045} />
                      ))}
                      {/* Joints */}
                      {POSE_JJACK_CLOSED.map((_, i) => (
                        <circle key={`joint0_${i}`} id={`joint0_${i}`} cx={-1000} cy={-1000} r={12} fill="#2c5ae9" stroke="#e8f0fe" strokeWidth={4} />
                      ))}
                      {/* Head highlight */}
                      <circle id={`head0`} cx={-1000} cy={-1000} r={38} fill="#e8f0fe" stroke="#2c5ae9" strokeWidth={12} />
                    </svg>
                  </Box>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
}

// Video section
function VideoDemo() {
  return (
    <Box
      id="demo"
      sx={{ 
        // background: 'linear-gradient(180deg, #e8f0fe 0%, #f8f9fa 100%)',
        py: 8,
        scrollMarginTop: { xs: 13, sm: 16 }
      }}
    >
      <Container maxWidth="lg">
      <Typography
            variant="h4"
            align="center"
            gutterBottom
            sx={{
              fontWeight: 'bold',
              textShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)', // diffused shadow
            }}
          >
            See PhysioFlow In Action
          </Typography>
        <Box
          sx={{
            width: '100%',
            height: 0,
            paddingBottom: '56.25%', // 16:9 ratio
            position: 'relative',
            mt: 4,
            bgcolor: 'grey.200',
            borderRadius: 2,
            overflow: 'hidden',
          }}
        >
          {/* Placeholder for video */}
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography variant="h6" color="text.secondary">
              Video Demo Placeholder
            </Typography>
          </Box>
        </Box>
      </Container>
    </Box>
  );
}

// Features section
function Features() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const features = [
    {
      title: 'Real-time Movement Analysis',
      description: 'Get instant feedback on your exercise form with advanced computer vision.',
      image: imgFeature1,
    },
    {
      title: 'AI-Powered Guidance',
      description: 'Groq AI provides personalized guidance and customized exercise plans.',
      image: imgFeature2,
    },
    {
      title: 'Curated List of Exercises',
      description: 'Choose which exercise to practise from our hand-picked list of physiotherapy movements.',
      image: imgFeature3,
    },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.3
      }
    }
  };

  const itemVariants = {
    hidden: { y: 50, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 100,
        damping: 12
      }
    }
  };

  return (
    <Box id="features" sx={{ py: 8, scrollMarginTop: { xs: 13, sm: 16 } }} ref={ref}>
      <Container maxWidth="lg">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.6 }}
        >
          <Typography
            variant="h4"
            align="center"
            gutterBottom
            sx={{
              fontWeight: 'bold',
              textShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)', // diffused shadow
            }}
          >
            Key Features
          </Typography>
        </motion.div>
        
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate={inView ? "visible" : "hidden"}
        >
          <Grid container spacing={4} sx={{ mt: 2 }}>
            {features.map((feature, index) => (
              <Grid item key={index} xs={12} sm={6} md={4}>
                <motion.div variants={itemVariants}>
                  <Card
                    sx={{
                      height: 340,
                      minHeight: 340,
                      maxHeight: 340,
                      display: 'flex',
                      flexDirection: 'column',
                      boxShadow: 3,
                      alignItems: 'stretch',
                      justifyContent: 'flex-start',
                      '&:hover': {
                        transform: 'translateY(-8px)',
                        transition: 'transform 0.3s ease-in-out',
                        boxShadow: 6,
                      },
                      transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
                    }}
                  >
                    <CardMedia
                      component="img"
                      height="220"
                      image={feature.image}
                      alt={feature.title}
                      sx={{ objectFit: 'cover', width: '100%' }}
                    />
                    <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', p: 1.5, minHeight: 0 }}>
                      <Typography gutterBottom variant="h5" component="h2" sx={{ 
                        textShadow: '0px 4px 5px rgba(0, 0, 0, 0.2)', // diffused shadow
                        color: '#6e4670', fontWeight: 700, textAlign: 'center', mb: 0.5, fontSize: 22, lineHeight: 1.2 }}>
                        {feature.title}
                      </Typography>
                      <Typography sx={{ fontSize: 14.5, color: 'text.secondary', textAlign: 'center', mt: 0, lineHeight: 1.3 }}>
                        {feature.description}
                      </Typography>
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
            ))}
          </Grid>
        </motion.div>
      </Container>
    </Box>
  );
}

// FAQ section
function FAQ() {
  const [expanded, setExpanded] = React.useState(false);
  
  const { ref: faqRef, inView: faqInView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const faqs = [
    {
      id: 'panel1',
      question: 'What equipment do I need to use PhysioFlow?',
      answer: 'Just a smartphone or tablet with a camera. PhysioFlow works on any modern device with web access. The app is optimized for both mobile and desktop experiences, with mobile focusing on camera-based tracking.',
    },
    {
      id: 'panel2',
      question: 'How accurate is the movement detection?',
      answer: 'Our AI-powered system achieves 85% accuracy in detecting proper form and movement patterns. We use a combination of OpenCV and MediaPipe technologies to track 33 key body points in real-time, allowing for precise analysis of your movements.',
    },
    {
      id: 'panel3',
      question: 'Can I use PhysioFlow without a prescription?',
      answer: 'Yes! While PhysioFlow works great with professional guidance, anyone can use it for exercise guidance and form correction. The app includes a exercise modules of common physiotherapy exercises and yoga poses that are safe for most users.',
    },
    {
      id: 'panel4',
      question: 'How does the Groq AI assistant help with my exercises?',
      answer: 'The Groq AI assistant analyzes your movements in real-time and provides personalized feedback through both voice and text. It can suggest adjustments to your form, track your progress over time, and adapt exercise recommendations based on your performance and recovery patterns.',
    },
    {
      id: 'panel5',
      question: 'Is my exercise data private and secure?',
      answer: 'Absolutely. Your privacy is our priority. All movement data is processed locally on your device when possible, and any data sent to our servers is encrypted and anonymized. We never share your personal health information with third parties without your explicit consent.',
    },
    {
      id: 'panel6',
      question: 'Can I track my progress over time?',
      answer: 'Unfortunately, PhysioFlow does not include comprehensive progress tracking features at the moment. We are working on providing detailed analytics of your performance, including range of motion improvements, exercise consistency, and form accuracy over time.',
    },
    {
      id: 'panel7',
      question: 'Do I need a subscription to use PhysioFlow?',
      answer: 'PhysioFlow is completely free to use. All features, including exercise tracking, form analysis, and access to our exercise library, are available at no cost. Enjoy the full experience without any subscription or hidden fees.',
    },
    {
      id: 'panel8',
      question: 'Can PhysioFlow be used for remote physical therapy sessions?',
      answer: 'Yes! PhysioFlow is designed to support remote therapy. Physical therapists can assign specific exercises, monitor patient progress remotely, and provide feedback based on the detailed movement data collected by the app. This makes it ideal for telehealth and hybrid care models.',
    },
  ];

  const handleExpand = (id) => {
    setExpanded(expanded === id ? false : id);
  };

  return (
    <Box id="faq" sx={{ py: 8, scrollMarginTop: { xs: 13, sm: 16 } }} ref={faqRef}>
      <Container maxWidth="md">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={faqInView ? { opacity: 1, y: 0 } : { opacity: 0, y: -50 }}
          transition={{ 
            type: 'spring',
            stiffness: 60,
            damping: 14
          }}
        >
          <Typography
            variant="h4"
            align="center"
            gutterBottom
            sx={{
              fontWeight: 'bold',
              textShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)', // diffused shadow
            }}
          >
            Frequently Asked Questions
          </Typography>
        </motion.div>
        <Box sx={{ mt: 4 }}>
          {faqs.map((faq, idx) => (
            <motion.div
              key={faq.id}
              initial={{ opacity: 0, y: 40 }}
              animate={faqInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
              transition={{ duration: 0.45, delay: 0.1 + idx * 0.08, ease: [0.4, 0, 0.2, 1] }}
              style={{ width: '100%', marginBottom: 20 }}
            >
              <Box
                sx={{
                  backgroundColor: '#9a629d',
                  color: 'white',
                  borderTopLeftRadius: 8,
                  borderTopRightRadius: 8,
                  borderBottomLeftRadius: expanded === faq.id ? 0 : 8,
                  borderBottomRightRadius: expanded === faq.id ? 0 : 8,
                  boxShadow: 2,
                  p: 1.5,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  cursor: 'pointer',
                  mb: 0,
                  transition: 'border-radius 0.3s',
                }}
                onClick={() => handleExpand(faq.id)}
              >
                <Typography variant="subtitle1" color="white">
                  {faq.question}
                </Typography>
                <Box sx={{ 
                  transform: expanded === faq.id ? 'rotate(180deg)' : 'rotate(0deg)',
                  transition: 'transform 0.3s'
                }}>
                  ▼
                </Box>
              </Box>
              <Collapse in={expanded === faq.id} timeout={400} easing={{ enter: 'cubic-bezier(0.4,0,0.2,1)', exit: 'cubic-bezier(0.4,0,0.2,1)' }}>
                <Box
                  sx={{
                    backgroundColor: '#b48bb6',
                    color: 'white',
                    borderBottomLeftRadius: 8,
                    borderBottomRightRadius: 8,
                    borderTopLeftRadius: 0,
                    borderTopRightRadius: 0,
                    boxShadow: 2,
                    p: 2,
                    mt: 0,
                  }}
                >
                  <Typography variant="body1" color="white" sx={{ p: 2, pt: 0 }}>
                    {faq.answer}
                  </Typography>
                </Box>
              </Collapse>
            </motion.div>
          ))}
        </Box>
      </Container>
    </Box>
  );
}

// Footer section
function Footer() {
  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <Box sx={{ 
      // bgcolor: 'primary.dark', 
      py: 3, color: 'black' }}>
      <Container maxWidth="lg">
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          flexDirection: { xs: 'column', sm: 'row' },
          gap: { xs: 2, sm: 0 }
        }}>
          {/* Navigation Links */}
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <Typography 
              variant="body2" 
              color="black" 
              sx={{ 
                cursor: 'pointer',
                '&:hover': { textDecoration: 'underline' }
              }}
              onClick={() => scrollToSection('home')}
            >
              Home
            </Typography>
            <Typography variant="body2" color="black">•</Typography>
            <Typography 
              variant="body2" 
              color="black"
              sx={{ 
                cursor: 'pointer',
                '&:hover': { textDecoration: 'underline' }
              }}
              onClick={() => scrollToSection('demo')}
            >
              Demo
            </Typography>
            <Typography variant="body2" color="black">•</Typography>
            <Typography 
              variant="body2" 
              color="black"
              sx={{ 
                cursor: 'pointer',
                '&:hover': { textDecoration: 'underline' }
              }}
              onClick={() => scrollToSection('features')}
            >
              Features
            </Typography>
            <Typography variant="body2" color="black">•</Typography>
            <Typography 
              variant="body2" 
              color="black"
              sx={{ 
                cursor: 'pointer',
                '&:hover': { textDecoration: 'underline' }
              }}
              onClick={() => scrollToSection('faq')}
            >
              FAQs
            </Typography>
          </Box>
          
          {/* Copyright Text */}
          <Typography variant="body2" color="black" sx={{ opacity: 0.9, fontWeight: 'medium', textAlign: 'center' }}>
            Copyright &copy; PhysioFlow {new Date().getFullYear()}
          </Typography>
          
          {/* GitHub Logo */}
          <IconButton 
            href="https://github.com/dhananjay2403/physioflow-ai.git" 
            target="_blank"
            sx={{ color: 'black' }}
            aria-label="GitHub repository"
          >
            <GitHubIcon />
          </IconButton>
        </Box>
      </Container>
    </Box>
  );
}

export default function HomePage() {
  return (
    <GradientBackground>
      <AppAppBar />
      <main>
        <Hero />
        <Divider></Divider>
        <VideoDemo />
        <Divider></Divider>
        <Features />
        <Divider></Divider>
        {/* <Testimonials /> */}
        <FAQ />
      </main>
      <Divider></Divider>
      <Footer />
    </GradientBackground>
  );
}