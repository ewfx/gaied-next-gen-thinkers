import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import emailjs from 'emailjs-com';
import { useNavigate } from 'react-router-dom';

const ServiceRequest = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: '',
        name: '',
        email: '',
        serviceDescription: '',
        files: []
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleFileChange = (e) => {
        setFormData({
            ...formData,
            files: [...formData.files, ...Array.from(e.target.files)]
        });
    };

    const handleRemoveFile = (index) => {
        const newFiles = formData.files.filter((_, i) => i !== index);
        setFormData({
            ...formData,
            files: newFiles
        });
    };

    const sendEmail = (e) => {
        e.preventDefault();

        const formDataToSend = {
            title: formData.title,
            name: formData.name,
            email: formData.email,
            serviceDescription: formData.serviceDescription,
            files: formData.files.map(file => ({
                name: file.name,
                size: file.size,
                type: file.type
            }))
        };

        console.log('formDataToSend:', formDataToSend);

        emailjs.send(
            'service_xjjo9so',  // Replace with your EmailJS Service ID
            "template_s3jgvkp", // Replace with your EmailJS Template ID
            formDataToSend,
            "6s_hVCd2ODYiZM1t1"      // Replace with your EmailJS User ID
        )
        .then((result) => {
            console.log('Email sent successfully:', result.text);
            navigate('/service-request-success');
        }, (error) => {
            console.error('Error sending email:', error.text);
        });
    };

    return (
        <div>
            <h1>Create Service Request</h1>
            <form onSubmit={sendEmail}>
                <div>
                    <TextField
                        label="Title"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <TextField
                        label="Name"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <TextField
                        label="Email"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <TextField
                        label="Service Description"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        multiline
                        rows={4}
                        name="serviceDescription"
                        value={formData.serviceDescription}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <input
                        accept="image/*"
                        style={{ display: 'none' }}
                        id="raised-button-file"
                        multiple
                        type="file"
                        onChange={handleFileChange}
                    />
                    {/* <label htmlFor="raised-button-file">
                        <Button variant="contained" color="primary" component="span">
                            Upload File
                        </Button>
                    </label> */}
                </div>
                <div>
                    {formData.files.length > 0 && (
                        <div>
                            <h3>Uploaded Files:</h3>
                            <ul style={{ listStyleType: 'none', padding: 0 }}>
                                {formData.files.map((file, index) => (
                                    <li key={index} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                        {file.name} ({(file.size / 1024).toFixed(2)} KB)
                                        <Button
                                            variant="outlined"
                                            color="secondary"
                                            onClick={() => handleRemoveFile(index)}
                                            style={{ marginLeft: '10px' }}
                                        >
                                            Remove
                                        </Button>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
                <div>
                    <Button variant="contained" color="primary" type="submit">
                        Submit
                    </Button>
                </div>
            </form>
        </div>
    );
};

export default ServiceRequest;