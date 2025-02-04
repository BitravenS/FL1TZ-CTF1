const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const authRoutes = require('./routes/auth');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, 'public')));

const mongoUrl = process.env.MONGO_URL || 'mongodb://localhost:27017/ctf_challenge';

mongoose.connect(mongoUrl, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Failed to connect to MongoDB', err));

app.use('/', authRoutes);

app.listen(8083, '0.0.0.0', () => {
  console.log('Server running on http://0.0.0.0:8083');
});