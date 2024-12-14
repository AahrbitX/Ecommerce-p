import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import styles from './verifyotp';
import { VerifyOTP } from "../../../api/common";

const VerifyOtp = () => {
    const [otp, setOtp] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleVerifyOtp = async (e) => {
        e.preventDefault();
        e.stopPropagation(); // Prevent the event from triggering other forms
        setError('');
        try {
            const response = await VerifyOTP(otp, newPassword);
            console.log(response);
            alert("Password changed successfully");
            navigate('/login/');
        } catch (error) {
            console.error("Wrong OTP:", error);
        }

        setNewPassword('');
        setOtp('');
    };

    return (
        <div style={styles.container}>
            <form style={styles.form} onSubmit={handleVerifyOtp}>
                <div style={styles.inputContainer}>
                    <label htmlFor="otp" style={styles.label}>OTP</label>
                    <input
                        type="text"
                        id="otp"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        style={styles.input}
                        placeholder="Enter your OTP"
                    />
                    <label htmlFor="newpassword" style={styles.label}>New Password</label>
                    <input
                        type="password"
                        id="newpassword"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        style={styles.input}
                        placeholder="Enter your new password"
                    />
                    <button type="submit" style={styles.button}>Verify & Confirm</button>
                </div>
                {error && <p style={styles.error}>{error}</p>}
            </form>
        </div>
    );
};

export default VerifyOtp;
