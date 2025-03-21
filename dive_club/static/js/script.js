document.addEventListener("DOMContentLoaded", function() {
  // === Плавное появление секций при прокрутке ===
  const sections = document.querySelectorAll("section");
  const observerOptions = { threshold: 0.2 };
  const appearObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("appear");
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  sections.forEach(section => {
    section.classList.add("before-appear");
    appearObserver.observe(section);
  });

  // === Динамическая смена цвета навбара при прокрутке ===
  const navbar = document.querySelector(".navbar");
  window.addEventListener("scroll", function() {
    if (window.scrollY > 50) {
      navbar.style.backgroundColor = "rgba(0, 0, 0, 0.95)";
    } else {
      navbar.style.backgroundColor = "rgba(0, 0, 0, 0.85)";
    }
  });

  // === Лайтбокс для галереи и мероприятий ===
  const images = document.querySelectorAll(".gallery-item, .event-image");
  if (images.length > 0) {
    const lightbox = document.createElement("div");
    lightbox.id = "lightbox";
    lightbox.classList.add("lightbox");
    document.body.appendChild(lightbox);

    const lightboxImg = document.createElement("img");
    lightboxImg.classList.add("lightbox-content");
    lightbox.appendChild(lightboxImg);

    const prev = document.createElement("a");
    prev.classList.add("prev");
    prev.innerHTML = "&#10094;";
    lightbox.appendChild(prev);

    const next = document.createElement("a");
    next.classList.add("next");
    next.innerHTML = "&#10095;";
    lightbox.appendChild(next);

    let currentIndex = 0;

    function openLightbox(index) {
      currentIndex = index;
      lightboxImg.src = images[currentIndex].dataset.full || images[currentIndex].src;
      lightbox.classList.add("active");
    }

    function closeLightbox() {
      lightbox.classList.remove("active");
    }

    function showPrev() {
      currentIndex = (currentIndex - 1 + images.length) % images.length;
      lightboxImg.src = images[currentIndex].dataset.full || images[currentIndex].src;
    }

    function showNext() {
      currentIndex = (currentIndex + 1) % images.length;
      lightboxImg.src = images[currentIndex].dataset.full || images[currentIndex].src;
    }

    images.forEach((img, index) => {
      img.addEventListener("click", () => openLightbox(index));
    });

    prev.addEventListener("click", function(e) {
      e.stopPropagation();
      showPrev();
    });

    next.addEventListener("click", function(e) {
      e.stopPropagation();
      showNext();
    });

    lightbox.addEventListener("click", function(e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape") closeLightbox();
      if (e.key === "ArrowLeft") showPrev();
      if (e.key === "ArrowRight") showNext();
    });
  }
});