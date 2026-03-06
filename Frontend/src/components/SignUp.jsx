import React, { useState } from 'react';
import {
  Box, Button, Checkbox, Container, Grid, Link, styled, TextField, Typography
} from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';
import FacebookIcon from '@mui/icons-material/Facebook';
import { auth } from '../utils/firebase';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';

const GradientBackground = styled(Box)(({ theme }) => ({
  position: 'relative',
  width: '100%',
  minHeight: '100vh',
  backgroundColor: '#f9f9f9',
  backgroundImage: `
    radial-gradient(circle at 70% 40%, rgba(255, 200, 100, 0.4), transparent 50%),
    radial-gradient(circle at 30% 70%, rgba(255, 100, 150, 0.3), transparent 50%),
    radial-gradient(circle at 90% 90%, rgba(100, 200, 255, 0.3), transparent 50%)
  `,
  backgroundRepeat: 'no-repeat',
  backgroundSize: 'cover',
}));

function SignUp() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const navigate = useNavigate();

  const handleSignUp = async () => {
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      alert("Account created successfully");
      navigate('/signin');
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <GradientBackground>
      <Container maxWidth="xs" sx={{ pt: 8 }}>
        <Box>
          <Typography sx={{textShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)'}} variant="h4" fontWeight="bold">Sign up</Typography>
          <TextField
            fullWidth
            margin="normal"
            label="Full name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            sx={{ background: 'white' }}
          />
          <TextField
            fullWidth
            margin="normal"
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            sx={{ background: 'white' }}
          />
          <TextField
            fullWidth
            margin="normal"
            type="password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{ background: 'white' }}
          />
          <Grid container alignItems="center">
            <Checkbox sx={{ padding: 1 }} />
            <Typography variant="body2">I want to receive updates via email.</Typography>
          </Grid>
          <Button
            fullWidth
            variant="contained"
            sx={{ mt: 2, mb: 1 }}
            onClick={handleSignUp}
          >
            Sign up
          </Button>
          <Typography align="center">or</Typography>
          <Button
            fullWidth
            startIcon={<GoogleIcon />}
            sx={{ mt: 2, background: 'white' }}
            variant="outlined"
          >
            Sign up with Google
          </Button>
          <Button
            fullWidth
            startIcon={<FacebookIcon />}
            sx={{ mt: 1, background: 'white' }}
            variant="outlined"
          >
            Sign up with Facebook
          </Button>
          <Typography align="center" sx={{ mt: 2 }}>
            Already have an account? <Link href="/signin">Sign in</Link>
          </Typography>
        </Box>
      </Container>
    </GradientBackground>
  );
}

export default SignUp;
