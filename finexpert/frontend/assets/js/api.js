/* Cliente HTTP para la API de MARA */

const API_BASE = "http://localhost:5000";

/** Envía el perfil al endpoint /diagnose y retorna el diagnóstico. */
async function fetchDiagnosis(profile) {
  const res = await fetch(`${API_BASE}/diagnose`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

/** Solicita la explicación detallada de una regla específica. */
async function fetchExplain(profile, reglaId) {
  const res = await fetch(`${API_BASE}/explain`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ perfil: profile, regla: reglaId }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `HTTP ${res.status}`);
  }
  return res.json();
}

/** Verifica que el backend esté disponible. */
async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    return res.ok;
  } catch {
    return false;
  }
}
