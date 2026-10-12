/* Penlulu shared front-end */
(function(){
  "use strict";
  var $=function(s,c){return (c||document).querySelector(s)};
  var $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};

  /* ---------- theme (default light) ---------- */
  try{
    var saved=localStorage.getItem("penlulu-theme");
    if(saved) document.documentElement.setAttribute("data-theme",saved);
  }catch(e){}
  document.addEventListener("click",function(e){
    var t=e.target.closest("#theme-toggle");
    if(!t) return;
    var cur=document.documentElement.getAttribute("data-theme")==="dark"?"light":"dark";
    document.documentElement.setAttribute("data-theme",cur);
    try{localStorage.setItem("penlulu-theme",cur)}catch(e){}
  });

  /* ---------- mobile menu ---------- */
  $("#burger").addEventListener("click",function(){
    $("#main-nav").classList.toggle("mobile-open");
  });

  /* ---------- singleton MegaMenu（header / footer 共用同一面板） ---------- */
  var panel=$("#mega-panel"), currentTrigger=null;
  function isMobile(){return window.innerWidth<=760}
  function closePanel(){
    if(!panel)return;
    panel.hidden=true; panel.innerHTML=""; panel.classList.remove("mobile");
    panel.removeAttribute("style");
    if(currentTrigger){currentTrigger.setAttribute("aria-expanded","false");currentTrigger=null}
  }
  function positionPanel(trigger){
    var r=trigger.getBoundingClientRect(), pw=panel.offsetWidth;
    var top=r.bottom+window.scrollY+8, left=r.left+window.scrollX;
    if(left+pw>window.innerWidth-12)left=window.innerWidth-pw-12+window.scrollX;
    if(left<window.scrollX+8)left=window.scrollX+8;
    panel.style.top=top+"px"; panel.style.left=left+"px";
  }
  function openPanel(trigger){
    var id=trigger.getAttribute("data-tpl"), tpl=document.getElementById(id);
    if(!tpl)return;
    if(currentTrigger&&currentTrigger!==trigger)closePanel();
    currentTrigger=trigger; trigger.setAttribute("aria-expanded","true");
    panel.innerHTML=""; panel.appendChild(tpl.content.cloneNode(true));
    panel.hidden=false;
    if(isMobile()){
      panel.classList.add("mobile");
      trigger.parentElement.insertBefore(panel,trigger.nextSibling);
    }else{
      document.body.appendChild(panel); positionPanel(trigger);
    }
  }
  document.addEventListener("click",function(e){
    var t=e.target.closest(".mega-trigger,#footer-mega-open");
    if(!t){if(panel&&!panel.hidden&&!isMobile())closePanel();return}
    e.preventDefault(); e.stopPropagation();
    if(panel&&!panel.hidden&&currentTrigger===t){closePanel();return}
    openPanel(t);
  });
  document.addEventListener("keydown",function(e){if(e.key==="Escape")closePanel()});
  window.addEventListener("scroll",function(){if(!isMobile()&&currentTrigger)positionPanel(currentTrigger)},{passive:true});
  window.addEventListener("resize",closePanel);

  /* ---------- search overlay + autocomplete ---------- */
  var idx=null, overlay=$("#search-overlay"), input=$("#search-input"), suggest=$("#search-suggest");
  function openSearch(){ if(overlay){overlay.classList.add("open"); loadIndex().then(function(){input.focus()})} }
  function closeSearch(){ if(overlay){overlay.classList.remove("open"); input.value=""; suggest.innerHTML=""} }
  $("#search-open").addEventListener("click",openSearch);
  var heroS=$("#hero-search-open"); if(heroS)heroS.addEventListener("click",openSearch);
  if(overlay){
    overlay.addEventListener("click",function(e){if(e.target===overlay)closeSearch()});
    $("#search-close").addEventListener("click",closeSearch);
  }
  document.addEventListener("keydown",function(e){
    if(e.key==="Escape") closeSearch();
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="k"){e.preventDefault();openSearch()}
  });

  function loadIndex(){
  if(idx) return Promise.resolve(idx);
  if(window.PENLULU_INDEX){idx=window.PENLULU_INDEX;return Promise.resolve(idx);}
    var rp=(function(){var m=document.querySelector('meta[name="site-root"]');return (m?m.getAttribute("content"):".")+"/";})();
    return fetch(rp+"search-index.json").then(function(r){return r.json()}).then(function(d){idx=d;return d});
  }
  function renderSuggest(q){
    var ql=q.trim().toLowerCase();
    if(!ql){suggest.innerHTML='<div class="search-hint">輸入關鍵字，例如：鋼筆、墨水、手帳、筆尖</div>';return}
    var items=idx.articles.filter(function(a){
      return (a.title+" "+a.categoryTitle+" "+(a.tags||[]).join(" ")+" "+(a.excerpt||"")).toLowerCase().indexOf(ql)>=0;
    }).slice(0,9);
    if(!items.length){suggest.innerHTML='<div class="s-empty">找不到相關文章，換個關鍵字試試。</div>';return}
    suggest.innerHTML=items.map(function(a){
      return '<a href="'+a.url+'"><span class="s-title">'+a.title+'</span>'+
        '<span class="s-meta">'+a.categoryTitle+' · '+a.level+'</span></a>';
    }).join("");
  }
  if(input){
    input.addEventListener("input",function(){loadIndex().then(function(){renderSuggest(input.value)})});
  }

  /* ---------- accordion ---------- */
  $$(".accordion-head").forEach(function(h){
    h.addEventListener("click",function(){h.parentElement.classList.toggle("open")});
  });

  /* ---------- TOC scrollspy ---------- */
  var toc=$("#toc");
  if(toc){
    var heads=$$(".article-content h2, .article-content h3");
    var links=$$("#toc a");
    links.forEach(function(l){l.addEventListener("click",function(){
      links.forEach(function(x){x.classList.remove("active")});l.classList.add("active");
    })});
    var byId={};
    heads.forEach(function(h){byId[h.id]=h});
    function spy(){
      var pos=window.scrollY+120, current=null;
      heads.forEach(function(h){if(h.offsetTop<=pos)current=h.id});
      if(current){
        links.forEach(function(l){l.classList.toggle("active",l.getAttribute("href")==="#"+current)});
      }
    }
    window.addEventListener("scroll",spy,{passive:true});spy();
  }

  /* ---------- favorites (localStorage) ---------- */
  var FAV="penlulu-favs";
  function getFav(){try{return JSON.parse(localStorage.getItem(FAV)||"[]")}catch(e){return[]}}
  function setFav(a){try{localStorage.setItem(FAV,JSON.stringify(a))}catch(e){}}
  function renderFavSide(){
    var box=$("#side-fav-list"); if(!box) return;
    var f=getFav();
    if(!f.length){box.innerHTML='<li class="empty">還沒有收藏，按文章上方的 ♥ 收藏。</li>';return}
    box.innerHTML=f.map(function(x){return '<li><a href="'+x.url+'">'+x.title+'</a></li>'}).join("");
  }
  document.addEventListener("click",function(e){
    var b=e.target.closest(".fav-btn");
    if(!b) return;
    var f=getFav(), url=b.getAttribute("data-url"), title=b.getAttribute("data-title");
    var i=f.findIndex(function(x){return x.url===url});
    if(i>=0){f.splice(i,1);b.classList.remove("active");b.textContent="♡ 收藏文章"}
    else{f.push({url:url,title:title});b.classList.add("active");b.textContent="♥ 已收藏"}
    setFav(f);renderFavSide();
  });
  renderFavSide();
  // mark active on load
  (function(){
    var b=$(".fav-btn"); if(!b)return;
    if(getFav().some(function(x){return x.url===b.getAttribute("data-url")})){
      b.classList.add("active");b.textContent="♥ 已收藏";
    }
  })();

  /* ---------- floating dock mega menu ---------- */
  var dmgBtn=$("#dock-mega"), dmgPanel=$("#dock-mega-panel");
  if(dmgBtn&&dmgPanel){
    function dmgClose(){dmgPanel.hidden=true;dmgBtn.setAttribute("aria-expanded","false")}
    dmgBtn.addEventListener("click",function(e){
      e.stopPropagation();
      var open=dmgPanel.hidden;
      dmgClose();
      if(open){dmgPanel.hidden=false;dmgBtn.setAttribute("aria-expanded","true")}
    });
    document.addEventListener("click",function(e){
      if(!dmgPanel.hidden&&!e.target.closest(".dock-mega,.dock-mega-panel"))dmgClose();
    });
    document.addEventListener("keydown",function(e){if(e.key==="Escape")dmgClose()});
    window.addEventListener("resize",dmgClose);
  }

  /* ---------- faceted search ---------- */
  var facetRoot=$("#facet-root");
  if(facetRoot){
    loadIndex().then(function(){
      function state(){
        var s={level:[],need:[],price:[],feature:[]};
        $$(".facet-panel input:checked").forEach(function(c){s[c.name].push(c.value)});
        return s;
      }
      function apply(){
        var s=state(), q=($("#facet-q").value||"").trim().toLowerCase(), sort=$("#facet-sort").value;
        var res=idx.articles.filter(function(a){
          if(s.level.length&&s.level.indexOf(a.level)<0)return false;
          if(s.need.length&&!(a.need||[]).some(function(n){return s.need.indexOf(n)>=0}))return false;
          if(s.price.length&&s.price.indexOf(a.price)<0)return false;
          if(s.feature.length&&!(a.feature||[]).some(function(n){return s.feature.indexOf(n)>=0}))return false;
          if(q&&(a.title+" "+(a.tags||[]).join(" ")).toLowerCase().indexOf(q)<0)return false;
          return true;
        });
        if(sort==="level")res.sort(function(a,b){return a.level>b.level?1:-1});
        $("#facet-count").textContent=res.length;
        $("#facet-results").innerHTML=res.length?
          '<div class="cards">'+res.map(cardHtml).join("")+'</div>':
          '<p class="s-empty">沒有符合的結果，請減少篩選條件。</p>';
      }
      $(".facet-panel").addEventListener("change",apply);
      $("#facet-q").addEventListener("input",apply);
      $("#facet-sort").addEventListener("change",apply);
      $("#clear-facets").addEventListener("click",function(){
        $$(".facet-panel input:checked").forEach(function(c){c.checked=false});apply();
      });
      apply();
    });
  }
  function cardHtml(a){
    return '<article class="card"><a class="thumb" href="'+a.url+'"><img loading="lazy" src="'+a.thumb+'" alt="'+(a.thumbAlt||"")+'"></a>'+
      '<div class="body"><div class="meta"><span class="level">'+a.level+'</span><span>'+a.date+'</span></div>'+
      '<h3><a href="'+a.url+'">'+a.title+'</a></h3><p class="excerpt">'+(a.excerpt||"")+'</p>'+
      '<div class="tags">'+(a.tags||[]).slice(0,3).map(function(t){return '<span class="tag">#'+t+'</span>'}).join("")+'</div></div></article>';
  }

  /* ---------- knowledge graph ---------- */
  var cv=$("#graph-canvas");
  if(cv){
    loadIndex().then(function(){
      var nodes=[],links=[];
      var cx=420,cy=210;
      nodes.push({id:"core",label:"文具與鋼筆",x:cx,y:cy,r:34,core:true});
      idx.categories.forEach(function(c,i){
        var ang=i/idx.categories.length*Math.PI*2-Math.PI/2;
        var x=cx+Math.cos(ang)*150,y=cy+Math.sin(ang)*120;
        nodes.push({id:c.slug,label:c.title,x:x,y:cy?y:y,r:20,url:c.url,color:c.color});
        links.push({s:"core",t:c.slug});
      });
      drawGraph(cv,nodes,links);
    });
  }
  function drawGraph(cv,nodes,links){
    var ctx=cv.getContext("2d"), dpr=window.devicePixelRatio||1;
    function size(){var r=cv.getBoundingClientRect();cv.width=r.width*dpr;cv.height=r.height*dpr;ctx.setTransform(dpr,0,0,dpr,0,0)}
    size();window.addEventListener("resize",size);
    function frame(){
      var w=cv.clientWidth,h=cv.clientHeight,sc=Math.min(w/840,h/420);
      ctx.clearRect(0,0,w,h);
      var ox=w/2-420*sc, oy=h/2-210*sc;
      ctx.strokeStyle="rgba(120,120,120,.4)";ctx.lineWidth=1.5;
      links.forEach(function(l){
        var a=nodes.find(function(n){return n.id===l.s}),b=nodes.find(function(n){return n.id===l.t});
        ctx.beginPath();ctx.moveTo(ox+a.x*sc,oy+a.y*sc);ctx.lineTo(ox+b.x*sc,oy+b.y*sc);ctx.stroke();
      });
      nodes.forEach(function(n){
        var x=ox+n.x*sc,y=oy+n.y*sc;
        ctx.beginPath();ctx.arc(x,y,n.r*sc,0,7);
        ctx.fillStyle=n.core?getCSS("--primary"):(n.color||getCSS("--accent"));ctx.fill();
        ctx.fillStyle="#fff";ctx.font=(n.core?14:11)+"px Microsoft JhengHei";
        ctx.textAlign="center";ctx.fillText(n.label,x,y-(n.r*sc)-6);
      });
      cv.addEventListener("click",function(e){
        var r=cv.getBoundingClientRect(),mx=(e.clientX-r.left-ox)/sc,my=(e.clientY-r.top-oy)/sc;
        nodes.forEach(function(n){if(!n.core){var dx=mx-n.x,dy=my-n.y;if(dx*dx+dy*dy<(n.r+8)*(n.r+8)&&n.url)location.href=n.url}});
      });
    }
    frame();
  }
  function getCSS(n){return getComputedStyle(document.documentElement).getPropertyValue(n).trim()}
})();
