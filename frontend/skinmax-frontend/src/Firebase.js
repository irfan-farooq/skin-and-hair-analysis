import { initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
} from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBiIpxdW30SqE5MXShlj_ptLQnJHDOE3Ns",
  authDomain: "skinmax-45b82.firebaseapp.com",
  projectId: "skinmax-45b82",
  storageBucket: "skinmax-45b82.firebasestorage.app",
  messagingSenderId: "552096851905",
  appId: "1:552096851905:web:ab6892cb7b09a6faac3140",
  measurementId: "G-GH9J50ZNYV",
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

const provider = new GoogleAuthProvider();

export const loginWithGoogle = async () => {
  const result = await signInWithPopup(
    auth,
    provider
  );

  const token =
    await result.user.getIdToken();

  return {
    token,
    user: result.user,
  };
};

export const logoutUser = async () => {
  await signOut(auth);
};