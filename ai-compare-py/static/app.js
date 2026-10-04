const $ = id => document.getElementById(id);
const sel = new Set();
let models = {}, outs = {}, prompt = "", picked = null, convo = [];

const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
async function api(path, body) {
  const r = await fetch(path, body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : undefined);
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.detail ? JSON.stringify(j.detail) : "Request failed");
  return j;
}

async function init() {
  (await api("/api/models")).forEach(m => {
    models[m.id] = m;
    const b = el("button", "rounded-full border px-4 py-1.5 text-sm transition " +
      (m.ready ? "border-stone-300 hover:border-emerald-700 dark:border-stone-700" : "cursor-not-allowed border-stone-200 text-stone-400 dark:border-stone-800"),
      m.label + (m.ready ? "" : " (no key)"));
    b.disabled = !m.ready; b.title = m.model;
    b.onclick = () => {
      sel.has(m.id) ? sel.delete(m.id) : sel.add(m.id);
      b.classList.toggle("bg-emerald-700", sel.has(m.id)); b.classList.toggle("text-white", sel.has(m.id));
      update();
    };
    $("chips").appendChild(b);
  });
  loadHistory();
}
function update() {
  $("send").disabled = !(sel.size >= 2 && $("prompt").value.trim());
  $("hint").textContent = sel.size < 2 ? "Select 2 or more models." : sel.size + " models selected.";
}
$("prompt").addEventListener("input", update);

$("send").onclick = () => {
  prompt = $("prompt").value.trim(); outs = {}; picked = null;
  $("final").classList.add("hidden"); $("results").classList.remove("hidden"); $("grid").innerHTML = "";
  sel.forEach(id => {
    const card = el("div", "flex flex-col gap-3 rounded-xl border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900");
    card.id = "c-" + id;
    const head = el("div", "flex justify-between"); head.append(el("h3", "font-medium", models[id].label), el("span", "text-xs text-stone-400", models[id].model));
    const out = el("div", "min-h-[7rem] flex-1 whitespace-pre-wrap animate-pulse text-stone-400", "Waiting for reply…");
    const meta = el("div", "text-xs text-stone-500"), acts = el("div");
    card.append(head, out, meta, acts); $("grid").appendChild(card);
    api("/api/ask", { model: id, messages: [{ role: "user", content: prompt }] }).then(r => {
      out.classList.remove("animate-pulse", "text-stone-400");
      if (r.error) { out.textContent = "Error: " + r.error; out.classList.add("text-red-600"); return; }
      outs[id] = r.text; out.textContent = r.text;
      meta.textContent = r.text.split(/\s+/).filter(Boolean).length + " words, " + (r.ms / 1000).toFixed(1) + "s";
      const b = el("button", "rounded-md border border-stone-300 px-3 py-1.5 text-sm hover:border-emerald-700 dark:border-stone-700", "Use this one");
      b.onclick = () => pick(id); acts.appendChild(b);
    }).catch(e => { out.classList.remove("animate-pulse"); out.textContent = "Error: " + e.message; });
  });
  $("results").scrollIntoView({ behavior: "smooth" });
};

function pick(id) {
  picked = id;
  document.querySelectorAll("#grid > div").forEach(c => c.classList.toggle("ring-2", c.id === "c-" + id));
  document.querySelectorAll("#grid > div").forEach(c => c.classList.toggle("ring-emerald-600", c.id === "c-" + id));
  $("fname").textContent = models[id].label + "'s output"; $("ftext").textContent = outs[id];
  convo = [{ role: "user", content: prompt }, { role: "assistant", content: outs[id] }];
  $("final").classList.remove("hidden"); $("final").scrollIntoView({ behavior: "smooth" });
  api("/api/select", { prompt, model: id, output: outs[id], outputs: outs }).then(loadHistory).catch(() => {});
}

$("copy").onclick = async () => {
  try { await navigator.clipboard.writeText($("ftext").textContent); $("fmsg").textContent = "Copied."; }
  catch { $("fmsg").textContent = "Copy failed. Select the text and copy it manually."; }
};
$("refine").onclick = () => { $("refrow").classList.toggle("hidden"); $("refrow").classList.toggle("flex"); };
$("go").onclick = async () => {
  const f = $("follow").value.trim(); if (!f) return;
  $("go").disabled = true; $("fmsg").textContent = "Refining…";
  convo[1].content = $("ftext").textContent; // keep manual edits
  try {
    const r = await api("/api/ask", { model: picked, messages: [...convo, { role: "user", content: f }] });
    if (r.error) throw new Error(r.error);
    convo.push({ role: "user", content: f }, { role: "assistant", content: r.text });
    $("ftext").textContent = r.text; $("follow").value = ""; $("fmsg").textContent = "Refined by " + models[picked].label + ".";
  } catch (e) { $("fmsg").textContent = "Error: " + e.message; }
  $("go").disabled = false;
};

async function loadHistory() {
  const ul = $("history"); ul.innerHTML = "";
  try {
    const rows = await api("/api/history?limit=10");
    if (!rows.length) ul.appendChild(el("li", "text-stone-500", "Nothing saved yet. Picks you make will appear here."));
    rows.forEach(r => { const li = el("li", "rounded border border-stone-200 p-3 dark:border-stone-800");
      li.append(el("div", "font-medium", r.prompt.slice(0, 120)), el("div", "text-stone-500", (models[r.model]?.label || r.model) + ": " + r.output.slice(0, 160))); ul.appendChild(li); });
  } catch {}
}
init();
