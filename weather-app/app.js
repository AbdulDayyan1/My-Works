const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000;

app.get('/weather', async (req, res) => {
    try {
        const response = await axios.get('https://weatherapi-com.p.rapidapi.com/forecast.json', {
            headers: {
                'x-rapidapi-host': 'weatherapi-com.p.rapidapi.com',
                'x-rapidapi-key': 'YOUR_RAPIDAPI_KEY'
            },
            params: {
                q: req.query.q || 'London', // Default location is London
                days: req.query.days || 3 // Default forecast for 3 days
            }
        });

        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
