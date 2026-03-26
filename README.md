# MARA — Personal Finance Monitor and Advisor

**MARA** is a forward-chaining Knowledge-Based System (KBS) that diagnoses the financial health of a Mexican user and generates personalized, prioritized, and explainable recommendations.

Developers: **Mario Ávila** · **Eduardo Figueroa**

![Preview light mode](architecture/preview1.png)
![Preview dark mode](architecture/preview2.png)

---

## Features

- Simplified RETE inference engine (Match → Select → Execute cycle)
- 80 production rules across 6 domains: diagnosis, debt, savings, risk profile, investment, and forecast
- Conflict resolution by priority → specificity → certainty factor
- Explainability: "Why?" panel exposing the full reasoning chain
- Flask REST API (`/diagnose`, `/explain`, `/health`) with backend input validation
- 4-step wizard frontend with a financial traffic light and 6-month projection chart
- Dark / light mode with `localStorage` persistence
- ES / EN internationalization (knowledge base stays in Spanish)
- Two-layer form validation: frontend (per-step, range/type) and backend (HTTP 400 with descriptive message)
- 152 automated tests (unit + integration)
- Knowledge base grounded in CONDUSEF / CNBV / Banxico / ENIF 2021 standards
- 3D animated node-network background built with [Three.js](https://threejs.org/) r148 — reacts to scroll and mouse movement, adapts colors to the active theme

---

## Architecture

```
finexpert/
├── backend/
│   ├── app.py                   ← Flask: /diagnose, /explain, /health + input validation
│   ├── config.py                ← Environment variables
│   ├── engine/
│   │   ├── inference_engine.py  ← Match-Select-Execute cycle
│   │   ├── working_memory.py    ← Active session facts
│   │   ├── agenda.py            ← MATCH phase + selection
│   │   ├── conflict_resolver.py ← Priority → specificity → certainty
│   │   └── explainer.py         ← Natural-language traceability
│   ├── knowledge/
│   │   ├── knowledge_base.py    ← JSON rule loader and validator
│   │   ├── fact_base.py         ← CONDUSEF/CNBV/Banxico thresholds
│   │   ├── rules/               ← 80 rules in 6 JSON files
│   │   └── ontology/            ← Domain concepts and thresholds
│   ├── models/
│   │   ├── user_profile.py      ← UserProfile + Diagnosis + Recommendation
│   │   └── rule.py              ← Rule + Condition (dataclasses)
│   └── utils/
│       ├── calculators.py       ← Pure financial functions
│       ├── validators.py        ← Range and type validation (called from app.py)
│       └── logger.py            ← Centralized logging configuration
├── frontend/
│   ├── index.html               ← SPA: 4-step wizard + dashboard, data-i18n attributes
│   ├── assets/
│   │   ├── css/
│   │   │   ├── main.css         ← CSS variables, dark mode ([data-theme="dark"]), controls bar
│   │   │   ├── wizard.css       ← Progress, steps, sections
│   │   │   └── dashboard.css    ← Traffic light, metrics, recommendations, dark mode overrides
│   │   ├── js/
│   │   │   ├── theme.js         ← Light/dark toggle, localStorage persistence
│   │   │   ├── i18n.js          ← ES/EN translations, applyTranslations(), persistence
│   │   │   ├── api.js           ← fetchDiagnosis(), fetchExplain(), checkHealth()
│   │   │   ├── wizard.js        ← Navigation, per-step validation, buildProfile()
│   │   │   ├── dashboard.js     ← renderDashboard(), metrics and situation with i18n
│   │   │   ├── charts.js        ← Chart.js chart with theme-aware colors
│   │   │   ├── explainer.js     ← "Why?" panel per rule
│   │   │   ├── background.js    ← Three.js 3D node-network background
│   │   │   └── three.min.js     ← Three.js r148 (local, no CDN dependency)
│   │   └── img/
│   │       └── logo.svg         ← Minimalist vector logo (polyline + circle)
└── tests/
    ├── unit/                    ← 9 unit test files
    └── integration/             ← 6 integration test files
```

### Inference flow

```
UserProfile → to_initial_facts() → WorkingMemory
                                       ↓
                    ┌──────────────────────────────┐
                    │   Match-Select-Execute cycle  │
                    │  ┌────────────────────────┐   │
                    │  │ MATCH: evaluate IF of  │   │
                    │  │ all rules              │   │
                    │  └──────────┬─────────────┘   │
                    │             ↓                  │
                    │  ┌────────────────────────┐   │
                    │  │ SELECT: ConflictResolver│   │
                    │  │ (prio → spec → cert)   │   │
                    │  └──────────┬─────────────┘   │
                    │             ↓                  │
                    │  ┌────────────────────────┐   │
                    │  │ EXECUTE: assert_fact() │   │
                    │  │ + Explainer.record()   │   │
                    │  └────────────────────────┘   │
                    └──────────────────────────────┘
                                       ↓
                                  Diagnosis
                    (situacion, semaforo, certeza,
                     recomendaciones, proyeccion_6m,
                     cadena_inferencia)
```

---

## Production rules

| Domain          | Rules | Example derived facts                                              |
|-----------------|-------|--------------------------------------------------------------------|
| `diagnostico`   | 20    | `situacion`, `alerta_DAI_alto`, `alerta_tasa_usuraria`             |
| `deuda`         | 15    | `nivel_endeudamiento`, `estrategia_deuda`, `accion_urgente_deuda`  |
| `ahorro`        | 15    | `nivel_fondo_emergencia`, `nivel_ahorro`, `urgencia_fondo_emergencia` |
| `perfil_riesgo` | 10    | `perfil_riesgo`, `tolerancia_riesgo`, `puede_invertir_renta_variable` |
| `inversion`     | 10    | `instrumento`, `recomendacion_diversificar_portafolio`             |
| `pronostico`    | 10    | `pronostico_6m`, `urgencia_intervencion`, `alerta_riesgo_insolvencia` |

All thresholds are based on CONDUSEF/CNBV/Banxico standards and the National Financial Inclusion Survey (ENIF) 2021.

---

## Setup and usage

### Requirements
- Python 3.11+
- A modern browser (for the frontend)

### Backend

```bash
cd finexpert/backend
pip install -r requirements.txt
python app.py
# Server running at http://localhost:5000
```

### Frontend

Open `finexpert/frontend/index.html` in the browser.
The frontend calls the backend at `http://localhost:5000` by default.

> **Tip:** to avoid CORB issues when opening via `file://`, serve the frontend with a simple static server:
> ```bash
> cd finexpert/frontend
> python -m http.server 8080
> ```

### Optional environment variables

| Variable       | Default | Description                      |
|----------------|---------|----------------------------------|
| `FLASK_PORT`   | `5000`  | Flask server port                |
| `FLASK_DEBUG`  | `false` | Flask debug mode                 |
| `LOG_LEVEL`    | `INFO`  | Logging level                    |
| `CORS_ORIGINS` | `*`     | Allowed CORS origins             |

---

## REST API

### `GET /health`
```json
{ "status": "ok", "sistema": "MARA", "reglas_cargadas": 80 }
```

### `POST /diagnose`
**Body:** user profile (see fields in `models/user_profile.py`)

**Required fields:** `ingreso_mensual`, `gastos_fijos`, `gastos_variables`

The backend validates ranges before running the engine (age 18–99, rate 0–200, etc.) and returns `400` with a descriptive message on error.

**Response:**
```json
{
  "situacion": "en_riesgo",
  "nivel_certeza": 82,
  "semaforo": "amarillo",
  "recomendaciones": [...],
  "hechos_derivados": {...},
  "cadena_inferencia": [...],
  "proyeccion_6m": [0, 1100, 2200, 3300, 4400, 5500, 6600]
}
```

### `POST /explain`
```json
{
  "perfil": { ...same fields as /diagnose... },
  "regla": "D03"
}
```

---

## Input validation

Validation happens in two layers:

**Frontend (`wizard.js`)** — before advancing each step:

| Step | Field                    | Rule                         |
|------|--------------------------|------------------------------|
| 1    | `edad`                   | Integer, 18–99               |
| 1    | `num_dependientes`       | 0–10                         |
| 2    | `ingreso_mensual`        | > 0                          |
| 2    | `gastos_fijos/variables` | ≥ 0                          |
| 2    | `tasa_promedio_anual`    | 0–200 %                      |
| 3    | `horizonte_temporal`     | Integer, 1–600 months        |
| 3    | `meses_fondo_emergencia` | 0–36 months                  |

**Backend (`validators.py` → `app.py`)** — on every call to `/diagnose` and `/explain`:
- Required fields present and non-negative
- Age 18–99 if provided
- Interest rate in valid range

Frontend error messages are available in both ES and EN.

---

## UI

### Dark / light mode

The `☾/☀` toggle in the controls bar (top-right corner) switches themes.
The preference is persisted in `localStorage` and applied before page render to avoid a flash of wrong theme.

Dark mode is implemented with CSS custom properties under `[data-theme="dark"]` in `main.css` and `dashboard.css`, without duplicating class names.

### Internationalization (ES / EN)

The `ES | EN` button in the controls bar switches the UI language.
The preference is persisted in `localStorage`.

- DOM texts are translated via `data-i18n`, `data-i18n-ph` (placeholders), and `data-i18n-title` (tooltips) attributes.
- The knowledge base and engine-generated recommendations always remain in Spanish.
- In EN mode an informational note is shown on the dashboard explaining this behavior.

### 3D background

An animated node-network rendered with **Three.js r148** covers the full viewport as a fixed canvas (z-index 1). Cards use glassmorphism (`backdrop-filter: blur`) so the network shows through. The camera reacts to scroll (Y-rotation) and mouse position (X/Y pitch). Colors adapt automatically when the theme is toggled via a `MutationObserver`.

---

## Tests

```bash
cd finexpert
pytest                    # all tests
pytest tests/unit/        # unit only
pytest tests/integration/ # integration only
pytest --cov=backend      # with coverage
```

```
152 passed  (0.33s)
```

---

## Financial traffic light

| Color  | Situation            | Characteristic condition                  |
|--------|----------------------|-------------------------------------------|
| Red    | Critical / Extreme   | expense_ratio > 70 % or DAI > 50 %       |
| Yellow | At risk / Moderate   | savings < 10 % or fixed expenses 50–70 % |
| Green  | Healthy              | fixed expenses ≤ 50 % and savings ≥ 20 % |
| Grey   | No data              | Insufficient information                  |
