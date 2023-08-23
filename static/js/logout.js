document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logout-button");

    logoutButton.addEventListener("click", async () => {
        try {
            // Make an API call to your logout endpoint. This assumes you have a POST logout endpoint
            const response = await fetch("/logout", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            if (response.status === 200) {
                // If logout is successful, remove the access_token and navigate to the login page
                localStorage.removeItem('access_token');
                window.location.href = "/login";
            } else {
                // Handle errors
                console.error("Failed to log out");
            }
        } catch (error) {
            console.error("An error occurred:", error);
        }
    });
});
