
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyDrJcDFfQtEZrDOLuxdDIyIRjLXf6jZ2Qs",
  authDomain: "physioflow-ai.firebaseapp.com",
  projectId: "physioflow-ai",
//   storageBucket: "physioflow-ai.firebasestorage.app",
//   messagingSenderId: "834301782859",
  appId: "1:834301782859:web:32ccf39a57a4b4b02416ce",
//   measurementId: "G-11LQY5LS0J"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
export const auth = getAuth(app);