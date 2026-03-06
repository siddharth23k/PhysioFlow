import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import MenuItem from '@mui/material/MenuItem';
import Drawer from '@mui/material/Drawer';
import MenuIcon from '@mui/icons-material/Menu';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import Sitemark from './Logo';

const StyledToolbar = styled(Toolbar)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  flexShrink: 0,
  borderRadius: `calc(${theme.shape.borderRadius}px + 8px)`,
  backdropFilter: 'blur(24px)',
  border: '1px solid',
  borderColor: (theme.vars || theme).palette.divider,
  backgroundColor: theme.vars
    ? `rgba(${theme.vars.palette.background.defaultChannel} / 0.4)`
    : alpha(theme.palette.background.default, 0.4),
  boxShadow: (theme.vars || theme).shadows[1],
  padding: '8px 12px',
}));

export default function AppAppBar() {
  const [open, setOpen] = React.useState(false);

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

  return (
    <AppBar
      position="fixed"
      enableColorOnDark
      sx={{
        boxShadow: 0,
        bgcolor: 'transparent',
        backgroundImage: 'none',
        mt: 'calc(var(--template-frame-height, 0px) + 28px)',
      }}
    >
      <Container maxWidth="lg">
        <StyledToolbar variant="dense" disableGutters>
          <Box sx={{ display: 'flex', alignItems: 'center', px: 0 }}>
            <Sitemark />
            {/* Add spacing between logo and links */}
            <Box sx={{ width: 32 }} />
          </Box>
          {/* Center links */}
          <Box sx={{ 
            flexGrow: 1, 
            display: { xs: 'none', md: 'flex' }, 
            justifyContent: 'center',
            gap: 3 
          }}>
              <Button variant="text" size="small" sx={{ color: '#6e4670' }}>
                Home
              </Button>
              {/* <Button variant="text" size="small" sx={{ color: '#6e4670' }}>
                Dashboard
              </Button> */}
              <Button variant="text" size="small" sx={{ color: '#6e4670' }}>
                Groq Assistant
              </Button>
              <Button variant="text" size="small" sx={{ color: '#6e4670' }}>
                Exercises
              </Button>
              <Button variant="text" size="small" sx={{ color: '#6e4670' }}>
                About Us
              </Button>
              {/* <Button variant="text" size="small" sx={{ color: '#6e4670' }}>
                Feedback
              </Button> */}
            </Box>
          <Box
            sx={{
              display: { xs: 'none', md: 'flex' },
              gap: 2,
              alignItems: 'center',
              ml: 4, // Add margin left for spacing from middle links
            }}
          >
            <Button variant="text" size="small" sx={{ color: '#6e4670' }}>
              Sign in
            </Button>
            <Button variant="contained" size="small" sx={{ backgroundColor: '#6e4670' }}>
              Sign up
            </Button>
          </Box>
          <Box sx={{ display: { xs: 'flex', md: 'none' }, gap: 1 }}>
            <IconButton aria-label="Menu button" onClick={toggleDrawer(true)}>
              <MenuIcon />
            </IconButton>
            <Drawer
              anchor="top"
              open={open}
              onClose={toggleDrawer(false)}
              PaperProps={{
                sx: {
                  top: 'var(--template-frame-height, 0px)',
                },
              }}
            >
              <Box sx={{ p: 2, backgroundColor: 'background.default' }}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'flex-end',
                  }}
                >
                  <IconButton onClick={toggleDrawer(false)}>
                    <CloseRoundedIcon />
                  </IconButton>
                </Box>

                <MenuItem sx={{ color: '#6e4670' }}>Home</MenuItem>
                {/* <MenuItem>Dashboard</MenuItem> */}
                <MenuItem sx={{ color: '#6e4670' }}>Groq Assistant</MenuItem>
                <MenuItem sx={{ color: '#6e4670' }}>Exercises</MenuItem>
                <MenuItem sx={{ color: '#6e4670' }}>About Us</MenuItem>
                {/* <MenuItem>Feedback</MenuItem> */}
                <Divider sx={{ my: 3 }} />
                <MenuItem>
                  <Button variant="contained" fullWidth sx={{ backgroundColor: '#6e4670' }}>
                    Sign up
                  </Button>
                </MenuItem>
                <MenuItem>
                  <Button variant="outlined" fullWidth sx={{ color: '#6e4670' }}>
                    Sign in
                  </Button>
                </MenuItem>
              </Box>
            </Drawer>
          </Box>
        </StyledToolbar>
      </Container>
    </AppBar>
  );
}
