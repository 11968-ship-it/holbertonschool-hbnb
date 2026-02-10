const API_BASE_URL = "http://127.0.0.1:5500/api/v1";

/* =========================================================
   PAGE DETECTION
========================================================= */
function detectCurrentPage() {
  const path = window.location.pathname;
  const page = path.substring(path.lastIndexOf('/') + 1);

  if (page === 'login.html' || page === 'login') return 'login';
  if (page === 'place.html' || page === 'place') return 'place';
  if (page === 'add-review.html' || page === 'review') return 'review';
  if (page === 'index.html' || page === 'index' || page === '') return 'index';

  return 'index';
}

/* =========================================================
   DOM READY
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
  const currentPage = detectCurrentPage();

  if (currentPage === 'login') handleLoginForm();

  if (currentPage === 'index') {
    checkAuthentication();
    initPriceFilter();
    setupLogout();
  }

  if (currentPage === 'place') {
    const placeId = getPlaceIdFromURL();
    handleAuthUI();
    setupAddReviewForm();

    if (!placeId) {
      const placeSection = document.getElementById("place-details");
      if (placeSection) {
        placeSection.innerHTML = `<p>No place ID provided in the URL. Please go back to <a href="index.html">Home</a>.</p>`;
      }
      return;
    }

    const token = getCookie("token");
    fetchPlaceDetails(placeId, token);
  }

  if (currentPage === 'review') {
    handleAuthUI();
    setupAddReviewForm();
  }
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
      if (errorEl) errorEl.textContent = "Please enter your email and password.";
      return;
    }

    setLoginLoading(true, loginBtn);

    try {
      const token = await loginUser(email, password);
      setCookie("token", token, 7);
      window.location.href = "index.html";
    } catch (error) {
      if (errorEl) errorEl.textContent = error.message || "Login failed.";
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
  const LOGIN_URL = `${API_BASE_URL}/auth/login`;

  const response = await fetch(LOGIN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("Invalid server response");
  }

  if (!response.ok) throw new Error(data?.message || "Invalid email or password");

  const token = data.access_token || data.token || data.jwt;
  if (!token) throw new Error("No token returned from server");

  return token;
}

/* =========================================================
   AUTH UI (SHOW/HIDE ELEMENTS)
========================================================= */
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.querySelector('.login-button');
  const logoutBtn = document.getElementById('logout-btn');

  const isValidToken = token && token.split('.').length === 3;

  if (!isValidToken) {
    if (loginLink) loginLink.style.display = 'block';
    if (logoutBtn) logoutBtn.style.display = 'none';
    if (token) document.cookie = 'token=; path=/; max-age=0';
  } else {
    if (loginLink) loginLink.style.display = 'none';
    if (logoutBtn) logoutBtn.style.display = 'block';
  }

  fetchPlaces(isValidToken ? token : null);
}

function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split("; ") : [];
  for (const cookie of cookies) {
    const eqIndex = cookie.indexOf("=");
    const rawKey = eqIndex === -1 ? cookie : cookie.slice(0, eqIndex);
    const rawVal = eqIndex === -1 ? "" : cookie.slice(eqIndex + 1);
    if (decodeURIComponent(rawKey) === name) return decodeURIComponent(rawVal);
  }
  return null;
}

function handleAuthUI() {
  const token = getCookie("token");
  const addReviewSection = document.getElementById("add-review");
  if (token && addReviewSection) addReviewSection.style.display = "block";
  else if (addReviewSection) addReviewSection.style.display = "none";
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

/* =========================================================
   LOGOUT FUNCTIONALITY
========================================================= */
function setupLogout() {
  const logoutBtn = document.getElementById('logout-btn');
  if (!logoutBtn) return;

  logoutBtn.addEventListener('click', (event) => {
    event.preventDefault();
    document.cookie = 'token=; path=/; max-age=0';
    window.location.reload();
  });
}

/* =========================================================
   PLACE DETAILS
========================================================= */
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

async function fetchPlaceDetails(placeId, token) {
  try {
    const headers = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
      method: "GET",
      headers
    });

    if (!response.ok) throw new Error(`Failed to fetch place details: ${response.status}`);

    const data = await response.json();
    displayPlaceDetails(data);
  } catch (error) {
    console.error(error);
    const placeSection = document.getElementById("place-details");
    if (placeSection) placeSection.innerHTML = `<p>Failed to load place details.</p>`;
  }
}

