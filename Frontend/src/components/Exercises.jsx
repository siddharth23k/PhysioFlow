import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  InputBase,
  Box,
  Grid,
  Card,
  CardContent,
  CardMedia,
  styled,
} from '@mui/material';
import { Search, ArrowBack } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { exerciseData } from '../utils/Exercises';

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

const Exercises = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearchChange = (e) => setSearchQuery(e.target.value);

  const filteredExercises = exerciseData.filter((exercise) =>
    exercise.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const displayedExercises = searchQuery ? filteredExercises : exerciseData;

  return (
    <GradientBackground sx={{ flexGrow: 1, bgcolor: '#f7f9fc', minHeight: '100vh' }}>
      {/* Top AppBar */}
      <AppBar position="static" color="default" sx={{ background: 'transparent',  boxShadow: 1 }}>
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={() => navigate(-1)} sx={{ mr: 2 }}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" sx={{ flexGrow: 1}}>
            Exercises
          </Typography>
          <Box
            sx={{
                display: 'flex',
                alignItems: 'center',
                bgcolor: '#e0e0e0',
                borderRadius: 2,
                pl: 1,
                pr: 2,
                width: { xs: 140, sm: 200, md: 250 },
            }}
            >
            <Search sx={{ color: 'dark gray', mr: 1 }} />
            <InputBase
                placeholder="Search exercises…"
                value={searchQuery}
                onChange={handleSearchChange}
                fullWidth
            />
            </Box>
        </Toolbar>
      </AppBar>

      {/* Exercise Cards */}
      <Grid container spacing={3} sx={{ p: 3 }}>
        {displayedExercises.length > 0 ? (
          displayedExercises.map((exercise) => (
            <Grid item key={exercise.id} xs={12} sm={6} md={4} lg={3}>
              <Card
                sx={{
                  height: '100%',
                  borderRadius: 3,
                  boxShadow: 3,
                  transition: 'transform 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'scale(1.03)',
                  },
                }}
              >
                <CardMedia
                  component="img"
                  height="180"
                  image={exercise.image}
                  alt={exercise.name}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent>
                  <Typography variant="h6" component="div" gutterBottom>
                    {exercise.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {exercise.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          <Grid item xs={12}>
            <Typography variant="body1" align="center" sx={{ mt: 4 }}>
              No exercises found for "{searchQuery}"
            </Typography>
          </Grid>
        )}
      </Grid>
    </GradientBackground>
  );
};

export default Exercises;
