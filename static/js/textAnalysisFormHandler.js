document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#analysisForm");
    const resultDiv = document.querySelector("#result");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();  // Prevent the default form submit action

        // Show "Work in progress..." text
        resultDiv.textContent = "Work in progress...";

        const formData = new FormData(form);

        const text = formData.get("text").trim();  // Trim whitespace
        if (!text) {
            resultDiv.textContent = "Please enter text for analysis.";
            return;
        }

        const data = {
            text: text,
            options: {
                sentiment: formData.get("sentiment") === "true",
                summary: formData.get("summary") === "true",
                keyword_extraction: formData.get("keyword_extraction") === "true"
            }
        };

        try {
            const response = await fetch("/analyze", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            let outputHtml = "<h2>Analysis Result:</h2>";

            if (response.ok) {
                const result = await response.json();
                const analysis = result.Result;

                if (analysis.sentiment) {
                    outputHtml += `<p><strong>Sentiment:</strong> ${analysis.sentiment}</p>`;
                }
                if (analysis.summary) {
                    outputHtml += `<p><strong>Summary:</strong> ${analysis.summary}</p>`;
                }
                if (analysis.score) {
                    outputHtml += `<p><strong>Score:</strong> ${analysis.score}</p>`;
                }
                if (analysis.keywords && analysis.keywords.length > 0) {
                    outputHtml += `<p><strong>Keywords:</strong> ${analysis.keywords.join(", ")}</p>`;
                }

                resultDiv.innerHTML = outputHtml;

            } else {
                const errorData = await response.json();
                const errorMessage = errorData.detail || "Unknown error";
                resultDiv.innerHTML = `Failed to analyze text. Reason: ${errorMessage}`;
            }

        } catch (err) {
            resultDiv.innerHTML = `An error occurred: ${err}`;
        }
    });
});
