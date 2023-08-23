document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Grabbing form data
        const formData = new FormData(form);

        // Assuming you need at least one of username or email
        const usernameOrEmail = formData.get("usernameOrEmail");

        // Preparing payload
        const payload = {
            username_or_email: usernameOrEmail,
            password: formData.get("password"),
        };

        console.log("Payload:", payload);  // Debugging line

        try {
            // Making the API call
            const res = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            console.log("Response Status:", res.status);  // Debugging line
            console.log("Response Object:", res);  // Debugging line

            // Parse JSON data from response
            const data = await res.json();
            console.log("Response Data:", data);  // Debugging line

            // Navigate if successful
            if (res.status === 200) {
                // We've received access_token, save it to the browser's local storage or session storage
                localStorage.setItem('access_token', data.access_token);

                // Make a fetch request to /app using the token in the Authorization header
                try {

                    const appResponse = await fetch("/app", {
                        headers: {
                            "Authorization": `Bearer ${data.access_token}`
                        }
                    });
                    
                    // Login successful
                    if (res.status === 200) {
                        // We've received access_token, save it to the browser's local storage or session storage
                        localStorage.setItem('access_token', data.access_token);
                        
                        // Navigate to /app
                        window.location.href = "/app";
                    } else {
                        alert(data.detail);
                    }

                } catch (error) {
                    console.error("An error occurred while fetching /app:", error);
                }
            } else {
                alert(data.detail);
            }
        } catch (error) {
            console.error("An error occurred:", error);  // Debugging line
        }
    });
});
