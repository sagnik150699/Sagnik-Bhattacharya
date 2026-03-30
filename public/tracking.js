// Comprehensive GA4 Event Tracking
// Tracks all user interactions across the site
(function () {
  "use strict";

  // -- Scroll depth tracking (25%, 50%, 75%) --
  // GA4 Enhanced Measurement already tracks 90%
  var scrollMilestones = { 25: false, 50: false, 75: false };
  window.addEventListener("scroll", function () {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    if (docHeight <= 0) return;
    var percent = Math.round((scrollTop / docHeight) * 100);
    [25, 50, 75].forEach(function (milestone) {
      if (percent >= milestone && !scrollMilestones[milestone]) {
        scrollMilestones[milestone] = true;
        gtag("event", "scroll_depth", {
          percent_scrolled: milestone,
          page_path: location.pathname,
        });
      }
    });
  });

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
        gtag("event", "time_on_page", {
          seconds: timeIntervals[timeIndex],
          page_path: location.pathname,
        });
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

    // CTA buttons (btn-primary, btn-outline)
    var cta = closest(target, ".btn-primary, .btn-outline");
    if (cta) {
      gtag("event", "cta_click", {
        button_text: getCleanText(cta),
        button_url: cta.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Logo link
    var logo = closest(target, ".nav-logo");
    if (logo) {
      gtag("event", "logo_click", {
        page_path: location.pathname,
      });
    }

    // Navigation links
    var navLink = closest(target, ".nav-links a");
    if (navLink) {
      gtag("event", "nav_click", {
        link_text: getCleanText(navLink),
        link_url: navLink.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Blog breadcrumb and author links
    var breadcrumb = closest(target, ".blog-breadcrumb a");
    if (breadcrumb) {
      gtag("event", "breadcrumb_click", {
        link_text: getCleanText(breadcrumb),
        link_url: breadcrumb.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    var authorLink = closest(target, ".blog-author-name, .blog-author-avatar");
    if (authorLink) {
      gtag("event", "author_click", {
        link_url: authorLink.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Blog card clicks
    var blogCard = closest(target, ".blog-card");
    if (blogCard) {
      var blogTitle = blogCard.querySelector("h3");
      gtag("event", "blog_card_click", {
        article_title: blogTitle ? getCleanText(blogTitle) : "",
        article_url: blogCard.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Course card clicks — only on actual links inside the card
    var courseCard = closest(target, ".course-card");
    if (courseCard) {
      var courseLink = closest(target, "a");
      if (courseLink && courseCard.contains(courseLink)) {
        var courseTitle = courseCard.querySelector("h3");
        gtag("event", "course_card_click", {
          course_title: courseTitle ? getCleanText(courseTitle) : "",
          link_url: courseLink.getAttribute("href") || "",
          page_path: location.pathname,
        });
      }
    }

    // Course enrollment buttons (Udemy links on courses page)
    var courseDetail = closest(target, ".course-detail-card");
    if (courseDetail && closest(target, ".btn-primary")) {
      var enrollTitle = courseDetail.querySelector("h2");
      gtag("event", "course_enroll_click", {
        course_name: enrollTitle ? getCleanText(enrollTitle) : "",
        enroll_url: closest(target, ".btn-primary").getAttribute("href") || "",
      });
    }

    // Social card clicks (contact page)
    var socialCard = closest(target, ".social-card");
    if (socialCard) {
      var socialName = socialCard.querySelector(".social-name");
      gtag("event", "social_click", {
        platform: socialName ? getCleanText(socialName) : "",
        social_url: socialCard.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Contact info links (email, website)
    var contactLink = closest(target, ".contact-info a");
    if (contactLink) {
      gtag("event", "contact_link_click", {
        link_text: getCleanText(contactLink),
        link_url: contactLink.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Project card clicks
    var projectCard = closest(target, ".project-card");
    if (projectCard) {
      var projectTitle = projectCard.querySelector("h3");
      gtag("event", "project_click", {
        project_name: projectTitle ? getCleanText(projectTitle) : "",
        project_url: projectCard.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Service project links
    var serviceProject = closest(target, ".service-project-link");
    if (serviceProject) {
      var spName = serviceProject.querySelector("strong");
      gtag("event", "project_click", {
        project_name: spName ? getCleanText(spName) : "",
        project_url: serviceProject.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Collaborator / inline links (e.g. Virginia Thorn on courses page)
    var courseTag = closest(target, ".course-tag a");
    if (courseTag) {
      gtag("event", "collaborator_click", {
        link_text: getCleanText(courseTag),
        link_url: courseTag.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Hamburger menu toggle (mobile)
    var hamburger = closest(target, ".hamburger");
    if (hamburger) {
      gtag("event", "hamburger_toggle", {
        page_path: location.pathname,
      });
    }

    // Email link click
    if (target.id === "email-link" || (target.parentElement && target.parentElement.id === "email-link")) {
      gtag("event", "email_click", {
        page_path: location.pathname,
      });
    }

    // Footer outbound links
    var footerLink = closest(target, "footer a");
    if (footerLink && footerLink.getAttribute("href") && footerLink.getAttribute("href").startsWith("http")) {
      gtag("event", "footer_link_click", {
        link_text: getCleanText(footerLink),
        link_url: footerLink.getAttribute("href"),
        page_path: location.pathname,
      });
    }

    // View all links
    var viewAll = closest(target, ".view-all");
    if (viewAll) {
      gtag("event", "view_all_click", {
        section: getCleanText(viewAll),
        link_url: viewAll.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }

    // Blog post content link clicks (links within blog article body)
    var blogContentLink = closest(target, ".blog-post-content a");
    if (blogContentLink) {
      gtag("event", "blog_content_link_click", {
        link_text: getCleanText(blogContentLink),
        link_url: blogContentLink.getAttribute("href") || "",
        page_path: location.pathname,
      });
    }
  });

  // -- Copy event tracking --
  document.addEventListener("copy", function () {
    gtag("event", "text_copy", {
      page_path: location.pathname,
    });
  });

  // -- Page leave tracking --
  // Fires once on beforeunload with accurate visible time
  window.addEventListener("beforeunload", function () {
    if (!document.hidden) {
      elapsed += (Date.now() - lastTick) / 1000;
    }
    gtag("event", "page_leave", {
      time_spent_seconds: Math.round(elapsed),
      page_path: location.pathname,
    });
  });
})();
