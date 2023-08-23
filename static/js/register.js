document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const payload = {
            username: formData.get("username"),
            email: formData.get("email"),
            password: formData.get("password"),
        };


        const res = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        console.log("Data:", data);

        if (res.status === 201) {
            // Navigate to login page or show some success message
            window.location.href = "/login";
        } else {
            // Handle error
            if (data.detail && typeof data.detail === "object" && data.detail.error) {
                alert(data.detail.error);  // Changed how we access error detail
            } else if (typeof data.detail === "string") {
                alert(data.detail);
            } else {
                // Handle error
                console.log("Response Status: ", res.status);
                console.log("Response Data: ", data);
            }
        }
    });
});
