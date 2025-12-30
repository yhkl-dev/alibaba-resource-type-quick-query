// Load a.json and implement quick search UI
(async function(){
  const qInput = document.getElementById('q');
  const resultsEl = document.getElementById('results');
  const countEl = document.getElementById('count');
  const fuzzyCheckbox = document.getElementById('fuzzy');

  let resources = [];

  async function loadData(){
    try{
      const resp = await fetch('a.json');
      const data = await resp.json();
      resources = (data.ResourceTypes || data.ResourceTypes) .map(r => r.ResourceType).filter(Boolean);
    }catch(err){
      console.error('Failed to load a.json', err);
      resources = [];
    }
  }

  function highlight(text, q){
    if(!q) return text;
    const esc = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(esc, 'ig');
    return text.replace(re, m => `<span class="hl">${m}</span>`);
  }

  function search(q){
    if(!q) return resources.slice(0,200);
    const ql = q.toLowerCase();
    const fuzzy = fuzzyCheckbox.checked;
    const out = [];
    for(const r of resources){
      const rl = r.toLowerCase();
      let ok = false;
      if(fuzzy){
        // fuzzy: check that all chars of q appear in order in r
        let i = 0;
        for(const ch of ql){
          i = rl.indexOf(ch, i);
          if(i === -1){ ok = false; break; }
          ok = true; i++;
        }
      }else{
        ok = rl.includes(ql);
      }
      if(ok) out.push(r);
      if(out.length >= 200) break;
    }
    return out;
  }

  function render(list, q){
    resultsEl.innerHTML = '';
    countEl.textContent = `结果: ${list.length}`;
    for(const r of list){
      const li = document.createElement('li');
      li.innerHTML = `<span class="res">${highlight(r, q)}</span>`;
      const btn = document.createElement('button');
      btn.textContent = '复制';
      btn.className = 'copy';
      btn.addEventListener('click', async ()=>{
        try{ await navigator.clipboard.writeText(r); btn.textContent = '已复制'; setTimeout(()=>btn.textContent='复制',900); }
        catch(e){ alert('复制失败，请手动复制: '+r); }
      });
      li.appendChild(btn);
      resultsEl.appendChild(li);
    }
  }

  function onInput(){
    const q = qInput.value.trim();
    const l = search(q);
    render(l, q);
  }

  await loadData();
  qInput.addEventListener('input', onInput);
  fuzzyCheckbox.addEventListener('change', onInput);
  // initial render
  render(resources.slice(0,200), '');
})();
