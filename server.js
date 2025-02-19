const express = require("express");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static("public"));

app.post("/download", (req, res) => {
    const { url } = req.body;
    
    if (!url) {
        return res.status(400).json({ error: "No URL provided" });
    }

    // Run the Python script to download the song
    const command = `python3 main.py "${url}"`;  // Assuming `main.py` is downloading the file to the "songs" folder

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${stderr}`);
            return res.status(500).json({ error: "Download failed" });
        }

        // Assuming your Python script saves the file to the "songs" folder on the desktop
        const downloadedFilePath = path.join(get_desktop_path(), "songs", "song.mp3"); // Adjust file name or path as necessary

        // Check if the file exists before trying to download it
        if (fs.existsSync(downloadedFilePath)) {
            // Send the file to the client for download
            res.download(downloadedFilePath, "song.mp3", (err) => {
                if (err) {
                    console.error("Error during file download", err);
                    res.status(500).send("Error downloading the file.");
                }
            });
        } else {
            res.status(500).json({ error: "Downloaded file not found." });
        }
    });
});

app.listen(PORT, () => console.log(`Server running at http://localhost:${PORT}`));