/* =========================================================
   FETCH PLACES
========================================================= */
async function fetchPlaces(token) {
  try {
    const headers = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE_URL}/places/`, { headers });
    if (!res.ok) throw new Error(`Failed to fetch places: ${res.status}`);

    const places = await res.json();
    displayPlaces(Array.isArray(places) ? places : []);
  } catch (error) {
    console.error('Error fetching places:', error);
    const placesList = document.getElementById('places-list');
    if (placesList) {
      placesList.innerHTML = `
        <div class="error-message">
          <p>Failed to load places. Please try again later.</p>
          <button onclick="location.reload()">Retry</button>
        </div>`;
    }
  }
}

/* =========================================================
   DISPLAY PLACE DETAILS
========================================================= */
function displayPlaceDetails(place) {
  const placeSection = document.getElementById("place-details");
  if (!placeSection) return;
  placeSection.innerHTML = "";

  const nameEl = document.createElement("h1");
  nameEl.textContent = place.name;
  placeSection.appendChild(nameEl);

  const descEl = document.createElement("p");
  descEl.textContent = place.description;
  placeSection.appendChild(descEl);

  const priceEl = document.createElement("p");
  priceEl.innerHTML = `<strong>Price:</strong> $${place.price} per night`;
  placeSection.appendChild(priceEl);

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

  if (place.reviews?.length) {
    const reviewsTitle = document.createElement("h2");
    reviewsTitle.textContent = "Reviews";
    placeSection.appendChild(reviewsTitle);

    place.reviews.forEach((review) => {
      const reviewCard = document.createElement("div");
      reviewCard.className = "review-card";
      reviewCard.innerHTML = `
        <p><strong>${review.user}</strong> rated <strong>${review.rating}/5</strong></p>
        <p>${review.comment}</p>`;
      placeSection.appendChild(reviewCard);
    });
  }
}

/* =========================================================
   ADD REVIEW FORM
========================================================= */
function setupAddReviewForm() {
  const form = document.getElementById("review-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = getCookie("token");
    if (!token) return alert("You must be logged in to submit a review.");

    const placeId = getPlaceIdFromURL();
    const rating = form.querySelector("#review-rating")?.value || 5;
    const comment = form.querySelector("#review-text")?.value;

    if (!comment) return alert("Please enter a review.");

    try {
      const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ rating, comment })
      });

      if (!response.ok) throw new Error("Failed to submit review");

      alert("Review submitted successfully!");
      fetchPlaceDetails(placeId, token);
      form.reset();
    } catch (err) {
      console.error(err);
      alert(err.message || "Error submitting review");
    }
  });
}

/* =========================================================
   PRICE RANGE FILTER
========================================================= */
function initPriceFilter() {
  const priceRange = document.getElementById("price-range");
  const priceValue = document.getElementById("price-value");
  const resetBtn = document.getElementById("price-reset");
  if (!priceRange || !priceValue) return;

  const DEFAULT_MAX = Number(priceRange.value);

  function formatSAR(v) {
    const max = Number(priceRange.max);
    const text = v.toLocaleString("en-US");
    return v === max ? `${text}+ SAR` : `${text} SAR`;
  }

  function setFill() {
    const min = Number(priceRange.min);
    const max = Number(priceRange.max);
    const val = Number(priceRange.value);
    const pct = ((val - min) / (max - min)) * 100;
    priceRange.style.setProperty("--fill", `${pct}%`);
  }

  function updateUI() {
    priceValue.textContent = formatSAR(Number(priceRange.value));
    setFill();
  }

  function getCardPrice(card) {
    const dp = card.getAttribute("data-price");
    return dp ? Number(dp) : Infinity;
  }

  let timer;
  function applyFilterDebounced() {
    clearTimeout(timer);
    timer = setTimeout(applyFilter, 80);
  }

  function applyFilter() {
    const maxPrice = Number(priceRange.value);
    document.querySelectorAll(".place-card").forEach(card => {
      const price = getCardPrice(card);
      card.style.display = price <= maxPrice ? "" : "none";
    });
  }

  priceRange.addEventListener("input", () => {
    updateUI();
    applyFilterDebounced();
  });

  resetBtn?.addEventListener("click", () => {
    priceRange.value = String(DEFAULT_MAX);
    updateUI();
    applyFilter();
  });

  updateUI();
  applyFilter();
}
