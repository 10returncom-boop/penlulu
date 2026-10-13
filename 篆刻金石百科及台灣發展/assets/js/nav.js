/* ============================================================
   nav.js — 兩層下拉導覽（章節 → 文章）、側邊欄樹狀導覽、手機抽屜
   資料來源：window.PEN（由 build.py 產生的 assets/js/config.js）
   連結修正：config.js 內的 url 為「根相對路徑」，依目前頁面深度
   （window.PEN_DEPTH，由 build.py 每頁注入）補上 ../ 前綴。
   Mega Menu 結構：下拉面板渲染於 .mainnav 下的獨立 .mega-layer
   圖層（位於捲動容器 .mainnav-inner 之外），由 JS 依 .nav-item
   位置定位並控制顯示，避免被 overflow 捲動容器裁切。
   ============================================================ */
(function () {
  var CHEV = '<svg class="chev" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5L6 7.5 9 4.5"/></svg>';

  /* 上層選單分組：把這些章節收進下拉選單（3 層以內：組 → 章節 → 文章） */
  var NAV_GROUPS = [
    {
      id: 'epigraphy-history', zh: '金石學與篆刻史', en: 'Epigraphy & History',
      desc: '金石學入門、篆刻兩千年演變',
      chapterIds: ['jinxue', 'history']
    },
    {
      id: 'material-technique', zh: '材料技法與工具', en: 'Materials & Techniques',
      desc: '印石材料、篆刻技法、印章形制、工具印泥',
      chapterIds: ['materials', 'techniques', 'seal-types', 'tools']
    },
    {
      id: 'taiwan-scene', zh: '台灣發展', en: 'Taiwan Scene',
      desc: '台灣篆刻發展史、印社社團、名家與文化現場',
      chapterIds: ['taiwan-history', 'taiwan-societies', 'taiwan-masters', 'taiwan-culture']
    }
  ];
  var GROUP_MAP = {};
  NAV_GROUPS.forEach(function (g) { g.chapterIds.forEach(function (id) { GROUP_MAP[id] = g; }); });

  function penUrl(u) {
    if (!u) return u;
    if (/^(?:[a-z]+:|#|\/)/i.test(u)) return u;   // 絕對/錨點/根路徑原樣
    var d = window.PEN_DEPTH || 0, p = '';
    while (d-- > 0) p += '../';
    return p + u;
  }

  /* 收集一章全部文章（跨子分類攤平） */
  function chArts(ch) {
    var arts = [];
    (ch.subs || []).forEach(function (sub) {
      (sub.articles || []).forEach(function (a) { arts.push(a); });
    });
    return arts;
  }

  /* 依 id 取章節 */
  function chapterMap() {
    var m = {};
    (window.PEN.chapters || []).forEach(function (ch) { m[ch.id] = ch; });
    return m;
  }

  /* ---------- Mega Menu（桌面，分組 → 章節 → 文章） ---------- */
  function renderMega() {
    var nav = document.getElementById('mainNav');
    var layer = document.getElementById('megaLayer');
    if (!nav || !layer || !window.PEN) return;
    var cmap = chapterMap();

    /* 依原始章節順序組出頂層項目：遇到分組就插入一個 group item */
    var topHtml = '';
    var seenGroups = {};
    var chapterPanels = [];   // 非分組章節的面板
    var groupPanels = [];     // 分組面板
    (window.PEN.chapters || []).forEach(function (ch) {
      var g = GROUP_MAP[ch.id];
      if (g) {
        if (!seenGroups[g.id]) {
          seenGroups[g.id] = true;
          topHtml += '<div class="nav-item nav-group" data-group="' + g.id + '">' +
            '<a class="nav-link" href="' + penUrl(cmap[g.chapterIds[0]].url) + '">' + g.zh +
            '<svg class="caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5L6 7.5 9 4.5"/></svg></a></div>';
          // 建分組面板
          var colsHtml = g.chapterIds.map(function (id) {
            var gc = cmap[id]; if (!gc) return '';
            var links = chArts(gc).map(function (a) {
              return '<a href="' + penUrl(a.url) + '">' + a.title + '</a>';
            }).join('');
            return '<div class="mega-col"><div class="mc-head"><a href="' + penUrl(gc.url) + '">' + gc.zh + '</a><span>' + gc.en + '</span></div>' + links + '</div>';
          }).join('');
          var wide = g.chapterIds.length >= 4 ? ' mega-panel-wide' : '';
          groupPanels.push('<div class="mega-panel' + wide + '" data-group="' + g.id + '">' +
            '<div class="mega-head"><span class="mh-zh">' + g.zh + '</span><span class="mh-en">' + g.en + '</span>' +
            '<div class="mh-desc">' + g.desc + '</div></div>' +
            '<div class="mega-cols' + (g.chapterIds.length < 4 ? ' mega-cols-auto' : '') + '">' + colsHtml + '</div>' +
            '<div class="mega-foot"><a href="' + penUrl(cmap[g.chapterIds[0]].url) + '">進入「' + g.zh + '」→</a></div>' +
            '</div>');
        }
      } else {
        topHtml += '<div class="nav-item" data-ch="' + ch.id + '">' +
          '<a class="nav-link" href="' + penUrl(ch.url) + '">' + ch.zh +
          '<svg class="caret" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4.5L6 7.5 9 4.5"/></svg></a></div>';
        var arts = chArts(ch);
        var artsHtml = arts.map(function (a) {
          return '<a href="' + penUrl(a.url) + '">' + a.title + '</a>';
        }).join('');
        chapterPanels.push('<div class="mega-panel" data-ch="' + ch.id + '">' +
          '<div class="mega-head"><span class="mh-zh">' + ch.zh + '</span><span class="mh-en">' + ch.en + '</span>' +
          '<div class="mh-desc">' + ch.desc + '</div></div>' +
          '<div class="mega-grid">' + artsHtml + '</div>' +
          '<div class="mega-foot"><a href="' + penUrl(ch.url) + '">查看「' + ch.zh + '」全部文章 →</a></div>' +
          '</div>');
      }
    });
    nav.innerHTML = topHtml + '<div class="nav-item nav-blog"><a class="nav-link" href="' + penUrl('blog/index.html') + '">部落格</a></div>';
    layer.innerHTML = groupPanels.join('') + chapterPanels.join('');
  }

  /* ---------- Mega 顯示控制（圖層定位 + hover/點擊開關） ---------- */
  function initMega() {
    var mainnav = document.querySelector('.mainnav');
    var layer = document.getElementById('megaLayer');
    if (!mainnav || !layer) return;
    // 圖層搬到 body 下，脫離 sticky / overflow 容器，避免被裁切
    document.body.appendChild(layer);
    var items = document.querySelectorAll('.mainnav .nav-item');
    if (!items.length) return;
    var panels = layer.querySelectorAll('.mega-panel');
    var hideTimer = null;
    var current = null;

    function hideAll() {
      for (var i = 0; i < panels.length; i++) panels[i].classList.remove('show');
      for (var j = 0; j < items.length; j++) items[j].classList.remove('open');
      current = null;
    }
    function scheduleHide() {
      clearTimeout(hideTimer);
      hideTimer = setTimeout(hideAll, 120);
    }
    // fixed 定位：把面板放到觸發項目正下方；靠右則向左收避免出畫面
    function placePanel(panel, item) {
      var ir = item.getBoundingClientRect();
      var w = Math.min(panel.offsetWidth || 680, window.innerWidth - 24);
      var left = ir.left;
      if (left + w > window.innerWidth - 8) left = Math.max(8, window.innerWidth - 8 - w);
      panel.style.left = left + 'px';
      panel.style.top = (ir.bottom + 2) + 'px';
    }
    function showPanel(key, item) {
      if (!item) return;
      clearTimeout(hideTimer);
      hideAll();
      var panel = layer.querySelector('.mega-panel[data-ch="' + key + '"], .mega-panel[data-group="' + key + '"]');
      if (!panel) return;
      placePanel(panel, item);
      panel.classList.add('show');
      item.classList.add('open');
      current = { panel: panel, item: item };
    }

    for (var i = 0; i < items.length; i++) {
      (function (item) {
        var key = item.getAttribute('data-ch') || item.getAttribute('data-group');
        item.addEventListener('mouseenter', function () { showPanel(key, item); });
        item.addEventListener('mouseleave', scheduleHide);
        var link = item.querySelector('.nav-link');
        if (link) {
          link.addEventListener('focus', function () { showPanel(key, item); });
          link.addEventListener('blur', scheduleHide);
        }
      })(items[i]);
    }
    // 面板 hover 時不關閉，離開面板或整列導覽才關閉
    layer.addEventListener('mouseenter', function () { clearTimeout(hideTimer); });
    layer.addEventListener('mouseleave', scheduleHide);
    mainnav.addEventListener('mouseleave', scheduleHide);
    // 捲動 / 縮視窗時，若面板開著就重新對準觸發項目正下方
    window.addEventListener('scroll', function () { if (current) placePanel(current.panel, current.item); }, true);
    window.addEventListener('resize', function () { if (current) placePanel(current.panel, current.item); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { hideAll(); }
    });
  }

  /* ---------- 側邊欄樹狀導覽（章節 → 文章，章節可展開收合） ---------- */
  function renderSidebar(currentChapter) {
    var sb = document.getElementById('sidebar');
    if (!sb || !window.PEN) return;
    var groups = PEN.chapters.map(function (ch) {
      var expanded = ch.id === currentChapter;
      var items = chArts(ch).map(function (a) {
        var cls = (a.slug && window.PEN.current && a.slug === window.PEN.current.slug) ? ' class="active"' : '';
        return '<a class="toc-l2"' + cls + ' href="' + penUrl(a.url) + '">' + a.title + '</a>';
      }).join('');
      return '<div class="toc-group' + (expanded ? ' expanded' : '') + '">' +
        '<a class="toc-l1' + (expanded ? ' active' : '') + '" href="' + penUrl(ch.url) + '">' +
        '<span>' + ch.zh + '</span>' + CHEV + '</a>' +
        '<div class="toc-sub">' + items + '</div></div>';
    }).join('');
    sb.innerHTML = '<h3>目錄 TOC</h3>' + groups +
      '<div class="side-note">此區為同章節樹狀導覽，點擊任一文章標題即可跳轉；上層分類以側欄首層展開。</div>';
    // 點擊 L1 展開/收合（非導航）
    var l1s = sb.querySelectorAll('.toc-l1');
    for (var i = 0; i < l1s.length; i++) {
      l1s[i].addEventListener('click', function (e) {
        var g = this.closest('.toc-group');
        if (g) {
          e.preventDefault();
          g.classList.toggle('expanded');
          var act = g.querySelector('.toc-l1');
          if (act) act.classList.toggle('active');
        }
      });
    }
  }

  /* ---------- 手機抽屜（分組 → 章節 → 文章） ---------- */
  function renderMobile() {
    var panel = document.getElementById('mobNav');
    if (!panel || !window.PEN) return;
    var cmap = chapterMap();
    function chapterBlock(ch) {
      var items = chArts(ch).map(function (a) {
        return '<a class="mob-art" href="' + penUrl(a.url) + '">' + a.title + '</a>';
      }).join('');
      return '<div class="mob-ch">' +
        '<button class="mob-ch-head" type="button">' + ch.zh + CHEV + '</button>' +
        '<div class="mob-ch-body">' + items + '</div></div>';
    }
    /* 依原始章節順序展開分組 */
    var html = '', seenG = {};
    (window.PEN.chapters || []).forEach(function (ch) {
      var g = GROUP_MAP[ch.id];
      if (g) {
        if (!seenG[g.id]) {
          seenG[g.id] = true;
          var inner = g.chapterIds.map(function (id) { return cmap[id]; }).filter(Boolean).map(chapterBlock).join('');
          html += '<div class="mob-ch mob-group">' +
            '<button class="mob-ch-head" type="button">' + g.zh + CHEV + '</button>' +
            '<div class="mob-ch-body">' + inner + '</div></div>';
        }
      } else {
        html += chapterBlock(ch);
      }
    });
    panel.innerHTML = html + '<div class="mob-ch mob-blog"><a class="mob-blog-link" href="' + penUrl('blog/index.html') + '">部落格</a></div>';
    // 摺疊互動
    panel.addEventListener('click', function (e) {
      var ch = e.target.closest('.mob-ch-head');
      if (ch) ch.parentNode.classList.toggle('open');
    });
    var toggle = document.getElementById('menuToggle');
    var close = document.getElementById('mobClose');
    var mp = document.getElementById('mobilePanel');
    if (toggle) toggle.addEventListener('click', function () { mp.classList.add('open'); document.body.style.overflow = 'hidden'; });
    if (close) close.addEventListener('click', function () { mp.classList.remove('open'); document.body.style.overflow = ''; });
    var lnk = panel.querySelectorAll('a');
    for (var i = 0; i < lnk.length; i++) {
      lnk[i].addEventListener('click', function () {
        mp.classList.remove('open'); document.body.style.overflow = '';
      });
    }
  }

  function init() {
    renderMega();
    initMega();
    renderSidebar(window.PEN && window.PEN.current ? window.PEN.current.chapter : null);
    renderMobile();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
