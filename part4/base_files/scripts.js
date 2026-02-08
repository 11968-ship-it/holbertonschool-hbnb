/* =========================================================
   DOM READY
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
  handleLoginForm();
  handleAuthUI();
});

/* =========================================================
   LOGIN FORM HANDLING
========================================================= */
function handleLoginForm() {
  const loginForm = document.getElementById("login-form");
  if (!loginForm) return;
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const errorEl = document.getElementById("login-error");
  const loginBtn = document.getElementById("login-btn");

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (errorEl) errorEl.textContent = "";

    const email = emailInput?.value.trim();
    const password = passwordInput?.value;

    if (!email || !password) {
      if (errorEl) {
        errorEl.textContent = "Please enter your email and password.";
      }
      return;
    }

    setLoginLoading(true, loginBtn);

    try {
      const token = await loginUser(email, password);
      setCookie("token", token, 7);
      window.location.href = "index.html";
    } catch (error) {
      if (errorEl) {
        errorEl.textContent = error.message || "Login failed.";
      }
    } finally {
      setLoginLoading(false, loginBtn);
    }
  });
}

function setLoginLoading(isLoading, button) {
  if (!button) return;
  button.disabled = isLoading;
  button.textContent = isLoading ? "Logging in..." : "Log in";
}

/* =========================================================
   API CALL
========================================================= */
async function loginUser(email, password) {
  const LOGIN_URL = "http://127.0.0.1:5000/api/v1/auth/login";

  const response = await fetch(LOGIN_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  });

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("Invalid server response");
  }

  if (!response.ok) {
    throw new Error(data?.message || "Invalid email or password");
  }

  const token = data.access_token || data.token || data.jwt;
  if (!token) {
    throw new Error("No token returned from server");
  }

  return token;
}

/* =========================================================
   AUTH UI (SHOW/HIDE ELEMENTS)
========================================================= */
function handleAuthUI() {
  const token = getCookie("token");

  const addReviewSection = document.getElementById("add-review-section");
  if (token && addReviewSection) {
    addReviewSection.style.display = "block";
  }
}

/* =========================================================
   COOKIE HELPERS
========================================================= */
function setCookie(name, value, days) {
  const maxAge = days ? `; max-age=${days * 24 * 60 * 60}` : "";
  const sameSite = "; samesite=lax";
  const secure = location.protocol === "https:" ? "; secure" : "";
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}${maxAge}; path=/${sameSite}${secure}`;
}

function getCookie(name) {
  const cookies = document.cookie.split("; ");
  for (const cookie of cookies) {
    const [key, value] = cookie.split("=");
    if (key === name) {
      return decodeURIComponent(value);
    }
  }
  return null;
}
