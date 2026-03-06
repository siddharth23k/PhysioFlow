
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: ProcessingInstruction.env.firebase_apiKey,
  authDomain: ProcessingInstruction.env.firebase_authDomain,
  projectId: ProcessingInstruction.env.firebase_projectId,
  storageBucket: ProcessingInstruction.env.firebase_storageBucket,
  messagingSenderId: ProcessingInstruction.env.firebase_messagingSenderId,
  appId: ProcessingInstruction.env.firebase_appId,
  measurementId: ProcessingInstruction.env.firebase_measurementId,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
export const auth = getAuth(app);