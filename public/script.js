async function downloadSong() {
    const url = document.getElementById("urlInput").value;
    const statusElement = document.getElementById("output");

    if (!url) {
        statusElement.innerText = "Please enter a URL!";
        return;
    }

    statusElement.innerText = "Downloading...";

    try {
        const response = await fetch("/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        if (response.ok) {
            statusElement.innerText = "Download started! Check your default download folder.";
        } else {
            statusElement.innerText = "Error: Could not download the song.";
        }
    } catch (error) {
        statusElement.innerText = "Error: Server not reachable.";
    }
}
