/* =========================================================
   Place Page Enhancements: Add Review & Optional UX
========================================================= */

/**
 * Show or hide the add review section based on authentication
 */
function handleAuthUI() {
  const token = getCookie("token");
  const addReviewSection = document.getElementById("add-review-section");
  
  if (token && addReviewSection) {
    addReviewSection.style.display = "block";
  } else if (addReviewSection) {
    addReviewSection.style.display = "none"; // hide if no token
  }
}

/**
 * Enhance displayPlaceDetails: show message if no amenities
 */
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
  } else {
    const noAmenities = document.createElement("p");
    noAmenities.textContent = "No amenities listed.";
    placeSection.appendChild(noAmenities);
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

/**
 * Setup Add Review Form submission
 */
function setupAddReviewForm() {
  const form = document.getElementById("add-review-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = getCookie("token");
    if (!token) return alert("You must be logged in to submit a review.");

    const placeId = getPlaceIdFromURL();
    const rating = form.querySelector("#review-rating").value;
    const comment = form.querySelector("#review-comment").value;

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ rating, comment })
      });

      if (!response.ok) throw new Error("Failed to submit review");

      alert("Review submitted successfully!");
      fetchPlaceDetails(placeId, token); // refresh place details to show new review
      form.reset();
    } catch (err) {
      console.error(err);
      alert(err.message || "Error submitting review");
    }
  });
}

/* =========================================================
   Initialize Place Page Enhancements on DOMContentLoaded
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
  if (detectCurrentPage() === "place") {
    handleAuthUI();        // show/hide review form
    setupAddReviewForm();  // handle review submissions
  }
});
