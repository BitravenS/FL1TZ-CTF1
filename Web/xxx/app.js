const express = require('express');
const xpath = require('xpath');
const dom = require('xmldom').DOMParser;
const fs = require('fs');
const path = require('path');
const app = express();
const port = 8080;

app.use(express.static('public'));

let xml;
try {
    xml = fs.readFileSync('./var/tmp/export.xml', 'utf8'); 
} catch (e) {
    console.error('Error reading XML file:', e.message);
    process.exit(1);
}
const doc = new dom().parseFromString(xml);

app.get('/showalbum', async (req, res) => {
    const albumName = req.query.album;
    if (!albumName) {
        return res.status(400).send('Album name is required.');
    }

    try {
        const nodes = xpath.select(`/albums/album[name='${albumName}']/tracks/track/title/text()`, doc);

        if (nodes.length === 0) {
            return res.sendFile(path.join(__dirname, 'public', 'index.html'));
        }

        let responseHtml = `
            <html>
            <head>
                <link rel="stylesheet" href="/styles.css">
            </head>
            <body>
                <h1>Tracklist for "${albumName}"</h1>
                <ul>
        `;
        nodes.forEach((n) => (responseHtml += `<li>${n.toString()}</li>`));
        responseHtml += `
                </ul>
                <a href="/">Search another album</a>
            </body>
            </html>
        `;
        res.send(responseHtml);
    } catch (e) {
        console.error('Error processing XPath query:', e.message);
        res.status(500).send('Internal Server Error');
    }
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Listening on http://localhost:1027}`);
});
