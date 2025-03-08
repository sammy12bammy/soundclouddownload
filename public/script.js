async function downloadSong() {
    const url = document.getElementById("urlInput").value;
    const statusElement = document.getElementById("output");
    const progressBar = document.getElementById("downloadProgress");

    if (!url) {
        statusElement.innerText = "Please enter a URL!";
        return;
    }

    statusElement.innerText = "Downloading...";
    progressBar.value = 1;  // Reset progress bar to 0

    try {
        // Send POST request to the server with the URL
        const response = await fetch("/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        // This is assuming you have some kind of response stream or progress updates.
        const result = await response.json();
        
        // If success, update the UI accordingly
        if (result.success) {
            statusElement.innerText = "Download complete!";
            progressBar.value = 100; // Set progress bar to 100% when done
        } else {
            statusElement.innerText = "Error: Could not download the song.";
        }
    } catch (error) {
        statusElement.innerText = "Error: Server not reachable.";
    }
}
