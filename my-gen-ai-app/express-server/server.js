import express from 'express';
import { readFile, writeFile } from 'fs';
import pkg from 'body-parser';
import cors from 'cors';

const { json } = pkg;

const app = express();
const port = 3000;
const dataFilePath = './data.json';

app.use(cors()); // Enable CORS
app.use(json());

// Endpoint to get data
app.get('/data', (req, res) => {
    readFile(dataFilePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Error reading data');
        }
        res.send(JSON.parse(data));
    });
});

// Endpoint to post data
app.post('/data', (req, res) => {
    const newData = req.body;
    writeFile(dataFilePath, JSON.stringify(newData, null, 2), (err) => {
        if (err) {
            return res.status(500).send('Error saving data');
        }
        res.send('Data saved successfully');
    });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});