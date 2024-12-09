import React, {useState} from "react";
import { useNavigate } from 'react-router-dom';
import styles from './verifyotp';
import { VerifyOTP } from "../../../api/common";


const VerifyOtp = ()=> {

    const [otp, setOtp ] = useState('');
    const [newPassword, setNewPassword] =useState('');
    const [error, setError] =useState('');

    const navigate=useNavigate();


    const handleVerifyOtp = async (e)=>{
        e.preventDefault();
        setError('');
        try{
            const response = await VerifyOTP(otp,newPassword);
            console.log(response);  
            alert("password changed sucessfully");
            navigate('/login/');
        }
        catch(error){
         console.error("Worng otp:" ,error)   
        }

        setNewPassword('');
        setOtp('');

    }


    return(
        <div style={styles.container}>
        <from style={styles.form}  onSubmit={handleVerifyOtp}>
            <div style={styles.inputContainer}>
                <label htmlFor="otp" style={styles.label}></label>
                <input type="text" id='otp' value={otp} onChange={(e)=>setOtp(e.target.value)} style={styles.input} placeholder='Enter your OTP' />
                <label htmlFor="newpassword" style={styles.label}></label>
                <input type="password" id='newpassword' value={newPassword} onChange={(e)=>setNewPassword(e.target.value)} style={styles.input} placeholder='Enter your new password' />
                <button type="submit"  style={styles.button}>Verify & Confirm </button>
            </div>
            {error && <p style={styles.error}>{error}</p>}
        </from>
        </div>
    )

}


export default VerifyOtp;

