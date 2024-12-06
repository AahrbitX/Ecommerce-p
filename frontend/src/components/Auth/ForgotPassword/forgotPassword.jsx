import React, { useState } from 'react'
import styles from './forgotpassword';

const ForgotPassword = ()=>{

    const [email, setEmail] =useState('');
    const [otp, setOtp ] = useState('');
    const [otpResponse, setOtpResponse] =useState('');
    const [error, setError] =useState('');


    const handleSendOTP = async (e) =>{
        e.preventDefault();
        setError('')


        //// need to continue the logic of api caling.. ineedt to maintain tha seprate components;
    }




    return (
        <div>
            <h1>Forgot Password</h1>
        <form>
            <div>
                <label htmlFor="email" style={styles.label}></label>
                <input type='email' id='email' value={email} onChange={(e)=>setEmail(e.target.value)} style={styles.input} placeholder='Enter your email'></input>
                <button type='submit' style={styles.button}>Send OTP</button>
            </div>
            {error && <p style={styles.error}>{error}</p>}
        </form>
        <a href="/signup">Back to Login</a>
        </div>
    )
}

export default ForgotPassword