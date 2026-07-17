/* Bright Byte — scroll-world engine.
   Scroll scrubs a continuous camera flight across the isometric SVG world:
   Discover → Design → Build → Launch. No cuts; scroll only drives time.
   Falls back to a static layout when JS is off or reduced motion is set
   (the <html> element ships with class "sw-static"; this engine removes it). */
(function () {
  "use strict";

  var scroller = document.getElementById("scrollWorld");
  if (!scroller) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reduce.matches) return; // keep the static fallback

  document.documentElement.classList.remove("sw-static");

  var stage = scroller.querySelector(".sw-stage");
  var world = scroller.querySelector(".sw-world");
  var space = scroller.querySelector(".sw-space");
  var hero = scroller.querySelector(".sw-hero");
  var hint = scroller.querySelector(".sw-hint");
  var cards = Array.prototype.slice.call(scroller.querySelectorAll(".sw-card"));
  var dots = Array.prototype.slice.call(scroller.querySelectorAll(".sw-rail button"));

  /* Island centres in world coordinates (must match the generated SVG). */
  var I1 = [650, 520], I2 = [2080, 760], I3 = [1000, 1520], I4 = [2420, 1800];
  var mid = function (a, b, fx, fy) {
    return [a[0] + (b[0] - a[0]) * fx, a[1] + (b[1] - a[1]) * fy];
  };
  var M12 = mid(I1, I2, 0.5, 0.28);
  var M23 = mid(I2, I3, 0.5, 0.55);
  var M34 = mid(I3, I4, 0.5, 0.3);

  /* Camera keyframes: p (scroll progress), world x/y, zoom z (log-lerped),
     ox = screen-space x offset as a fraction of viewport width, so the island
     sits beside the copy card instead of behind it. */
  var KEYS = [
    { p: 0.0,   x: I1[0], y: I1[1],      z: 0.62, ox: 0.10 },
    { p: 0.09,  x: I1[0], y: I1[1],      z: 1.0,  ox: 0.15 },
    { p: 0.185, x: I1[0], y: I1[1] - 26, z: 1.09, ox: 0.15 },
    { p: 0.25,  x: M12[0], y: M12[1],    z: 0.5,  ox: 0.0 },
    { p: 0.315, x: I2[0], y: I2[1],      z: 0.98, ox: -0.16 },
    { p: 0.405, x: I2[0], y: I2[1] - 26, z: 1.07, ox: -0.16 },
    { p: 0.475, x: M23[0], y: M23[1],    z: 0.48, ox: 0.0 },
    { p: 0.545, x: I3[0], y: I3[1],      z: 0.96, ox: 0.15 },
    { p: 0.635, x: I3[0], y: I3[1] - 26, z: 1.05, ox: 0.15 },
    { p: 0.71,  x: M34[0], y: M34[1],    z: 0.5,  ox: 0.0 },
    { p: 0.79,  x: I4[0], y: I4[1],      z: 0.95, ox: -0.15 },
    { p: 1.0,   x: I4[0], y: I4[1] - 34, z: 1.05, ox: -0.15 },
  ];

  /* Copy bands: [fadeInStart, holdStart, holdEnd, fadeOutEnd] per scene. */
  var BANDS = [
    [0.05, 0.09, 0.185, 0.235],
    [0.27, 0.315, 0.405, 0.455],
    [0.5, 0.545, 0.635, 0.685],
    [0.745, 0.79, 1.01, 1.02],
  ];
  var CENTERS = BANDS.map(function (b) { return (b[1] + Math.min(b[2], 0.96)) / 2; });

  /* --- interpolation: C1 Hermite spline with finite-difference tangents --- */
  function spline(keys, prop, logSpace) {
    var n = keys.length;
    var v = keys.map(function (k) { return logSpace ? Math.log(k[prop]) : k[prop]; });
    var t = keys.map(function (k) { return k.p; });
    var m = new Array(n);
    for (var i = 0; i < n; i++) {
      var i0 = Math.max(0, i - 1), i1 = Math.min(n - 1, i + 1);
      m[i] = (v[i1] - v[i0]) / (t[i1] - t[i0] || 1);
    }
    return function (p) {
      if (p <= t[0]) return logSpace ? Math.exp(v[0]) : v[0];
      if (p >= t[n - 1]) return logSpace ? Math.exp(v[n - 1]) : v[n - 1];
      var i = 0;
      while (i < n - 2 && p > t[i + 1]) i++;
      var h = t[i + 1] - t[i];
      var s = (p - t[i]) / h;
      var s2 = s * s, s3 = s2 * s;
      var out =
        (2 * s3 - 3 * s2 + 1) * v[i] +
        (s3 - 2 * s2 + s) * h * m[i] +
        (-2 * s3 + 3 * s2) * v[i + 1] +
        (s3 - s2) * h * m[i + 1];
      return logSpace ? Math.exp(out) : out;
    };
  }

  var camX = spline(KEYS, "x");
  var camY = spline(KEYS, "y");
  var camZ = spline(KEYS, "z", true);
  var camOX = spline(KEYS, "ox");

  function smoothstep(a, b, x) {
    var s = Math.min(1, Math.max(0, (x - a) / (b - a || 1)));
    return s * s * (3 - 2 * s);
  }

  /* --- state --- */
  var vw = 0, vh = 0, fit = 1, maxScroll = 1;
  var target = 0, current = -1;
  var lastW = 0, dirty = true;

  function measure() {
    /* On touch devices ignore height-only resizes (URL bar show/hide). */
    var w = window.innerWidth;
    var isTouch = window.matchMedia("(pointer: coarse)").matches;
    if (isTouch && w === lastW && vh) return;
    lastW = w;
    vw = w;
    vh = window.innerHeight;
    fit = Math.min(vw / 950, vh / 1250);
    maxScroll = Math.max(1, scroller.offsetHeight - vh);
    dirty = true;
  }

  function progress() {
    var top = scroller.getBoundingClientRect().top;
    return Math.min(1, Math.max(0, -top / maxScroll));
  }

  function apply(p) {
    var z = camZ(p) * fit;
    /* Phones: copy cards are bottom-centred, so keep the island centred and
       anchored a little above the vertical middle. */
    var narrow = vw <= 760;
    var tx = vw / 2 + (narrow ? 0 : camOX(p)) * vw - camX(p) * z;
    var ty = vh * (narrow ? 0.4 : 0.5) - camY(p) * z;
    world.style.transform =
      "translate3d(" + tx.toFixed(2) + "px," + ty.toFixed(2) + "px,0) scale(" + z.toFixed(4) + ")";

    if (space) {
      space.style.transform = "translate3d(0," + (-p * 130).toFixed(1) + "px,0)";
    }

    /* Hero overlay fades out as the flight begins. */
    if (hero) {
      var ho = 1 - smoothstep(0.015, 0.075, p);
      hero.style.opacity = ho.toFixed(3);
      hero.style.transform = "translateY(" + (-p * 260).toFixed(1) + "px)";
      hero.style.visibility = ho < 0.02 ? "hidden" : "visible";
    }
    if (hint) hint.style.opacity = (1 - smoothstep(0.005, 0.035, p)).toFixed(3);

    /* Scene copy cards. */
    for (var i = 0; i < cards.length; i++) {
      var b = BANDS[i];
      var o = smoothstep(b[0], b[1], p) * (1 - smoothstep(b[2], b[3], p));
      cards[i].style.opacity = o.toFixed(3);
      cards[i].style.setProperty("--ty", ((1 - o) * 30).toFixed(1) + "px");
      cards[i].dataset.active = o > 0.5 ? "true" : "false";
    }

    /* Route rail. */
    var nearest = 0, best = Infinity;
    for (var j = 0; j < CENTERS.length; j++) {
      var d = Math.abs(p - CENTERS[j]);
      if (d < best) { best = d; nearest = j; }
    }
    for (var k = 0; k < dots.length; k++) {
      dots[k].setAttribute("aria-current", k === nearest ? "true" : "false");
    }
  }

  var frozen = false;

  function frame() {
    if (!vw || !vh) measure(); /* viewport may not have laid out yet */
    if (!frozen) target = progress();
    if (dirty || Math.abs(target - current) > 0.00015) {
      dirty = false;
      current += (target - current) * 0.14;
      if (Math.abs(target - current) < 0.0002) current = target;
      apply(current);
    }
    requestAnimationFrame(frame);
  }

  /* Rail dots jump the flight to a scene. */
  dots.forEach(function (dot, i) {
    dot.addEventListener("click", function () {
      var y = scroller.offsetTop + CENTERS[i] * maxScroll;
      window.scrollTo({ top: y, behavior: "smooth" });
    });
  });

  window.addEventListener("resize", measure);
  window.addEventListener("orientationchange", function () {
    lastW = 0;
    measure();
  });

  reduce.addEventListener("change", function (e) {
    if (e.matches) location.reload();
  });

  measure();
  current = progress();
  apply(current);
  requestAnimationFrame(frame);

  /* Dev helper: freeze the flight at a progress value (0–1) without scrolling.
     Usage from the console: __sw.freeze(0.5); __sw.unfreeze(); */
  window.__sw = {
    freeze: function (p) { frozen = true; current = target = p; dirty = true; },
    unfreeze: function () { frozen = false; dirty = true; },
  };
})();
