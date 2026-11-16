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

  ADDENDUM II (XVI day of November, 2026 e.v.): THE TABVLA SPREADS.
  At the founder's order the same table now stands on the shop's
  other pages, and the read-back learns two new seats:
    data-track="<file name>" — a page with several fixed players
                     (the First Renders) gives each box the file it
                     answers for; the box reads that track's plays
                     and listening blocks, slugged by the same
                     trackSlug() that counts them, so the printed
                     key can never drift from the counted key. A box
                     without data-track keeps the first law: it
                     follows the page's player, and on a page whose
                     one player swaps its file per track (the
                     Unfriendly Ghost) the count follows the track
                     in the player.
    data-books="<slug,slug,...>" — a page with no player at all
                     (the Shelf, the series page) still prints its
                     Visits, and sums the book-<slug> knocks of the
                     cards it names into a Books knocked row. A book
                     is read, not heard; its table counts the
                     reader's knock the same weather-way.
  No new event kinds are minted by this addendum: views, plays,
  listening blocks and knocks were already counted on every page
  that carries this script. The addendum only prints them.

  ADDENDUM III (XVI day of November, 2026 e.v.): THE 64 LETTERS.
  Printing the counts exposed a law of the counting house that
  silent counting never had to face: Abacus refuses any key
  longer than 64 characters, hit and read alike. A play key is
  "play-" + page + "-" + track slug, and the long-named tracks —
  all three First Renders, half the Unfriendly Ghost — ran past
  the limit; their hits were turned away at the gate and counted
  NOWHERE (the read-back's error is the witness: "length must be
  between 3 and 64 characters"). Views and knocks, whose keys are
  short, were never touched by this. The repair, in trackKey()
  below: a key that fits keeps its exact old form — those
  counters hold real counts and are not orphaned — and only an
  over-long key is shortened, its slug cut to fit with a
  six-letter hash of the whole slug seated at the tail, so two
  long names sharing a head can never collide into one counter.
  The over-long keys held nothing (every hit was refused), so
  nothing is lost by their repair; their counts honestly begin
  at zero from this day.
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

  // THE 64 LETTERS (Addendum III): every play / listening key is
  // built here and nowhere else, so the counted key and the
  // printed key are one key by construction.
  var KEY_MAX = 64;
  function hash6(s) {
    var h = 5381;
    for (var i = 0; i < s.length; i++) { h = ((h * 33) ^ s.charCodeAt(i)) >>> 0; }
    return ('00000' + h.toString(36)).slice(-6);
  }
  function trackKey(kind, slug) {
    var head = kind + '-' + page + '-';
    var key = head + slug;
    if (key.length <= KEY_MAX) { return key; }
    var room = KEY_MAX - head.length - 7; // '-' + the six-letter hash
    return head + slug.slice(0, room) + '-' + hash6(slug);
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
      var key = trackKey('play', slug);
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
            if (slug) { hit(trackKey('lt10', slug)); }
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
    function set(cls, txt) {
      var n = box.querySelector('.' + cls);
      if (n) { n.textContent = txt; }
    }
    // Visits print in every seat — a page with no player is still
    // visited, and its table still stands.
    readCount('view-' + page, function (v) { set('m-visits', String(v)); });
    // The track this box answers for: its own data-track naming
    // wins; otherwise the page's player, as the first law had it.
    var slug = null;
    var named = box.getAttribute('data-track');
    if (named) { slug = trackSlug(named); }
    if (!slug) {
      var audio = document.querySelector('audio');
      if (audio) { slug = trackSlug(audio.currentSrc || audio.getAttribute('src') || audio.src); }
    }
    if (slug) {
      readCount(trackKey('play', slug), function (v) { set('m-plays', String(v)); });
      readCount(trackKey('lt10', slug), function (v) { set('m-listen', fmtListen(v)); });
    }
    // The books this box answers for: data-books names the cards
    // whose knocks the box sums and prints as one weather reading.
    var books = box.getAttribute('data-books');
    if (books) {
      var slugs = books.split(',').map(function (s) { return s.trim(); }).filter(Boolean);
      var total = 0, left = slugs.length;
      if (!left) { set('m-knocks', '0'); }
      slugs.forEach(function (bs) {
        readCount('book-' + bs, function (v) {
          total += v; left -= 1;
          if (!left) { set('m-knocks', String(total)); }
        });
      });
    }
  }

  function wireTabvla() {
    var boxes = document.querySelectorAll('.listen-metrics');
    for (var i = 0; i < boxes.length; i++) {
      (function (box) {
        renderTabvla(box);
        setInterval(function () { renderTabvla(box); }, 30000);
        // Every player on the page may be the one just played —
        // on a many-player page the refresh follows any of them.
        var audios = document.querySelectorAll('audio');
        for (var k = 0; k < audios.length; k++) {
          audios[k].addEventListener('play', function () {
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
