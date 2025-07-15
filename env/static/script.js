// static/script.js

const API_BASE = ""; // Se o front e back estiverem no mesmo host

// Metadados das categorias (ícones, cores e rótulos)
const CAT_META = {
  hard_skill:   { icon: "bi-tools",        color: "primary",   label: "Hard Skill" },
  soft_skill:   { icon: "bi-people",       color: "success",   label: "Soft Skill" },
  experiencia:  { icon: "bi-briefcase",    color: "warning",   label: "Experiência" },
  formacao:     { icon: "bi-mortarboard",  color: "info",      label: "Formação" },
  certificacao: { icon: "bi-patch-check",  color: "dark",      label: "Certificação" },
};

// ===== Função de Upload de CV =====
document.getElementById("form-upload").addEventListener("submit", async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById("cv-file");
  if (!fileInput.files.length) return;

  // Preparar feedback de loading
  const container = document.getElementById("upload-result");
  container.innerHTML = `
    <div class="text-center w-100">
      <div class="spinner-border text-success" role="status"></div>
      <p class="mt-2">Processando currículo…</p>
    </div>`;

  // Monta FormData e faz requisição
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const res = await fetch(`${API_BASE}/analyze-cv`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error(`Erro ${res.status}`);
    const data = await res.json();

    // 1) Exibe o card de Resumo + Score
    container.innerHTML = `
      <div class="col-12">
        <div class="card shadow-sm mb-4">
          <div class="card-body">
            <h5 class="card-title"><i class="bi bi-card-text me-2"></i>Resumo</h5>
            <p>${data.summary ?? "<em>— não disponível —</em>"}</p>
            <h6>Pontuação: <span class="badge bg-primary">${data.score ?? "—"}</span></h6>
            ${data.gpt_error
              ? `<div class="alert alert-warning mt-3">
                   <strong>GPT Error:</strong> ${data.gpt_error}
                   <details class="mt-2"><summary>Mostrar raw_ai</summary>
                     <pre class="small bg-light p-2">${data.raw_ai}</pre>
                   </details>
                 </div>`
              : ""
            }
          </div>
        </div>
      </div>`;

    // 2) Exibe os cards de cada categoria de entidade
    for (const key of Object.keys(data)) {
      const val = data[key];
      if (!Array.isArray(val)) continue;  // pula summary e curriculo_nome
      const meta = CAT_META[key];
      const items = val.length ? val : ["— vazio —"];
      const col = document.createElement("div");
      col.className = "col-12 col-md-6 col-lg-4";
      col.innerHTML = `
        <div class="card shadow-sm h-100 mb-4">
          <div class="card-header bg-${meta.color} text-white">
            <i class="bi ${meta.icon} me-2"></i>${meta.label}
          </div>
          <div class="card-body">
            ${items.map(i => 
              `<span class="badge bg-${meta.color} badge-entity">${i}</span>`
            ).join("")}
          </div>
        </div>`;
      container.append(col);
    }

  } catch (err) {
    container.innerHTML = `<div class="alert alert-danger">Falha: ${err.message}</div>`;
  }
});

// ===== Função de Busca de CVs =====
document.getElementById("form-search").addEventListener("submit", async (e) => {
  e.preventDefault();
  const category = document.getElementById("search-category").value;
  const value = document.getElementById("search-value").value.trim();
  const ul = document.getElementById("search-result");

  // Loading da busca
  ul.innerHTML = `<li class="list-group-item text-center">
                    <div class="spinner-border spinner-border-sm me-2" role="status"></div>Buscando…
                  </li>`;

  try {
    const res = await fetch(
      `${API_BASE}/search?category=${encodeURIComponent(category)}&value=${encodeURIComponent(value)}`
    );
    if (!res.ok) throw new Error(res.statusText);
    const { cvs } = await res.json();

    if (!cvs.length) {
      ul.innerHTML = `<li class="list-group-item text-muted">Nenhum currículo encontrado.</li>`;
    } else {
      ul.innerHTML = cvs.map(f => 
        `<li class="list-group-item"><i class="bi bi-file-earmark-text me-2"></i>${f}</li>`
      ).join("");
    }
  } catch (err) {
    ul.innerHTML = `<li class="list-group-item text-danger">Erro: ${err.message}</li>`;
  }
});
