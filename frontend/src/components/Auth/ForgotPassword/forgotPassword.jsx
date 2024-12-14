
import React, { useState } from 'react';
import styles from './forgotpassword';
import { SendOtp } from '../../../api/common';
import VerifyOtp from '../VerifyOtp/verifyOtp';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [showVerifyOtp, setShowVerifyOtp] = useState(false);

    const handleSendOTP = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await SendOtp(email);
            console.log(response);
            alert("OTP sent to email");
            setShowVerifyOtp(true); // Show VerifyOtp form after successful OTP generation
        } catch (error) {
            console.error("No user found:", error);
            alert('No user found');
        }
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.title}>Forgot Password</h1>
            <form style={styles.form} onSubmit={handleSendOTP}>
                <div style={styles.inputContainer}>
                    <label htmlFor="email" style={styles.label}>Email</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={styles.input}
                        placeholder="Enter your email"
                    />
                    <button type="submit" style={styles.button}>Send OTP</button>
                </div>
                {error && <p style={styles.error}>{error}</p>}
            </form>
            {showVerifyOtp && <VerifyOtp />} {/* Render VerifyOtp form conditionally */}
            <a href="/Login">Back to Login</a>
        </div>
    );
};

export default ForgotPassword;
