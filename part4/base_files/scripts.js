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
  const token = getCookie("token");

 // --- GLOBAL SETUP ---
  setupLogout();
        
  // --- MAIN PAGE LOGIC ---
  if (currentPage === 'login') handleLoginForm();
  if (currentPage === 'signup') handleSignupForm();
  
  if (currentPage === 'add_place') {
    if (!token) {
      window.location.href = "index.html";
      return;
    }
    handleAddPlaceForm();
  }
  
  if (currentPage === 'index') {
    checkAuthentication();
    initPriceFilter();
    setupLogout();
    populateLocationDatalist();
    setupIndexSearch();
    initCustomDatePicker(); 
  }

  if (currentPage === 'place') {
  const placeId = getPlaceIdFromURL();

  // Show/hide Login vs Logout in the header
  const loginLink = document.querySelector(".login-button");
  const logoutBtn = document.getElementById("logout-btn");
  if (token) {
    if (loginLink) loginLink.style.display = "none";
    if (logoutBtn) logoutBtn.style.display = "inline-block";
  } else {
    if (loginLink) loginLink.style.display = "inline-block";
    if (logoutBtn) logoutBtn.style.display = "none";
  }

/* ==================================
         addReview Section
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
  } else {
    fetchPlaceDetails(placeId, token);
  }
 }

    if (currentPage === 'review') {
       const placeId = getPlaceIdFromURL();
       if (!token || !placeId) {
         window.location.href = "index.html";
         return;
       }
       loadReviewPlacePreview(placeId);   // 🔥 THIS loads the image
       setupAddReviewForm();
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
        const locationInput = document.getElementById("location");
        const priceInput = document.getElementById("price");
        const latitudeInput = document.getElementById("latitude");
        const longitudeInput = document.getElementById("longitude");
        const amenitiesInput = document.getElementById("amenities");
        const imageInput = document.getElementById("image_url");
        const errorEl = document.getElementById("error-message");
        const addPlaceBtn = document.getElementById("add-place-btn");
        
        addPlaceForm.addEventListener("submit", async (event) => {
                event.preventDefault();
                if (errorEl) errorEl.textContent = "";
                
                // Get form values
                const title = titleInput?.value.trim();
                const description = descriptionInput?.value.trim();
                const location = locationInput?.value.trim();
                const price = parseFloat(priceInput?.value);
                const latitude = parseFloat(latitudeInput?.value);
                const longitude = parseFloat(longitudeInput?.value);
                const imageUrl = imageInput?.value.trim();
                const amenitiesRaw = amenitiesInput?.value.trim() || "";
                const amenities = amenitiesRaw
                        ? amenitiesRaw.split(",").map(a => a.trim()).filter(Boolean)
                        : [];
                
                // Validation
                if (!title || !description || !location || !price || !latitude || !longitude) {
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
                                location,
                                price,
                                latitude,
                                longitude,
                                image_url: imageUrl,
                                amenities,
                        });
                        
                        // Show success message
                        addPlaceBtn.textContent = "✓ Created!";
                        addPlaceBtn.style.backgroundColor = "#28a745";
                        
                        setTimeout(() => {
                                window.location.href = "index.html";
                        }, 1500);
                        
                        // Redirect to home page
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
                        HELPERS
========================================================= */
function setCookie(name, value, days) {
  const maxAge = days ? `; max-age=${days * 24 * 60 * 60}` : "";
  const sameSite = "; samesite=lax";
  const secure = location.protocol === "https:" ? "; secure" : "";
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}${maxAge}; path=/${sameSite}${secure}`;
}

function decodeJwt(token) {
  try {
    const payload = token.split(".")[1];
    const base64 = payload.replace(/-/g, "+").replace(/_/g, "/");
    const json = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(json);
  } catch {
    return null;
  }
}

function getAuthInfoFromToken(token) {
  const decoded = decodeJwt(token);
  if (!decoded) return { userId: null, isAdmin: false };

  const userId = decoded.sub ? String(decoded.sub) : null;
  const isAdmin = Boolean(decoded.is_admin);

  return { userId, isAdmin };
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
                ---- PLACE DETAILS ----
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
     setupIndexSearch();
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
                        const name = String(p.title || p.name || "").toLowerCase();
                        const desc = String(p.description || "").toLowerCase();
                        const placeLocation = String(p.location || "").toLowerCase();
                        const price = Number(p.price ?? Infinity);
                        
                        const matchesLocation =
                                !location ||
                                name.includes(location) ||
                                desc.includes(location) ||
                                placeLocation.includes(location);
                        
                        const matchesPrice = price <= maxPrice;
                        const maxGuests = Number(p.max_guests ?? 0);
                        const matchesGuests = !guests || (maxGuests >= guests);
                        
                        // Date filter
                        let matchesDate = true;
                        const checkInText = document.getElementById("checkin-display")?.textContent;
                        const checkOutText = document.getElementById("checkout-display")?.textContent;
                        
                        // Only filter if the user actually selected dates
                        if (checkInText !== "Add dates" && checkOutText !== "Add dates" && p.available_from && p.available_to) {
                                const checkIn = new Date(checkInText);
                                const checkOut = new Date(checkOutText);
                                const availableFrom = new Date(p.available_from);
                                const availableTo = new Date(p.available_to);
                                matchesDate = availableFrom <= checkIn && availableTo >= checkOut;
                        }
                        
                        return matchesLocation && matchesPrice && matchesGuests && matchesDate;
                });
                displayPlaces(filtered);
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
    <h1>${escapeHtml(place.title ?? place.name ?? "Unnamed place")}</h1>
    <p class="place-location">
    <i class="fa fa-map-marker-alt"></i>
    ${escapeHtml(place.location ?? "Location not specified")}
    </p>
    <p>${escapeHtml(place.description ?? "")}</p>
    <p><strong>Price:</strong> ${formatPrice(place.price)}</p>
  `;
  placeSection.appendChild(infoDiv);

// === DELETE ===
const deleteWrapper = document.createElement("div");
deleteWrapper.className = "delete-wrapper";

deleteWrapper.innerHTML = `
  <button id="delete-place-btn" class="details-button danger" style="display:none;">
    <i class="fa fa-trash"></i> Delete Place
  </button>
`;

placeSection.appendChild(deleteWrapper);

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
        const reviews = Array.isArray(place.reviews) ? place.reviews : [];
        const reviewCount = reviews.length;
        
        let averageRating = 0;
        if (reviewCount > 0) {
                const total = reviews.reduce((sum, r) => sum + Number(r.rating || 0), 0);
                averageRating = total / reviewCount;
        }
        
        const ratingValueEl = document.querySelector(".rating-value");
        const reviewCountEl = document.querySelector(".review-count");
        
        if (ratingValueEl) ratingValueEl.textContent = reviewCount ? averageRating.toFixed(1) : "0.0";
        if (reviewCountEl) reviewCountEl.textContent = reviewCount === 1 ? " • 1 review" : ` • ${reviewCount} reviews`;
        
        renderReviews(place);
        
        const token = getCookie("token");
        const { userId, isAdmin } = token ? getAuthInfoFromToken(token) : { userId: null, isAdmin: false };
        setupPlaceDeleteButton(place, token, userId, isAdmin);
}

