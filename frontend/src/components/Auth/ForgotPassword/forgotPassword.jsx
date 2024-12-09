import React, { useState } from 'react'
import styles from './forgotpassword';
import { SendOtp} from '../../../api/common';
import VerifyOtp from '../VerifyOtp/verifyOtp';

const ForgotPassword = ()=>{

    const [email, setEmail] =useState('');
    const [error, setError] =useState('');
    const handleSendOTP = async (e) =>{
        e.preventDefault();
        setError('');
        try{
            const response = await SendOtp(email);
            console.log(response);
            alert("Otp Send to Email")
        }
        catch{
            console.error("No user Found: ", error);
            alert('No user Found');
        };
    }

    return (
        <div style={styles.container}>
            <h1 style={styles.title} >Forgot Password</h1>
        <form style={styles.form} onSubmit={handleSendOTP}>
            <div style={styles.inputContainer}>
                <label htmlFor="email" style={styles.label}></label>
                <input type='email' id='email' value={email} onChange={(e)=>setEmail(e.target.value)} style={styles.input} placeholder='Enter your email'></input>
                <button type='submit' style={styles.button}>Send OTP</button>
                <VerifyOtp/>
            </div>
            {error && <p style={styles.error}>{error}</p>}
        </form>
        <a href="/Login">Back to Login</a>
        </div>
    )
}

export default ForgotPassword