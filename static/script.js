document.addEventListener("DOMContentLoaded", function () {
    const scanBtn = document.getElementById("scanBtn");
    scanBtn.addEventListener("click", analyzeURL);
});

async function analyzeURL() {
    const urlInput = document.getElementById("urlInput");
    const loader = document.getElementById("loader");
    const resultBox = document.getElementById("resultBox");

    const urlValue = urlInput.value.trim();

    if (!urlValue) {
        alert("Please enter a URL first!");
        return;
    }

    loader.style.display = "block";
    resultBox.style.display = "none";

    try {
        const response = await fetch("/api/url-check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: urlValue })
        });

        const data = await response.json();

        if (response.ok) {
            const verdictSpan = document.getElementById("resVerdict");
            
            // Format text and apply status class from styles.css
            verdictSpan.innerText = data.verdict;
            if (data.is_phishing) {
                verdictSpan.className = "badge-danger";
            } else {
                verdictSpan.className = "badge-safe";
            }

            document.getElementById("resTarget").innerText = data.target_url;
            document.getElementById("resRisk").innerText = data.risk_score + "%";
            document.getElementById("resHttps").innerText = data.details.has_https ? "Yes" : "No";

            resultBox.style.display = "block";
        } else {
            alert("Error: " + (data.error || "Failed to analyze URL"));
        }
    } catch (error) {
        alert("Server connection failed. Ensure your Flask server is running.");
    } finally {
        loader.style.display = "none";
    }
}