/* =========================================================
   DOM READY
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
  handleLoginForm();
  handleAuthUI();
   initPriceFilter();

  const placeId = getPlaceIdFromURL();
  const placeSection = document.getElementById("place-details");

  if (!placeId) {
    if (placeSection) {
      placeSection.innerHTML = `<p>No place ID provided in the URL. Please go back to <a href="index.html">Home</a>.</p>`;
    }
    return;
  }

  const token = getCookie("token");
  fetchPlaceDetails(placeId, token);
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
  const cookies = document.cookie ? document.cookie.split("; ") : [];
  for (const cookie of cookies) {
    const eqIndex = cookie.indexOf("=");
    const rawKey = eqIndex === -1 ? cookie : cookie.slice(0, eqIndex);
    const rawVal = eqIndex === -1 ? "" : cookie.slice(eqIndex + 1);

    const key = decodeURIComponent(rawKey);
    if (key === name) return decodeURIComponent(rawVal);
  }
  return null;
}

/* =========================================================
   Place
========================================================= */
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id"); // expects URL like place.html?id=123
}
async function fetchPlaceDetails(placeId, token) {
  try {
    const headers = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: "GET",
      headers
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch place details: ${response.status}`);
    }

    const data = await response.json();
    displayPlaceDetails(data);
  } catch (error) {
    console.error(error);
    const placeSection = document.getElementById("place-details");
    if (placeSection) {
      placeSection.innerHTML = `<p>Failed to load place details.</p>`;
    }
  }
}

function displayPlaceDetails(place) {
  const placeSection = document.getElementById("place-details");
  if (!placeSection) return;

  placeSection.innerHTML = ""; // clear existing content

  // Name
  const nameEl = document.createElement("h1");
  nameEl.textContent = place.name;
  placeSection.appendChild(nameEl);

  // Description
  const descEl = document.createElement("p");
  descEl.textContent = place.description;
  placeSection.appendChild(descEl);

  // Price
  const priceEl = document.createElement("p");
  priceEl.innerHTML = `<strong>Price:</strong> $${place.price} per night`;
  placeSection.appendChild(priceEl);

  // Amenities
  if (place.amenities?.length) {
    const amenitiesTitle = document.createElement("h2");
    amenitiesTitle.textContent = "Amenities";
    placeSection.appendChild(amenitiesTitle);

    const ul = document.createElement("ul");
    ul.className = "amenities-list";
    place.amenities.forEach((amenity) => {
      const li = document.createElement("li");
      li.innerHTML = `<i class="fa fa-check"></i> ${amenity}`;
      ul.appendChild(li);
    });
    placeSection.appendChild(ul);
  }

  // Reviews
  if (place.reviews?.length) {
    const reviewsTitle = document.createElement("h2");
    reviewsTitle.textContent = "Reviews";
    placeSection.appendChild(reviewsTitle);

    place.reviews.forEach((review) => {
      const reviewCard = document.createElement("div");
      reviewCard.className = "review-card";
      reviewCard.innerHTML = `
        <p><strong>${review.user}</strong> rated <strong>${review.rating}/5</strong></p>
        <p>${review.comment}</p>
      `;
      placeSection.appendChild(reviewCard);
    });
  }
}

/* =========================================================
   PRICE RANGE FILTER
========================================================= */
function initPriceFilter() {
  const priceRange = document.getElementById("price-range");
  const priceValue = document.getElementById("price-value");
  const filterForm = document.getElementById("filter-form");

  if (!priceRange || !priceValue || !filterForm) return;

  function updatePriceLabel() {
    const v = Number(priceRange.value);
    priceValue.textContent = v === 3000 ? "3000+ SAR" : `${v} SAR`;
  }

  priceRange.addEventListener("input", updatePriceLabel);
  updatePriceLabel();

  filterForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const maxPrice = Number(priceRange.value);

    document.querySelectorAll(".place-card").forEach(card => {
      const text = card.querySelector("p")?.textContent || "";
      const match = text.match(/(\d+)\s*$/);
      const price = match ? Number(match[1]) : Infinity;

      card.style.display = price <= maxPrice ? "" : "none";
    });
  });
}
