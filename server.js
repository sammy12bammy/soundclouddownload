const express = require("express");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static("public")); // Serve static files (index.html, script.js)

app.post("/download", (req, res) => {
    const { url } = req.body;

    if (!url) {
        return res.status(400).json({ error: "No URL provided" });
    }

    const songsFolder = path.join(__dirname, "songs");
    if (!fs.existsSync(songsFolder)) {
        fs.mkdirSync(songsFolder, { recursive: true });
    }

    // Run Python script with the provided URL
    const process = spawn("python3", ["main.py", url]);

    process.stdout.on("data", (data) => {
        console.log(`stdout: ${data}`);
    });

    process.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
    });

    process.on("close", (code) => {
        if (code !== 0) {
            return res.status(500).json({ error: "Download failed" });
        }

        // Find the downloaded file dynamically
        fs.readdir(songsFolder, (err, files) => {
            if (err) {
                return res.status(500).json({ error: "Failed to find downloaded file." });
            }

            const mp3Files = files.filter(file => file.endsWith(".mp3"));
            if (mp3Files.length === 0) {
                return res.status(500).json({ error: "No MP3 file found." });
            }

            const downloadedFilePath = path.join(songsFolder, mp3Files[0]);
            res.download(downloadedFilePath, mp3Files[0]); // Send the file to frontend
        });
    });
});

app.listen(PORT, () => console.log(`Server running at http://localhost:${PORT}`));
