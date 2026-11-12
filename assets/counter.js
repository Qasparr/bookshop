/*
  THE BOOKSHOP COUNTER — anonymous listen/read counting for the store pages.
  "Do what thou wilt shall be the whole of the Law."
  Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
  (Greek, -ARR, All Rights Reserved, Without Prejudice).
  Scientific Illuminism: Method of Science, Aim of Religion.

  DOCTRINE (the Line): public counts, private persons. This script keeps
  AGGREGATES ONLY — a number per page, a number per track. No cookies, no
  local storage, no fingerprinting, no referrer harvesting, no cross-site
  tracking, nothing that could name or follow a listener. A play is a
  weather reading, not a record of a person.

  MECHANISM: counters live at Abacus (abacus.jasoncameron.dev), a free
  no-account counting API: GET /hit/<namespace>/<key> adds one, GET
  /get/<namespace>/<key> reads the number. Two event kinds:
    view-<page>               — fired once when a store page loads.
    play-<page>-<track slug>  — fired on the FIRST 'play' event for that
                                track within a single page load, so a
                                pause-and-resume never double-counts, and
                                each track the listener reaches counts once.
  The track slug is derived from the audio element's current file name,
  which covers both page shapes in this shop: pages with one player whose
  src is swapped per track (Royals, Unfriendly Ghost) and pages with one
  fixed player per track (Honey and Hammer, First Renders).

  FAILURE LAW: every call is fire-and-forget inside try/catch with a
  swallowed promise rejection. If the counter service is down, blocked,
  or someday gone, the pages degrade in total silence — the music and
  the reading never wait on the counting.
*/
(function () {
  'use strict';

  var NAMESPACE = 'qasparr-bookshop';
  var BASE = 'https://abacus.jasoncameron.dev/hit/' + NAMESPACE + '/';

  function hit(key) {
    try {
      var p = fetch(BASE + encodeURIComponent(key), {
        method: 'GET',
        mode: 'cors',
        credentials: 'omit',
        keepalive: true
      });
      if (p && p.catch) { p.catch(function () { /* silence is the law */ }); }
    } catch (e) { /* the page owes the counter nothing */ }
  }

  // The page's own name is its folder: /bookshop/<page>/ -> <page>.
  function pageName() {
    try {
      var parts = window.location.pathname.split('/').filter(Boolean);
      var last = parts.length ? parts[parts.length - 1] : '';
      if (!last || last === 'bookshop' || /\.html?$/i.test(last)) { return null; }
      return last.toLowerCase();
    } catch (e) { return null; }
  }

  // "tracks/Qasparr - Keeper of the Keys.mp3" -> "qasparr-keeper-of-the-keys"
  function trackSlug(src) {
    try {
      var base = String(src || '').split('/').pop().split('?')[0];
      base = decodeURIComponent(base).replace(/\.[a-z0-9]+$/i, '');
      return base.toLowerCase().replace(/[^a-z0-9]+/g, '-')
                 .replace(/^-+|-+$/g, '').slice(0, 90);
    } catch (e) { return null; }
  }

  var page = pageName();
  if (!page) { return; }

  // (a) the read: one view per page load.
  hit('view-' + page);

  // (b) the listen: first play per track per page load.
  var counted = {};
  function wirePlayer(el) {
    el.addEventListener('play', function () {
      var slug = trackSlug(el.currentSrc || el.getAttribute('src') || el.src);
      if (!slug) { return; }
      var key = 'play-' + page + '-' + slug;
      if (counted[key]) { return; }
      counted[key] = true;
      hit(key);
    });
  }

  function wire() {
    var players = document.querySelectorAll('audio');
    for (var i = 0; i < players.length; i++) { wirePlayer(players[i]); }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wire);
  } else {
    wire();
  }
})();
