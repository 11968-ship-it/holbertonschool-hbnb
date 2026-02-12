const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';
let ALL_PLACES = [];

/* =========================================================
   PAGE DETECTION
========================================================= */
function detectCurrentPage() {
  const path = window.location.pathname;
  const page = path.substring(path.lastIndexOf('/') + 1);
   
   if (page === 'login.html' || page === 'login') return 'login';
   if (page === 'signup.html' || page === 'signup') return 'signup';
   if (page === 'place.html' || page === 'place') return 'place';
   if (page === 'add_review.html' || page === 'review') return 'review';
   if (page === 'add_place.html' || page === 'add_place') return 'add_place';
   if (page === 'index.html' || page === 'index' || page === '') return 'index';

  return 'index';
}

/* =========================================================
   DOM READY
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
  const currentPage = detectCurrentPage();

  // --- MAIN PAGE LOGIC ---
  if (currentPage === 'login') handleLoginForm();
  if (currentPage === 'signup') handleSignupForm();
  
  if (currentPage === 'add_place') {
    const token = getCookie("token");
    if (!token) {
      window.location.href = "index.html";
      return;
    }
    setupLogout();
    handleAddPlaceForm();
  }
  
  if (currentPage === 'index') {
    checkAuthentication();
    initPriceFilter();
    setupLogout();
    populateLocationDatalist();
    setupIndexSearch();
  }

  if (currentPage === 'place') {
  const placeId = getPlaceIdFromURL();

  // Show/hide Login vs Logout in the header
  const token = getCookie("token");
  const loginLink = document.querySelector(".login-button");
  const logoutBtn = document.getElementById("logout-btn");
  if (token) {
    if (loginLink) loginLink.style.display = "none";
    if (logoutBtn) logoutBtn.style.display = "inline-block";
  } else {
    if (loginLink) loginLink.style.display = "inline-block";
    if (logoutBtn) logoutBtn.style.display = "none";
  }

  setupLogout();


/* ==================================
              addReview
====================================
*/

  const addReviewSection = document.getElementById("add-review");
  const addReviewLink = document.getElementById("add-review-link");
  if (token && addReviewSection && addReviewLink && placeId) {
    addReviewSection.style.display = "block";
    addReviewLink.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
  } else if (addReviewSection) {
    addReviewSection.style.display = "none";
  }

  if (!placeId) {
    const placeSection = document.getElementById("place-details");
    if (placeSection) {
      placeSection.innerHTML = `<p>No place ID provided in the URL. Please go back to <a href="index.html">Home</a>.</p>`;
    }
    return;
  }

  fetchPlaceDetails(placeId, token);
}

   if (currentPage === 'review') {
  const token = getCookie("token");
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    window.location.href = "index.html";
    return;
  }

  setupLogout();
  loadReviewPlacePreview(placeId);   // 🔥 THIS loads the image
  setupAddReviewForm();
}

   if (currentPage === 'add_place') {
  const token = getCookie("token");
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  setupLogout();
}
});

 // --- MODAL CLOSE BUTTON ---
  const closeBtn = document.querySelector(".modal-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      window.location.href = "index.html";
    });
  }
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
   SIGNUP FORM HANDLING
========================================================= */
function handleSignupForm() {
  const signupForm = document.getElementById("signup-form");
  if (!signupForm) return;

  const firstNameInput = document.getElementById("first_name");
  const lastNameInput = document.getElementById("last_name");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const errorEl = document.getElementById("error-message");
  const signupBtn = document.getElementById("signup-btn");

  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (errorEl) errorEl.textContent = "";

    // Get form values
    const firstName = firstNameInput?.value.trim();
    const lastName = lastNameInput?.value.trim();
    const email = emailInput?.value.trim();
    const password = passwordInput?.value;

    // Validation
    if (!firstName || !lastName || !email || !password) {
      if (errorEl) errorEl.textContent = "All fields are required.";
      return;
    }

    if (password.length < 6) {
      if (errorEl) errorEl.textContent = "Password must be at least 6 characters.";
      return;
    }

    // Email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      if (errorEl) errorEl.textContent = "Please enter a valid email address.";
      return;
    }

    setSignupLoading(true, signupBtn);

    try {
      await registerUser(firstName, lastName, email, password);
      
      // Show success message
      alert("Account created successfully! Please login.");
      
      // Redirect to login page
      window.location.href = "login.html";
    } catch (error) {
      if (errorEl) {
        errorEl.textContent = error.message || "Registration failed. Please try again.";
      }
    } finally {
      setSignupLoading(false, signupBtn);
    }
  });
}

