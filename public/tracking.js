// Comprehensive GA4 Event Tracking
// Tracks all user interactions across the site
// Deferred to idle time so it does not block first paint
(function () {
  "use strict";

  function init() {

  // -- Common page context sent with every event --
  function pageContext() {
    return {
      page_path: location.pathname,
      page_title: document.title,
      page_location: location.href,
    };
  }

  // -- Scroll depth tracking (25%, 50%, 75%) --
  // GA4 Enhanced Measurement already tracks 90%
  var scrollMilestones = { 25: false, 50: false, 75: false };
  var scrollThrottle = null;

  function onScrollDepth() {
    if (scrollThrottle) return;
    scrollThrottle = setTimeout(function () {
      scrollThrottle = null;
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      var docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      if (docHeight <= 0) return;
      var percent = Math.round((scrollTop / docHeight) * 100);
      [25, 50, 75].forEach(function (milestone) {
        if (percent >= milestone && !scrollMilestones[milestone]) {
          scrollMilestones[milestone] = true;
          gtag("event", "scroll_depth", Object.assign({
            percent_scrolled: milestone,
          }, pageContext()));
        }
      });
      if (scrollMilestones[25] && scrollMilestones[50] && scrollMilestones[75]) {
        window.removeEventListener("scroll", onScrollDepth);
      }
    }, 200);
  }

  window.addEventListener("scroll", onScrollDepth, { passive: true });

  // -- Time on page tracking (visibility-aware) --
  var timeIntervals = [30, 60, 120, 300];
  var timeIndex = 0;
  var timerId = null;
  var elapsed = 0;
  var lastTick = Date.now();

  function startTimer() {
    if (timerId || timeIndex >= timeIntervals.length) return;
    lastTick = Date.now();
    timerId = setInterval(function () {
      elapsed += (Date.now() - lastTick) / 1000;
      lastTick = Date.now();
      if (timeIndex < timeIntervals.length && elapsed >= timeIntervals[timeIndex]) {
        gtag("event", "time_on_page", Object.assign({
          seconds: timeIntervals[timeIndex],
        }, pageContext()));
        timeIndex++;
        if (timeIndex >= timeIntervals.length) pauseTimer();
      }
    }, 1000);
  }

  function pauseTimer() {
    if (timerId) {
      elapsed += (Date.now() - lastTick) / 1000;
      clearInterval(timerId);
      timerId = null;
    }
  }

  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") {
      pauseTimer();
    } else {
      startTimer();
    }
  });

  if (!document.hidden) startTimer();

  // -- Helper: get clean text from element --
  function getCleanText(el) {
    return (el.textContent || el.innerText || "").replace(/\s+/g, " ").trim().substring(0, 100);
  }

  // -- Helper: find closest ancestor matching selector --
  function closest(el, selector) {
    while (el && el !== document) {
      if (el.matches && el.matches(selector)) return el;
      el = el.parentElement;
    }
    return null;
  }

  // -- Delegated click tracking --
  document.addEventListener("click", function (e) {
    var target = e.target;
    var ctx = pageContext();

    // CTA buttons (btn-primary, btn-outline)
    var cta = closest(target, ".btn-primary, .btn-outline");
    if (cta) {
      gtag("event", "cta_click", Object.assign({
        button_text: getCleanText(cta),
        button_url: cta.getAttribute("href") || "",
      }, ctx));
    }

    // Logo link
    var logo = closest(target, ".nav-logo");
    if (logo) {
      gtag("event", "logo_click", ctx);
    }

    // Navigation links
    var navLink = closest(target, ".nav-links a");
    if (navLink) {
      gtag("event", "nav_click", Object.assign({
        link_text: getCleanText(navLink),
        link_url: navLink.getAttribute("href") || "",
      }, ctx));
    }

    // Blog breadcrumb and author links
    var breadcrumb = closest(target, ".blog-breadcrumb a");
    if (breadcrumb) {
      gtag("event", "breadcrumb_click", Object.assign({
        link_text: getCleanText(breadcrumb),
        link_url: breadcrumb.getAttribute("href") || "",
      }, ctx));
    }

    var authorLink = closest(target, ".blog-author-name, .blog-author-avatar");
    if (authorLink) {
      gtag("event", "author_click", Object.assign({
        link_url: authorLink.getAttribute("href") || "",
      }, ctx));
    }

    // Blog card clicks
    var blogCard = closest(target, ".blog-card");
    if (blogCard) {
      var blogTitle = blogCard.querySelector("h3");
      gtag("event", "blog_card_click", Object.assign({
        article_title: blogTitle ? getCleanText(blogTitle) : "",
        article_url: blogCard.getAttribute("href") || "",
      }, ctx));
    }

    // Course card clicks — only on actual links inside the card
    var courseCard = closest(target, ".course-card");
    if (courseCard) {
      var courseLink = closest(target, "a");
      if (courseLink && courseCard.contains(courseLink)) {
        var courseTitle = courseCard.querySelector("h3");
        gtag("event", "course_card_click", Object.assign({
          course_title: courseTitle ? getCleanText(courseTitle) : "",
          link_url: courseLink.getAttribute("href") || "",
        }, ctx));
      }
    }

    // Course enrollment buttons (Udemy links on courses page)
    var courseDetail = closest(target, ".course-detail-card");
    if (courseDetail && closest(target, ".btn-primary")) {
      var enrollTitle = courseDetail.querySelector("h2");
      gtag("event", "course_enroll_click", Object.assign({
        course_name: enrollTitle ? getCleanText(enrollTitle) : "",
        enroll_url: closest(target, ".btn-primary").getAttribute("href") || "",
      }, ctx));
    }

    // Social card clicks (contact page)
    var socialCard = closest(target, ".social-card");
    if (socialCard) {
      var socialName = socialCard.querySelector(".social-name");
      gtag("event", "social_click", Object.assign({
        platform: socialName ? getCleanText(socialName) : "",
        social_url: socialCard.getAttribute("href") || "",
      }, ctx));
    }

    // Contact info links (email, website)
    var contactLink = closest(target, ".contact-info a");
    if (contactLink) {
      gtag("event", "contact_link_click", Object.assign({
        link_text: getCleanText(contactLink),
        link_url: contactLink.getAttribute("href") || "",
      }, ctx));
    }

    // Project card clicks
    var projectCard = closest(target, ".project-card");
    if (projectCard) {
      var projectTitle = projectCard.querySelector("h3");
      gtag("event", "project_click", Object.assign({
        project_name: projectTitle ? getCleanText(projectTitle) : "",
        project_url: projectCard.getAttribute("href") || "",
      }, ctx));
    }

    // Service project links
    var serviceProject = closest(target, ".service-project-link");
    if (serviceProject) {
      var spName = serviceProject.querySelector("strong");
      gtag("event", "project_click", Object.assign({
        project_name: spName ? getCleanText(spName) : "",
        project_url: serviceProject.getAttribute("href") || "",
      }, ctx));
    }

    // Collaborator / inline links (e.g. Virginia Thorn on courses page)
    var courseTag = closest(target, ".course-tag a");
    if (courseTag) {
      gtag("event", "collaborator_click", Object.assign({
        link_text: getCleanText(courseTag),
        link_url: courseTag.getAttribute("href") || "",
      }, ctx));
    }

    // Hamburger menu toggle (mobile)
    var hamburger = closest(target, ".hamburger");
    if (hamburger) {
      gtag("event", "hamburger_toggle", ctx);
    }

    // Email link click
    if (target.id === "email-link" || (target.parentElement && target.parentElement.id === "email-link")) {
      gtag("event", "email_click", ctx);
    }

    // Footer outbound links
    var footerLink = closest(target, "footer a");
    if (footerLink && footerLink.getAttribute("href") && footerLink.getAttribute("href").startsWith("http")) {
      gtag("event", "footer_link_click", Object.assign({
        link_text: getCleanText(footerLink),
        link_url: footerLink.getAttribute("href"),
      }, ctx));
    }

    // View all links
    var viewAll = closest(target, ".view-all");
    if (viewAll) {
      gtag("event", "view_all_click", Object.assign({
        section: getCleanText(viewAll),
        link_url: viewAll.getAttribute("href") || "",
      }, ctx));
    }

    // Blog post content link clicks (links within blog article body)
    var blogContentLink = closest(target, ".blog-post-content a");
    if (blogContentLink) {
      gtag("event", "blog_content_link_click", Object.assign({
        link_text: getCleanText(blogContentLink),
        link_url: blogContentLink.getAttribute("href") || "",
      }, ctx));
    }
  });

  // -- Copy event tracking --
  document.addEventListener("copy", function () {
    gtag("event", "text_copy", pageContext());
  });

  // -- Page leave tracking --
  // Fires once on beforeunload with accurate visible time
  window.addEventListener("beforeunload", function () {
    if (!document.hidden) {
      elapsed += (Date.now() - lastTick) / 1000;
    }
    gtag("event", "page_leave", Object.assign({
      time_spent_seconds: Math.round(elapsed),
    }, pageContext()));
  });

  } // end init

  if (typeof requestIdleCallback === 'function') {
    requestIdleCallback(init, { timeout: 3000 });
  } else {
    setTimeout(init, 1500);
  }
})();
