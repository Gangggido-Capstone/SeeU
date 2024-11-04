import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// 외부에서 사용할 수 있도록 `sx`와 `sy`를 export로 정의
export let sx = parseInt(localStorage.getItem('x'), 10) || 0;
export let sy = parseInt(localStorage.getItem('y'), 10) || 0;

const SettingsPage = () => {
    const [localSX, setLocalSX] = useState(sx);
    const [localSY, setLocalSY] = useState(sy);
    const navigate = useNavigate();

    const handleXChange = (e) => {
        const intValue = parseInt(e.target.value, 10) || 0;
        setLocalSX(intValue);
        sx = intValue; // export된 변수 업데이트
    };

    const handleYChange = (e) => {
        const intValue = parseInt(e.target.value, 10) || 0;
        setLocalSY(intValue);
        sy = intValue; // export된 변수 업데이트
    };

    const handleHomeClick = () => {
        navigate('/');
    };

    useEffect(() => {
        localStorage.setItem('x', localSX);
    }, [localSX]);

    useEffect(() => {
        localStorage.setItem('y', localSY);
    }, [localSY]);

    return (
        <div style={styles.container}>
            <h1 style={styles.header}>Settings Page</h1>
            <form style={styles.form}>
                <div style={styles.inputGroup}>
                    <label htmlFor="x" style={styles.label}>X : </label>
                    <input 
                        type="number" 
                        id="x" 
                        value={localSX} 
                        onChange={handleXChange} 
                        style={styles.input}
                    />
                </div>
                <div style={styles.inputGroup}>
                    <label htmlFor="y" style={styles.label}>Y : </label>
                    <input 
                        type="number" 
                        id="y" 
                        value={localSY} 
                        onChange={handleYChange} 
                        style={styles.input}
                    />
                </div>
            </form>
            <p style={styles.output}> 저장된 X 값: {localSX}</p>
            <p style={styles.output}>저장된 Y 값: {localSY}</p>
            <button onClick={handleHomeClick} style={styles.button}>홈</button>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        backgroundColor: '#000', // 검정색 배경
        fontFamily: 'Arial, sans-serif',
        color: '#fff', // 텍스트 흰색
    },
    header: {
        fontSize: '2rem',
        marginBottom: '1.5rem',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '1rem',
        width: '100%',
        maxWidth: '400px',
        padding: '1.5rem',
        backgroundColor: '#333', // 폼 배경을 어두운 회색으로 설정
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
    },
    inputGroup: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        width: '100%',
    },
    label: {
        fontSize: '1rem',
        marginRight: '1rem',
        color: '#fff', // 레이블 텍스트 흰색
    },
    input: {
        flex: '1',
        padding: '0.5rem',
        fontSize: '1rem',
        borderRadius: '4px',
        border: '1px solid #555',
        backgroundColor: '#222', // 입력 필드 배경을 어두운 회색으로 설정
        color: '#fff', // 입력 텍스트 흰색
    },
    output: {
        fontSize: '1rem',
        marginTop: '1rem',
    },
    button: {
        marginTop: '2rem',
        padding: '0.75rem 1.5rem',
        fontSize: '1rem',
        color: '#fff', // 버튼 텍스트 흰색
        backgroundColor: '#ff0000', // 버튼 빨간색
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        transition: 'background-color 0.3s ease',
    },
};

export default SettingsPage;
