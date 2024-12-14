import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './signup';
import { SignUp } from '../../../api/common';


const Signup = () => {
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
      const response = await SignUp(email,password);
      console.log(response.data)
      alert('User Created Sucessfully');
      navigate('/login');
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
      <h2 style={styles.title}>Signup</h2>
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
        <button type="submit" style={styles.button}>Signup</button>

        <a href="/login">already have account ?</a>
      </form>
    </div>
  );
};


export default Signup;