function setSignupLoading(isLoading, button) {
  if (!button) return;
  button.disabled = isLoading;
  button.classList.toggle('loading', isLoading);
  button.textContent = isLoading ? "Creating Account..." : "Create Account";
}
/* =========================================================
   ADD PLACE FORM HANDLING
========================================================= */
function handleAddPlaceForm() {
  const addPlaceForm = document.getElementById("add-place-form");
  if (!addPlaceForm) return;

  const token = getCookie("token");
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  const titleInput = document.getElementById("title");
  const descriptionInput = document.getElementById("description");
  const priceInput = document.getElementById("price");
  const latitudeInput = document.getElementById("latitude");
  const longitudeInput = document.getElementById("longitude");
  const errorEl = document.getElementById("error-message");
  const addPlaceBtn = document.getElementById("add-place-btn");

  addPlaceForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (errorEl) errorEl.textContent = "";

    // Get form values
    const title = titleInput?.value.trim();
    const description = descriptionInput?.value.trim();
    const price = parseFloat(priceInput?.value);
    const latitude = parseFloat(latitudeInput?.value);
    const longitude = parseFloat(longitudeInput?.value);

    // Validation
    if (!title || !description || !price || !latitude || !longitude) {
      if (errorEl) errorEl.textContent = "All fields are required.";
      return;
    }

    if (price <= 0) {
      if (errorEl) errorEl.textContent = "Price must be greater than 0.";
      return;
    }

    if (latitude < -90 || latitude > 90) {
      if (errorEl) errorEl.textContent = "Latitude must be between -90 and 90.";
      return;
    }

    if (longitude < -180 || longitude > 180) {
      if (errorEl) errorEl.textContent = "Longitude must be between -180 and 180.";
      return;
    }

    setAddPlaceLoading(true, addPlaceBtn);

    try {
      const placeData = await createPlace(token, {
        title,
        description,
        price,
        latitude,
        longitude
      });
      
      // Show success message
      alert("Place created successfully!");
      
      // Redirect to home page
      window.location.href = "index.html";
    } catch (error) {
      if (errorEl) {
        errorEl.textContent = error.message || "Failed to create place. Please try again.";
      }
    } finally {
      setAddPlaceLoading(false, addPlaceBtn);
    }
  });
}

function setAddPlaceLoading(isLoading, button) {
  if (!button) return;
  button.disabled = isLoading;
  button.classList.toggle('loading', isLoading);
  button.textContent = isLoading ? "Creating..." : "Create Place";
}

async function createPlace(token, placeData) {
  const CREATE_PLACE_URL = `${API_BASE_URL}/places/`;

  const response = await fetch(CREATE_PLACE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(placeData)
  });

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("Invalid server response");
  }

  if (!response.ok) {
    throw new Error(data?.error || data?.message || "Failed to create place");
  }

  return data;
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

async function registerUser(firstName, lastName, email, password) {
  const SIGNUP_URL = `${API_BASE_URL}/auth/signup`;

  const response = await fetch(SIGNUP_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password
    })
  });

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("Invalid server response");
  }

  // Handle different error responses from Flask-RESTX
  if (!response.ok) {
    if (response.status === 409) {
      throw new Error("Email already registered. Please login instead.");
    }
    throw new Error(data?.error || data?.message || "Registration failed");
  }

  return data; // Returns { id, email, first_name, last_name }
}

