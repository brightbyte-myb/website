/* Bright Byte — shared behaviour: nav, reveal-on-scroll, footer year, contact form. */
(function () {
  "use strict";

  /* Sticky header shadow */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Mobile nav */
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".site-nav a").forEach(function (a) {
      a.addEventListener("click", function () {
        document.body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Reveal on scroll */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* Contact form → opens a pre-filled email draft (no backend required).
     Swap this for your form endpoint (e.g. POST /api/contact) when available. */
  var form = document.getElementById("contactForm");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var get = function (id) {
        var el = form.querySelector("#" + id);
        return el ? el.value.trim() : "";
      };
      var subject = "Project inquiry — " + (get("cCompany") || get("cName") || "Bright Byte website");
      var body = [
        "Name: " + get("cName"),
        "Email: " + get("cEmail"),
        "Company: " + (get("cCompany") || "—"),
        "Project type: " + get("cType"),
        "Budget range: " + get("cBudget"),
        "",
        "Project details:",
        get("cMessage"),
      ].join("\n");
      var to = form.getAttribute("data-to") || "";
      window.location.href =
        "mailto:" + to +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
      var note = document.getElementById("formStatus");
      if (note) {
        note.textContent =
          "Your email app should open with a pre-filled draft. If it doesn't, email us directly at " + to + ".";
      }
    });
  }
})();
