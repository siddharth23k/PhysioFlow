import React from 'react';
import { useState } from 'react';
import {
  Box, Button, Checkbox, Container, Grid, Link, styled, TextField, Typography
} from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';
import FacebookIcon from '@mui/icons-material/Facebook';
import { useNavigate } from 'react-router-dom';
import { auth } from '../utils/firebase';
import { signInWithEmailAndPassword } from 'firebase/auth';

const GradientBackground = styled(Box)(({ theme }) => ({
    position: 'relative',
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

function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignIn = async () => {
    try {
      await signInWithEmailAndPassword(auth, email, password);
      alert("Signed in successfully");
    } catch (err) {
      if (err.code === 'auth/user-not-found') {
        navigate('/signup');
      } else {
        alert(err.message);
      }
    }
  };

  return (
    <GradientBackground>
        <Container maxWidth="xs" >
            <Box >
            <Typography variant="h4" fontWeight="bold" sx={{ pt: 8, textShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)' }}>Sign in</Typography>
            <TextField sx={{ background: 'white' }} fullWidth margin="normal" label="Email" value={email}
                onChange={(e) => setEmail(e.target.value)} />
            <TextField sx={{ background: 'white' }} fullWidth margin="normal" type="password" label="Password"
                value={password} onChange={(e) => setPassword(e.target.value)} />
            <Grid container alignItems="center">
                <Checkbox sx={{ padding: 1 }} />
                <Typography variant="body2">Remember me</Typography>
            </Grid>
            <Button fullWidth variant="contained" sx={{ mt: 2, mb: 1 }} onClick={handleSignIn}>
                Sign in
            </Button>
            <Link href="#" variant="body2" sx={{ display: 'block', m: 2 }}>
                Forgot your password?
            </Link>
            <Typography align="center">or</Typography>
            <Button fullWidth startIcon={<GoogleIcon />} sx={{ mt: 2, background: 'white'}} variant="outlined">
                Sign in with Google
            </Button>
            <Button fullWidth startIcon={<FacebookIcon />} sx={{ mt: 1, background: 'white' }} variant="outlined">
                Sign in with Facebook
            </Button>
            <Typography align="center" sx={{ mt: 2 }}>
                Don't have an account? <Link href="/signup">Sign up</Link>
            </Typography>
            </Box>
        </Container>
    </GradientBackground>
  );
}

export default SignIn;
