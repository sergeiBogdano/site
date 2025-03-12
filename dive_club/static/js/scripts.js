document.addEventListener("DOMContentLoaded", function() {
  // Плавная прокрутка по якорям
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth"
      });
    });
  });

  // Анимация появления секций при прокрутке
  const sections = document.querySelectorAll("section");
  const appearOptions = {
    threshold: 0.2,
    rootMargin: "0px 0px -50px 0px"
  };

  const appearOnScroll = new IntersectionObserver(function(entries, observer) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("appear");
        observer.unobserve(entry.target);
      }
    });
  }, appearOptions);

  sections.forEach(section => {
    section.classList.add("before-appear");
    appearOnScroll.observe(section);
  });

  // Лайтбокс для изображений мероприятий
  const eventImages = document.querySelectorAll(".event-image");
  const lightbox = document.createElement("div");
  lightbox.id = "lightbox";
  document.body.appendChild(lightbox);

  eventImages.forEach(img => {
    img.addEventListener("click", () => {
      lightbox.classList.add("active");
      // Очистка предыдущего содержимого
      while (lightbox.firstChild) {
        lightbox.removeChild(lightbox.firstChild);
      }
      const lightboxImg = document.createElement("img");
      lightboxImg.src = img.src;
      lightbox.appendChild(lightboxImg);
    });
  });

  lightbox.addEventListener("click", e => {
    if (e.target === lightbox) {
      lightbox.classList.remove("active");
    }
  });
});
