import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './login';
import {login} from "../../../api/common";
import { saveToken } from '../../../utils/auth';



const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate =useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please fill in all fields.');
      return;
    }

    if (!/\S+@\S+\.\S+/.test(email)) {
      setError('Invalid email format.');
      return;
    }
    try {
      const response = await login(email,password);
      console.log("API Response:", response);
      const {token} = response.data;
      saveToken(token);
      alert('Login Successful');
      navigate('/');
    }
    catch (error) {
      console.error("Login Failed: ", error);
      alert('Login Failed');

    }
    setEmail('');
    setPassword('');

  };
  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Login</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.inputContainer}>
          <label htmlFor="email" style={styles.label}>Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
            placeholder="Enter your email"
          />
        </div>
        <div style={styles.inputContainer}>
          <label htmlFor="password" style={styles.label}>Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
            placeholder="Enter your password"
          />
        </div>
        {error && <p style={styles.error}>{error}</p>}
        <button type="submit" style={styles.button}>Login</button>

        <a href="/signup">Create New account ?</a>
      </form>
    </div>
  );
};


export default Login;
