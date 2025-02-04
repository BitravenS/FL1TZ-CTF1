const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const router = express.Router();

const User = mongoose.model('User', new mongoose.Schema({
  username: { type: String, required: true },
  password: { type: String, required: true },
}));

router.use(express.json());

router.post('/login', async (req, res) => {
  const { username, password } = req.body;

  try {
    const user = await User.findOne({ username, password });

    if (user) {
      res.send(`<h1>Welcome, ${user.username}!</h1>`);
    } else {
      res.status(401).send('<h1>Invalid credentials</h1>');
    }
  } catch (err) {
    res.status(500).send('<h1>Internal Server Error</h1>');
  }
});

router.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../views/login.html'));
});

module.exports = router;