/* =========================================================
               AUTH UI (SHOW/HIDE ELEMENTS)
========================================================= */
function checkAuthentication() {
  const token = getCookie("token");

  const signupLink = document.getElementById("signup-link");
  const loginLink  = document.getElementById("login-link");
  const createLink = document.getElementById("create-place-link");
  const logoutBtn  = document.getElementById("logout-btn");

  const isValidToken = token && token.split(".").length === 3;

  if (isValidToken) {
    if (signupLink) signupLink.style.display = "none";
    if (loginLink)  loginLink.style.display = "none";
    if (createLink) createLink.style.display = "inline-block";
    if (logoutBtn)  logoutBtn.style.display = "inline-block";
  } else {
    if (signupLink) signupLink.style.display = "inline-block";
    if (loginLink)  loginLink.style.display = "inline-block";
    if (createLink) createLink.style.display = "none";
    if (logoutBtn)  logoutBtn.style.display = "none";

    // clear bad token if present
    if (token) document.cookie = "token=; path=/; max-age=0";
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
     ALL_PLACES = Array.isArray(places) ? places : [];
     displayPlaces(ALL_PLACES);
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

/* =============================================
                Searching bar
================================================ */

function setupIndexSearch() {
  const form = document.getElementById("filter-form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const location = document.getElementById("location")?.value.trim().toLowerCase();
    const guests = Number(document.getElementById("guests")?.value || 0);
    const maxPrice = Number(document.getElementById("price-range")?.value || Infinity);

    const filtered = ALL_PLACES.filter((p) => {
      const name = String(p.name ?? "").toLowerCase();
      const desc = String(p.description ?? "").toLowerCase();
      const price = Number(p.price ?? Infinity);

      const matchesLocation =
        !location ||
        name.includes(location) ||
        desc.includes(location);

      const matchesPrice = price <= maxPrice;

      const maxGuests = Number(p.max_guests ?? 0);
      const matchesGuests = !guests || (maxGuests >= guests);

       // Date filter
  let matchesDate = true;
  const checkInInput = document.getElementById("check-in")?.value;
  const checkOutInput = document.getElementById("check-out")?.value;
  if (checkInInput && checkOutInput && p.available_from && p.available_to) {
    const checkIn = new Date(checkInInput);
    const checkOut = new Date(checkOutInput);
    const availableFrom = new Date(p.available_from);
    const availableTo = new Date(p.available_to);
    matchesDate = availableFrom <= checkIn && availableTo >= checkOut;
  }
       
      return matchesLocation && matchesPrice && matchesGuests;
    });

    displayPlaces(filtered);
    initPriceFilter(); // re-apply slider visuals
  });
}

/* =========================================================
                 DISPLAY PLACE DETAILS
========================================================= */
function displayPlaceDetails(place) {
  const placeSection = document.getElementById("place-details");
  if (!placeSection) return;

  placeSection.innerHTML = "";

  // === IMAGES ===
  const images = getPlaceImages(place);
  const imagesContainer = document.createElement("div");
  imagesContainer.className = "place-images";

  images.forEach((src) => {
    const img = document.createElement("img");
    img.src = src;
    img.alt = place.name || "Place image";
    imagesContainer.appendChild(img);
  });

  placeSection.appendChild(imagesContainer);

  // === INFO ===
  const infoDiv = document.createElement("div");
  infoDiv.className = "place-info";
  infoDiv.innerHTML = `
    <h1>${escapeHtml(place.name ?? "Unnamed place")}</h1>
    <p>${escapeHtml(place.description ?? "")}</p>
    <p><strong>Price:</strong> ${formatPrice(place.price)}</p>
  `;
  placeSection.appendChild(infoDiv);

  // === AMENITIES ===
  if (place.amenities?.length) {
    const amenitiesTitle = document.createElement("h2");
    amenitiesTitle.textContent = "Amenities";
    placeSection.appendChild(amenitiesTitle);

    const ul = document.createElement("ul");
    ul.className = "amenities-list";

    place.amenities.forEach((amenity) => {
      const li = document.createElement("li");
      li.innerHTML = `<i class="fa fa-check"></i> ${escapeHtml(amenity)}`;
      ul.appendChild(li);
    });

    placeSection.appendChild(ul);
  }

  // === REVIEWS ===
  if (place.reviews?.length) {
    const reviewsTitle = document.createElement("h2");
    reviewsTitle.textContent = "Reviews";
    placeSection.appendChild(reviewsTitle);

    place.reviews.forEach((review) => {
      const reviewCard = document.createElement("div");
      reviewCard.className = "review-card";
      reviewCard.innerHTML = `
        <p><strong>${escapeHtml(review.user ?? "User")}</strong> rated <strong>${review.rating ?? "?"}/5</strong></p>
        <p>${escapeHtml(review.comment ?? "")}</p>
      `;
      placeSection.appendChild(reviewCard);
    });
  }
}

function getFallbackImage(place) {
  const imgs = ["images/place-01.jpg", "images/place-02.jpg", "images/place-03.jpg"];
  const id = String(place.id || "");
  const idx = id.length ? (id.charCodeAt(id.length - 1) % imgs.length) : 0;
  return imgs[idx];
}

function getPlaceImages(place) {
  // If API sends an array:
  if (Array.isArray(place?.images) && place.images.length) return place.images;
  if (Array.isArray(place?.photos) && place.photos.length) return place.photos;

  // If API sends single image:
  if (place?.image_url) return [place.image_url];

  // Otherwise: fallbacks
  return [getFallbackImage(place), "images/place-02.jpg"];
}

function getPlaceCardImage(place) {
  // for index page thumbnail (just 1 image)
  const imgs = getPlaceImages(place);
  return imgs[0];
}

/* =========================================================
              ADD REVIEW FORM
========================================================= */
function setupAddReviewForm() {
  const form = document.getElementById("review-form");
  if (!form) return;

  const token = getCookie("token");
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    window.location.href = "index.html";
    return;
  }

  
  // --- Fetch existing reviews ---
  async function loadReviews() {
    try {
      const res = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Failed to fetch reviews");
      const reviews = await res.json();

      reviewsContainer.innerHTML = ""; // clear container
      if (!reviews.length) {
        reviewsContainer.innerHTML = "<p>No reviews yet.</p>";
        return;
      }

      reviews.forEach((review) => {
        const div = document.createElement("div");
        div.className = "review-card";
        div.innerHTML = `
          <p><strong>${escapeHtml(review.user ?? "User")}</strong> rated ${review.rating ?? "?"}/5</p>
          <p>${escapeHtml(review.comment ?? "")}</p>
        `;
        reviewsContainer.appendChild(div);
      });
    } catch (err) {
      console.error(err);
      reviewsContainer.innerHTML = "<p>Failed to load reviews.</p>";
    }
  }
   
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const rating = form.querySelector("#review-rating")?.value || 5;
    const comment = form.querySelector("#review-text")?.value?.trim();

    if (!comment) return alert("Please enter a review.");

    try {
      const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ rating, comment }),
      });

      if (!response.ok) throw new Error("Failed to submit review");

      alert("Review submitted successfully!");
      form.reset();

      // ✅ go back to place details after submit
      window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
    } catch (err) {
      console.error(err);
      alert(err.message || "Error submitting review");
    }
  });
}



