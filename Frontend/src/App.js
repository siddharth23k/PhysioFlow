import {BrowserRouter, Routes, Route} from 'react-router-dom';
import {Box, ThemeProvider, CssBaseline} from '@mui/material';
import HomePage from './components/HomePage';
import GroqAssistant from './components/GroqAssistant';
import theme from './theme'; // Import your theme
import Exercises from './components/Exercises';
import ImplementationPage from './components/ImplementationPage';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';


const App = () => (
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <BrowserRouter>
      <Box sx={{ backgroundColor: '#f0f2f5', minHeight: '100vh' }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chatbot" element={<GroqAssistant />}/>
          <Route path="/exercises" element={<Exercises />}/>
          <Route path="/implementation" element={<ImplementationPage />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
        </Routes>
      </Box>
    </BrowserRouter>
  </ThemeProvider>
);

export default App;