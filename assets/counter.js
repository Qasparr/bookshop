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
  /get/<namespace>/<key> reads the number. Three event kinds:
    view-<page>               — fired once when a store page loads.
                                The shop's root shelf page counts as
                                view-shelf.
    play-<page>-<track slug>  — fired on the FIRST 'play' event for that
                                track within a single page load, so a
                                pause-and-resume never double-counts, and
                                each track the listener reaches counts once.
    book-<slug>               — fired on the FIRST tap within a page load
                                on a book card (any element carrying a
                                data-count="<slug>" attribute). A book has
                                no player to listen to; the tap on its card
                                is the reader's knock, and it is counted
                                the same weather-way as a play.
  The track slug is derived from the audio element's current file name,
  which covers both page shapes in this shop: pages with one player whose
  src is swapped per track (Royals, Unfriendly Ghost) and pages with one
  fixed player per track (Honey and Hammer, First Renders).

  FAILURE LAW: every call is fire-and-forget inside try/catch with a
  swallowed promise rejection. If the counter service is down, blocked,
  or someday gone, the pages degrade in total silence — the music and
  the reading never wait on the counting.

  ADDENDUM (XV day of November, 2026 e.v.): THE TABVLA. Pages that
  carry a .listen-metrics table get their measures read back and
  printed on the page, in a table, in the open:
    Plays          — the play-<page>-<track slug> counter above.
    Listening time — a new counter, lt10-<page>-<track slug>: one hit
                     per whole ten seconds of actual playback, timed
                     on the audio element's own clock (timeupdate
                     deltas), so a pause counts nothing and a seek
                     counts nothing — only time the track sounded.
                     The table prints the blocks back as min and sec.
    Visits         — the view-<page> counter above.
  The counts are client-reported and indicative: a visitor with
  scripts blocked is not counted, and a part-block of listening
  (under ten seconds, still unflushed when the page closes) is not
  counted either. Aggregates only, as ever — the Line holds.
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
  // The root of the shop (/bookshop/ or /bookshop/index.html) is the
  // SHELF — the book page — and counts as 'shelf'. A subpage served by
  // its file name (/bookshop/<page>/index.html) still names its folder.
  function pageName() {
    try {
      var parts = window.location.pathname.split('/').filter(Boolean);
      var last = parts.length ? parts[parts.length - 1] : '';
      if (!last || last === 'bookshop') { return 'shelf'; }
      if (/\.html?$/i.test(last)) {
        var prev = parts.length > 1 ? parts[parts.length - 2] : '';
        if (!prev || prev === 'bookshop') { return 'shelf'; }
        return prev.toLowerCase();
      }
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

  // (c) the book knock: first tap per card per page load.
  var knocked = {};
  function wireCard(el) {
    el.addEventListener('click', function () {
      var slug = el.getAttribute('data-count');
      if (!slug) { return; }
      var key = 'book-' + slug;
      if (knocked[key]) { return; }
      knocked[key] = true;
      hit(key);
    });
  }

  // (d) the listening clock: whole ten-second blocks of actual
  // playback, timed on the element's own clock. A pause counts
  // nothing; a seek counts nothing; only time the track sounded.
  function wireListenTime(el) {
    var last = null, pending = 0;
    el.addEventListener('timeupdate', function () {
      var t = el.currentTime;
      if (last !== null && !el.paused) {
        var d = t - last;
        if (d > 0 && d < 1.5) {
          pending += d;
          while (pending >= 10) {
            pending -= 10;
            var slug = trackSlug(el.currentSrc || el.getAttribute('src') || el.src);
            if (slug) { hit('lt10-' + page + '-' + slug); }
          }
        }
      }
      last = t;
    });
    function reset() { last = null; }
    el.addEventListener('pause', reset);
    el.addEventListener('ended', reset);
    el.addEventListener('seeking', reset);
  }

  // (e) the TABVLA read-back: the same counters, read and printed on
  // any page that carries a .listen-metrics table. A key that does
  // not exist yet reads as 0 — a new song's table starts at zero,
  // honestly. Refreshed every 30 seconds, and once shortly after the
  // visitor's own first play, so their own count is seen to land.
  var GET_BASE = 'https://abacus.jasoncameron.dev/get/' + NAMESPACE + '/';

  function readCount(key, done) {
    try {
      var p = fetch(GET_BASE + encodeURIComponent(key), {
        method: 'GET',
        mode: 'cors',
        credentials: 'omit'
      });
      if (p && p.then) {
        p.then(function (r) {
          if (!r || !r.ok) { done(0); return null; }
          return r.json();
        }).then(function (j) {
          if (j && typeof j.value === 'number') { done(j.value); }
        }).catch(function () { /* silence is the law */ });
      }
    } catch (e) { /* the page owes the counter nothing */ }
  }

  function fmtListen(blocks) {
    var secs = blocks * 10;
    if (secs < 60) { return secs + ' sec'; }
    var m = Math.floor(secs / 60), s = secs % 60;
    return s ? (m + ' min ' + s + ' sec') : (m + ' min');
  }

  function renderTabvla(box) {
    var audio = document.querySelector('audio');
    if (!audio) { return; }
    var slug = trackSlug(audio.currentSrc || audio.getAttribute('src') || audio.src);
    function set(cls, txt) {
      var n = box.querySelector('.' + cls);
      if (n) { n.textContent = txt; }
    }
    readCount('view-' + page, function (v) { set('m-visits', String(v)); });
    if (slug) {
      readCount('play-' + page + '-' + slug, function (v) { set('m-plays', String(v)); });
      readCount('lt10-' + page + '-' + slug, function (v) { set('m-listen', fmtListen(v)); });
    }
  }

  function wireTabvla() {
    var boxes = document.querySelectorAll('.listen-metrics');
    for (var i = 0; i < boxes.length; i++) {
      (function (box) {
        renderTabvla(box);
        setInterval(function () { renderTabvla(box); }, 30000);
        var audio = document.querySelector('audio');
        if (audio) {
          audio.addEventListener('play', function () {
            setTimeout(function () { renderTabvla(box); }, 3000);
          });
        }
      })(boxes[i]);
    }
  }

  function wire() {
    var players = document.querySelectorAll('audio');
    for (var i = 0; i < players.length; i++) { wirePlayer(players[i]); wireListenTime(players[i]); }
    var cards = document.querySelectorAll('[data-count]');
    for (var j = 0; j < cards.length; j++) { wireCard(cards[j]); }
    wireTabvla();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wire);
  } else {
    wire();
  }
})();
