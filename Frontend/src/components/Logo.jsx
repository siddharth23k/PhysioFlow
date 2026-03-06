import * as React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function SitemarkIcon() {
  return (
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      <Typography variant="h5" component="div" sx={{ fontWeight: 'bold', color: '#c57196' }}>
        PhysioFlow
      </Typography>
    </Box>
  );
}
