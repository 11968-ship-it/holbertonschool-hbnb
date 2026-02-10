/* =========================================================
   PAGE DETECTION
========================================================= */
function detectCurrentPage() {
  // Get the current page filename from the URL
  const path = window.location.pathname;
  const page = path.substring(path.lastIndexOf('/') + 1);
  
  // Remove .html extension and return page name
  if (page === 'login.html' || page === 'login') return 'login';
  if (page === 'place.html' || page === 'place') return 'place';
  if (page === 'add-review.html' || page === 'review') return 'review';
  if (page === 'index.html' || page === 'index' || page === '') return 'index';
  
  // Default to index if unknown
  return 'index';
}
/* =========================================================
   DOM READY
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
   // handle different pages
   const currentPage = detectCurrentPage();
   
   // Login page
   if (currentPage === 'login') {
      handleLoginForm();
   }
   
   // Index/Home page (places list)
   if (currentPage === 'index') {
      checkAuthentication();
      initPriceFilter();
      setupLogout();
   }
   
   // Place details page
   if (currentPage === 'place') {
      handleAuthUI();
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
      }

      // add review page
      if (currentPage === 'review'){
         handleAuthUI();
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
function checkAuthentication() {
   const token = getCookie('token');
   const loginLink = document.getElementById('login-link');
   const logoutBtn = document.getElementById('logout-btn');

   // Basic token validation (check if it exists and looks like a JWT)
   const isValidToken = token && token.split('.').length === 3;

   if (!isValidToken) {
      // user not authenticated: show login link, hide logout button
      if (loginLink) loginLink.style.display = 'block';
      if (logoutBtn) logoutBtn.style.display = 'none';
      
      // Clear invalid token
      if (token) {
         document.cookie = 'token=; path=/; max-age=0';
      }
   } else {
      // user IS authenticated: hide login link, show logout button
      if (loginLink) loginLink.style.display = 'none';
      if (logoutBtn) logoutBtn.style.display = 'block';
   }
   // ALWAYS fetch places, regardless of authentication
   // pass null if token is invalid
   fetchPlaces(isValidToken ? token : null);
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

/* =========================================================
   LOGOUT FUNCTIONALITY
========================================================= */
function setupLogout() {
   const logoutBtn = document.getElementById('logout-btn');
   if (!logoutBtn) return; // Exit if logout button doesn't exist on this page

   logoutBtn.addEventListener('click', (event) => {
      event.preventDefault();

      // clear the token cookie
      document.cookie = 'token=; path=/; max-age=0';

      // redirect to login page
      window.location.href = 'login.html';
   });
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

async function fetchPlaces(token) {
   try {
      const headers = {};
      if (token) headers["Authorization"] = `Bearer ${token}`;
      
      const res = await fetch("http://127.0.0.1:5000/api/v1/places", { headers });
      if (!res.ok) {
         throw new Error(`Failed to fetch places: ${res.status}`);
      }
      
      const places = await res.json();
      displayPlaces(Array.isArray(places) ? places : []);
   } catch (error) {
      console.error('Error fetching places:', error);

      //show error message to user
      const placesList = document.getElementById('places-list');
      if (placesList) {
         placesList.innerHTML = `
            <div class="error-message">
                <p>Failed to load places. Please try again later.</p>
                <button onclick="location.reload()">Retry</button>
            </div> 
         `;
      }
   }
}

function displayPlaces(places) {
  const list = document.getElementById("places-list");
  if (!list) return;

  list.innerHTML = "";

  const imgs = ["images/place-01.jpg", "images/place-02.jpg", "images/place-03.jpg"];

  places.forEach((place, idx) => {
    const card = document.createElement("article");
    card.className = "place-card";
    card.setAttribute("data-price", String(place.price ?? 0));

    const imgSrc = place.image_url || imgs[idx % imgs.length];

    card.innerHTML = `
      <div class="place-images">
        <img src="${imgSrc}" alt="Place Image">
      </div>
      <h3>${place.name ?? "Untitled place"}</h3>
      <p>Price per night:
        <img src="images/Saudi_Riyal_Symbol-1.png" alt="SAR symbol" class="currency-icon">
        ${place.price ?? "N/A"}
      </p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    list.appendChild(card);
  });

  // apply current slider filter to the new cards
  const priceRange = document.getElementById("price-range");
  if (priceRange) {
    const maxPrice = Number(priceRange.value);
    document.querySelectorAll(".place-card").forEach(card => {
      const p = Number(card.getAttribute("data-price") || 0);
      card.style.display = p <= maxPrice ? "" : "none";
    });
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
    const v = Number(priceRange.value);
    priceValue.textContent = formatSAR(v);
    setFill();
  }

  function getCardPrice(card) {
    // Best: put data-price on the card: <article class="place-card" data-price="220">
    const dp = card.getAttribute("data-price");
    if (dp) return Number(dp);

    // Fallback: last number in first <p>
    const text = card.querySelector("p")?.textContent || "";
    const match = text.match(/(\d+)\s*$/);
    return match ? Number(match[1]) : Infinity;
  }

  // Debounce for smooth drag
  let timer;
  function applyFilterDebounced() {
    clearTimeout(timer);
    timer = setTimeout(applyFilter, 80);
  }

  function applyFilter() {
    const maxPrice = Number(priceRange.value);
    document.querySelectorAll(".place-card").forEach((card) => {
      const price = getCardPrice(card);
      card.style.display = price <= maxPrice ? "" : "none";
    });
  }

  // Live behavior while dragging
  priceRange.addEventListener("input", () => {
    updateUI();
    applyFilterDebounced();
  });

  // Reset
  resetBtn?.addEventListener("click", () => {
    priceRange.value = String(DEFAULT_MAX);
    updateUI();
    applyFilter();
  });

  // Init
  updateUI();
  applyFilter();
}
