# AI OFM Agent — Autonomous 6-Layer Agency System

Proiect creat în `F:\KJT\Assests\AI OFM Agent` (`/mnt/f/KJT/Assests/AI OFM Agent`), bazat pe arhitectura operațională de **$1,000,000/lună** analizată din interviul lui **Dr. Hadi & Nick** ([docs/ANALIZA_COMPLETA_AI_OFM_1M_MONTH.md](./docs/ANALIZA_COMPLETA_AI_OFM_1M_MONTH.md)).

## Structura Proiectului

```text
F:\KJT\Assests\AI OFM Agent\
├── docs/
│   ├── ANALIZA_COMPLETA_AI_OFM_1M_MONTH.md   # Analiza A-Z și cuvânt cu cuvânt a videoclipului
│   └── transcript_en.txt                     # Transcriptul integral cu timestamp-uri (1.650 linii)
├── brain/                                    # LAYER 1: Central Agency Brain (Context Folders)
│   ├── agency_overview.md                    # Sumar executiv actualizat automat
│   ├── departments/                          # Log-urile interconectate ale managerilor
│   ├── models/                               # KPIs.json pentru fiecare model AI
│   └── sops/                                 # Playbook-urile de Chatting (6 Capitole) & Viral Hooks
├── data/
│   └── ofm_agency.db                         # Baza de date SQLite (Modele, Fani, Vault, PPV Ledger, Telefoane)
└── src/ofm_agent/
    ├── config.py                             # Guardrails: CAC max $7, LTV min $12, Whale $250
    ├── db/database.py                        # Schema SQLite
    ├── brain/context_engine.py               # LAYER 1: Interconnected Manager Context Engine
    ├── chatting/state_machine.py             # LAYER 2: 6-Chapter Overnight Closer ($10k/night architecture)
    ├── factory/persona_gen.py                # LAYER 3: Model Factory & Anti-Generation-Frenzy Guard
    ├── traffic/matrix_manager.py             # LAYER 4: 5 Models x 30 Physical iPhone Accounts & Hook Gen
    ├── analytics/kpi_gatekeeper.py           # LAYER 5: Unit Economics Auditor (SCALE / OPTIMIZE / KILL)
    └── cli.py                                # LAYER 6: CLI Control Center
```

## Comenzi Rapide (CLI)

```bash
# 1. Inițializează Stage-1 (5 Modele US + Minimum Viable Vault + 150 Conturi pe iPhone-uri fizice)
PYTHONPATH=src python3 -m ofm_agent.cli init-stage1

# 2. Rulează Auditul Financiar (Layer 5 KPI Gatekeeper: CAC vs LTV -> SCALE / KILL)
PYTHONPATH=src python3 -m ofm_agent.cli kpi-audit

# 3. Simulează Chatbot-ul pe 6 Capitole (Layer 2 Overnight Closer + Apple Pay PPV + Whale Detection)
PYTHONPATH=src python3 -m ofm_agent.cli simulate-chat --model chloe-texas

# 4. Întreabă "Creierul Central al Agenției" (Layer 1 Interconnected Brain)
PYTHONPATH=src python3 -m ofm_agent.cli brain-ask "Care este statusul agenției și ce modele scalăm azi?"

# 5. Generează Scripturi de Reels pe formula de Conversie Inversată (Layer 4)
PYTHONPATH=src python3 -m ofm_agent.cli generate-hooks --model mia-cali
```
