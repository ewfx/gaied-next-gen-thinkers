import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const ServiceRequestSuccess = () => {
    const navigate = useNavigate();

    const handleBackToHome = () => {
        navigate('/');
    };

    return (
        <Container style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', textAlign: 'center', padding: '24px' }}>
            <Box>
                <Typography variant="h4" style={{ marginBottom: '16px' }}>
                    Your service request has been successfully created.
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '32px' }}>
                    Our team is analyzing your request and will get back to you soon.
                </Typography>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleBackToHome}
                >
                    Back to Home
                </Button>
            </Box>
        </Container>
    );
};

export default ServiceRequestSuccess;