function setupReviewDeleteButtons(place, token, userId, isAdmin) {
  if (!token) return;

  document.querySelectorAll(".review-delete-btn").forEach((btn) => {
    const reviewId = btn.dataset.reviewId;

    const reviewObj = (place.reviews || []).find((r) => String(r.id) === String(reviewId));
    const reviewOwnerId = reviewObj?.user_id ? String(reviewObj.user_id) : null;

    const canDelete = isAdmin || (userId && reviewOwnerId && userId === reviewOwnerId);
    if (!canDelete) return;

    btn.style.display = "inline-flex";

    btn.onclick = async () => {
      if (!confirm("Delete this review?")) return;

      try {
        const res = await fetch(`${API_BASE_URL}/places/${place.id}/reviews/${reviewId}`, {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        });

        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
          alert(data?.error || data?.message || "Failed to delete review");
          return;
        }

        alert("Review deleted!");
        fetchPlaceDetails(place.id, token);
      } catch (err) {
        console.error(err);
        alert("Network error while deleting review");
      }
    };
  });
}

function setupPlaceDeleteButton(place, token, userId, isAdmin) {
  const deleteBtn = document.getElementById("delete-place-btn");
  if (!deleteBtn) return;

  deleteBtn.style.display = "none";

  if (!token) return;

  const ownerId = place.owner_id ? String(place.owner_id) : null;
  const canDelete = isAdmin || (userId && ownerId && userId === ownerId);

  if (!canDelete) return;

  deleteBtn.style.display = "inline-flex";

  deleteBtn.onclick = async () => {
    if (!confirm("Are you sure you want to delete this place?")) return;

    try {
      const res = await fetch(`${API_BASE_URL}/places/${place.id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        alert(data?.error || data?.message || "Failed to delete place");
        return;
      }

      alert("Place deleted successfully!");
      window.location.href = "index.html";
    } catch (err) {
      console.error(err);
      alert("Network error while deleting place");
    }
  };
}

function renderReviews(place) {
  const reviewsList = document.getElementById("reviews-list");
  if (!reviewsList) return;

  reviewsList.innerHTML = "";

  const reviews = Array.isArray(place.reviews) ? place.reviews : [];

  if (!reviews.length) {
    reviewsList.innerHTML = "<p class='empty-message'>No reviews yet.</p>";
    return;
  }

  reviews.forEach((review) => {
    const reviewCard = document.createElement("div");
    reviewCard.className = "review-card";

    const name = review.user_name || "User";
    const rating = review.rating ?? "?";
    const text = review.text || "";

    reviewCard.innerHTML = `
      <p><strong>${escapeHtml(name)}</strong> rated <strong>${escapeHtml(rating)}/5</strong></p>
      <p>${escapeHtml(text)}</p>

      <div class="review-actions">
        <button class="details-button danger review-delete-btn" style="display:none;"
          data-review-id="${escapeHtml(review.id)}">
          <i class="fa fa-trash"></i> Delete Review
        </button>
      </div>
    `;

    reviewsList.appendChild(reviewCard);
  });

  // enable delete buttons after rendering
  const token = getCookie("token");
  const { userId, isAdmin } = token ? getAuthInfoFromToken(token) : { userId: null, isAdmin: false };
  setupReviewDeleteButtons(place, token, userId, isAdmin);
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

  const reviewsContainer = document.getElementById("reviews-container");
  if (!reviewsContainer) return;

/* =================================================
           --- Fetch existing reviews ---
==================================================== */
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
              const name = review.user_name || "User";
              const rating = review.rating ?? "?";
              const text = review.text || "";
              
              div.innerHTML = `
              <p><strong>${escapeHtml(name)}</strong> rated <strong>${rating}/5</strong></p>
              <p>${escapeHtml(text)}</p>
              `;
        reviewsContainer.appendChild(div);
      });
    } catch (err) {
      console.error(err);
      reviewsContainer.innerHTML = "<p>Failed to load reviews.</p>";
    }
  }

         loadReviews();
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const rating = form.querySelector("#review-rating")?.value || 5;
    const comment = form.querySelector("#review-text")?.value?.trim();

    if (!comment) return alert("Please enter a review.");

    try {
const response = await fetch(`${API_BASE_URL}/reviews/`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  },
  body: JSON.stringify({
    place_id: placeId,
    text: comment,
    rating: Number(rating),
  }),
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
      title.textContent = place.title ?? place.name ?? "Unnamed place";
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
     const form = document.getElementById("filter-form");
     if (form) {
        form.dispatchEvent(new Event('submit'));
    }
    /*const maxPrice = Number(priceRange.value);
    document.querySelectorAll(".place-card").forEach(card => {
      const price = getCardPrice(card);
      card.style.display = price <= maxPrice ? "" : "none";
    });*/
  }
  priceRange.addEventListener("input", () => {
    updateUI();
    applyFilterDebounced();
  });

  resetBtn?.addEventListener("click", () => {
    priceRange.value = String(DEFAULT_MAX);
    updateUI();
    /*applyFilter();*/
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

/* =========================================================
    DATE PICKER UI LOGIC (CORRECTED)
========================================================= */
function initCustomDatePicker() {
  const zones = document.querySelectorAll('.date-zone');
  const amPmBtns = document.querySelectorAll('.time-btn');

  // 1. Handle AM/PM Toggle
  amPmBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation(); // Stops the calendar from opening when clicking buttons
      const parent = btn.parentElement;
      const activeBtn = parent.querySelector('.time-btn.active');
      if (activeBtn) activeBtn.classList.remove('active');
      btn.classList.add('active');
      
      // Store period (AM/PM) on the zone for filtering
      const zone = btn.closest('.date-zone');
      if (zone) zone.dataset.period = btn.textContent;
    });
  });

  // 2. Handle Date Picking & Highlighting
  zones.forEach(zone => {
    // Create hidden input to trigger the browser's native calendar
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'date';
    // Prevent picking past dates
    hiddenInput.min = new Date().toISOString().split("T")[0];
    hiddenInput.style.cssText = "position:absolute; opacity:0; pointer-events:none; left:0; top:0;";
    zone.appendChild(hiddenInput);

    zone.addEventListener('click', () => {
      // Manage Active Highlight UI
      zones.forEach(z => z.classList.remove('active-zone'));
      zone.classList.add('active-zone');
      
      // Open Calendar
      if (typeof hiddenInput.showPicker === 'function') {
        hiddenInput.showPicker();
      } else {
        hiddenInput.click(); // Fallback
      }
    });

    // Update UI when a real date is chosen
    hiddenInput.addEventListener('change', (e) => {
      const display = zone.querySelector('.date-display');
      if (e.target.value && display) {
        display.textContent = e.target.value; 
      }
    });
  });
}
