(function () {
  "use strict";

  function pages() {
    return Array.from(document.querySelectorAll(".page"));
  }

  function pageEl(id) {
    return document.getElementById(id);
  }

  function crumbTrail(id) {
    var trail = [];
    var cur = id;
    var seen = {};
    while (cur && !seen[cur]) {
      seen[cur] = true;
      var el = pageEl(cur);
      if (!el) break;
      trail.unshift(cur);
      cur = el.dataset.parent || null;
    }
    return trail;
  }

  function render(id) {
    var all = pages();
    var ids = all.map(function (p) { return p.id; });
    if (ids.indexOf(id) === -1) id = ids[0];

    all.forEach(function (p) { p.classList.remove("active"); });
    var current = pageEl(id);
    current.classList.add("active");

    var crumbsEl = document.getElementById("crumbs");
    if (crumbsEl) {
      crumbsEl.innerHTML = "";
      var trail = crumbTrail(id);
      trail.forEach(function (pid, i) {
        var label = pageEl(pid).dataset.title;
        if (i === trail.length - 1) {
          var span = document.createElement("span");
          span.className = "current";
          span.textContent = label;
          crumbsEl.appendChild(span);
        } else {
          var a = document.createElement("a");
          a.href = "#" + pid;
          a.textContent = label;
          crumbsEl.appendChild(a);
          var sep = document.createElement("span");
          sep.className = "sep";
          sep.textContent = "›";
          crumbsEl.appendChild(sep);
        }
      });
    }

    var idx = ids.indexOf(id);
    var prevBtn = document.getElementById("prevBtn");
    var nextBtn = document.getElementById("nextBtn");
    if (prevBtn) prevBtn.disabled = idx <= 0;
    if (nextBtn) nextBtn.disabled = idx === -1 || idx >= ids.length - 1;
    var pageIndexEl = document.getElementById("pageIndex");
    if (pageIndexEl) pageIndexEl.textContent = (idx + 1) + " / " + ids.length;
  }

  function goto(id) {
    if (location.hash === "#" + id) { render(id); return; }
    location.hash = id;
  }

  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-goto]");
    if (!el) return;
    e.preventDefault();
    if (el.disabled) return;
    goto(el.dataset.goto);
  });

  document.addEventListener("DOMContentLoaded", function () {
    var ids = pages().map(function (p) { return p.id; });

    var prevBtn = document.getElementById("prevBtn");
    var nextBtn = document.getElementById("nextBtn");
    if (prevBtn) prevBtn.addEventListener("click", function () {
      var idx = ids.indexOf(location.hash.slice(1));
      if (idx > 0) goto(ids[idx - 1]);
    });
    if (nextBtn) nextBtn.addEventListener("click", function () {
      var idx = ids.indexOf(location.hash.slice(1));
      if (idx >= 0 && idx < ids.length - 1) goto(ids[idx + 1]);
    });

    var fsBtn = document.getElementById("fullscreenBtn");
    var frame = document.getElementById("deckFrame");
    if (fsBtn && frame) {
      fsBtn.addEventListener("click", function () {
        if (document.fullscreenElement) {
          document.exitFullscreen();
        } else {
          frame.requestFullscreen();
        }
      });
    }

    window.addEventListener("hashchange", function () {
      render(location.hash.slice(1) || ids[0]);
    });

    render(location.hash.slice(1) || ids[0]);
  });
})();
