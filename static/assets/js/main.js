/**
* Template Name: ComingSoon
* Updated: May 30 2023 with Bootstrap v5.3.0
* Template URL: https://bootstrapmade.com/comingsoon-free-html-bootstrap-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Countdown timer
   */
  let countdown = select('.countdown');
  const output = countdown.innerHTML;

  // const countDownDate = function() {
  //   let timeleft = new Date(countdown.getAttribute('data-count')).getTime() - new Date().getTime();

  //   let days = Math.floor(timeleft / (1000 * 60 * 60 * 24));
  //   let hours = Math.floor((timeleft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  //   let minutes = Math.floor((timeleft % (1000 * 60 * 60)) / (1000 * 60));
  //   let seconds = Math.floor((timeleft % (1000 * 60)) / 1000);

  //   countdown.innerHTML = output.replace('%d', days).replace('%h', hours).replace('%m', minutes).replace('%s', seconds);
  // }
  // countDownDate();
  // setInterval(countDownDate, 1000);

  function updateClock() {
    var now = new Date();
    
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();
    var day = now.getDay();
    var nowYear = now.getFullYear();

    // Pad single digits with leading zeros
    hours = hours.toString().padStart(2, '0');
    minutes = minutes.toString().padStart(2, '0');
    seconds = seconds.toString().padStart(2, '0');

    // Get the day name based on the day index (0 = Sunday, 1 = Monday, etc.)
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var dayName = days[day];

    // Update the clock elements in the HTML
    countdown.innerHTML = output.replace('%h', hours).replace('%m', minutes).replace('%s', seconds);
    document.getElementById('current-year').textContent = nowYear;
  }

  // Update the clock every second (1000 milliseconds)
  updateClock();
  setInterval(updateClock, 1000);

})()