async function loadReviewPlacePreview(placeId) {
  try {
    const res = await fetch(`${API_BASE_URL}/places/${placeId}`);
    if (!res.ok) throw new Error("Failed to load place");

    const place = await res.json();

    const img = document.getElementById("review-place-image");
    const title = document.getElementById("review-place-title");

    if (img) {
       img.src = place.image_url || getFallbackImage(place);
    }

    if (title) {
      title.textContent = place.name;
    }

  } catch (err) {
    console.error(err);
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

/* =========================================================
   DISPLAY PLACES (INDEX PAGE)
========================================================= */
function displayPlaces(places) {
  const placesList = document.getElementById("places-list");
  if (!placesList) return;

  placesList.innerHTML = "";

  if (!places.length) {
    placesList.innerHTML = `<p class="empty-message">No places found.</p>`;
    return;
  }

  const frag = document.createDocumentFragment();

  places.forEach((place) => {
    const card = document.createElement("article");
    card.className = "place-card";

    // Used by your price filter
    if (place.price != null) card.setAttribute("data-price", String(place.price));

    const id = place.id || place._id || place.place_id; // covers common API shapes
     
     const imgSrc = place.image_url || getFallbackImage(place);

     card.innerHTML = `
  <a class="place-card__link" href="place.html?id=${encodeURIComponent(id)}">
    <img class="place-card__img" src="${imgSrc}" alt="${escapeHtml(place.name ?? "Place")}" loading="lazy" />
    <div class="place-card__body">
      <h3 class="place-card__title">${escapeHtml(place.title ?? place.name ?? "Unnamed place")}</h3>
      <p class="place-card__desc">${escapeHtml(place.description ?? "")}</p>
      <div class="place-card__meta">
        <span class="place-card__price"><strong>${formatPrice(place.price)}</strong></span>
      </div>
    </div>
  </a>
`;

    frag.appendChild(card);
  });

  placesList.appendChild(frag);
}

function formatPrice(price) {
  if (price == null || Number.isNaN(Number(price))) return "Price not available";
  return `${Number(price).toLocaleString("en-US")} SAR / night`;
}

// Basic XSS-safe escaping for any user-provided strings
function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/* =========================================================
   POPULATE LOCATION DATALIST
========================================================= */
function populateLocationDatalist() {
  const locations = [
    "Al Ain, UAE",
    "Dubai, UAE",
    "Jakarta, Indonesia",
    "London, UK",
    "Los Angeles, USA",
    "Muscat, Oman",
    "New York, USA",
    "Paris, France",
    "Riyadh, Saudi Arabia",
    "Sharjah, UAE",
    "Tokyo, Japan",
    "Toronto, Canada",
    "Toulouse, France"
  ];

  locations.sort();

  const datalist = document.getElementById("location-suggestions");
  if (!datalist) return;

  datalist.innerHTML = "";

  locations.forEach(loc => {
    const option = document.createElement("option");
    option.value = loc;
    datalist.appendChild(option);
  });
}
