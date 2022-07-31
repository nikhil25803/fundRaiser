const express  = require('express');
const connectDB  = require('./db/connectdb.js');
const webRoute = require('./routes/web');
const app = express();
const DATABASE_URL = process.env.DATABASE_URL || "mongodb://localhost:27017";

connectDB(DATABASE_URL);

// API JSON
app.use(express.json())

// Load Routes
app.use('/student', webRoute);


app.get('/', (req, res) => {
    console.log('Get method running');
})


app.listen(3000, () => {
    console.log('Server running');
})