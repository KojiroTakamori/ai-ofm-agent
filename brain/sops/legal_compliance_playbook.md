# SOP: Legal, Compliance & Platform ToS Protection (Zero-Risk Protocol)

Acest protocol traduce avertismentul lui Nick de la minutul `00:36:40` (*"From a legal aspect it's a total different story... it's been a struggle for us to maintain the right line with the legal things because things can go up extremely quickly"*) într-un **Scut Juridic & Tehnic Automatizat**.

---

## 1. Cei 5 Piloni de Risc Legal în AI OFM (SUA, UE / România & Platforme)

### Pilonul A: Dreptul la Imagine & Interzicerea Deepfake-urilor Neconsensuale
- **Risc critic:** Folosirea feței unei persoane reale (influencer, model real, celebritate) prin *face-swap* fără contract de cesiune a drepturilor de imagine încalcă legislația penală și civilă din SUA (*TAKE IT DOWN Act*, *State Right of Publicity*) și UE (*AI Act* / GDPR).
- **Regula Agentului (`SYNTHETIC_LINEAGE_ONLY`):**
  - Fiecare model AI din agenție trebuie să aibă un **Seed Sintetic Original** (generat din combinarea a 3+ latenți sintetici / LoRA-uri originale, verificat prin reverse-image search să nu corespundă niciunei persoane reale).
  - Sau, dacă se folosește trăsătura unei persoane reale, existența obligatorie în dosarul modelului a **Contractului de Licențiere Likeness (KYC + Release Form semnat)**.

### Pilonul B: Toleranță Zero pentru Vârstă Ambiguă & Teme Interzise (21+ Strict Policy)
- **Risc critic:** Orice aluzie la minori, liceu (*"high school"*, *"teen"*, *"barely 18"*, *"schoolgirl"*), incest, lipsă de consimțământ (*non-consensual / forced*), violență sau substanțe ilegale atrage blocarea instantanee a procesatorilor de plăți (Visa/Mastercard) și răspundere penală.
- **Regula Agentului (`AGE_FLOOR_21` & `CHAT_FIREWALL`):**
  - Toate modelele AI au vârsta minimă declarată și vizuală de **21+ ani** (roluri permise: *universitate/college 21+, asistentă, instructor pilates, gamer, barista*).
  - **Firewall-ul de Chatting** scanează în timp real fiecare mesaj al fanului ȘI fiecare răspuns generat de AI. Dacă un fan încearcă să ducă discuția în zone ilegale, agentul refuză automat și rotește conversația sau blochează utilizatorul.

### Pilonul C: Anti-Solicitare Offline & Protecția Contului Fanvue / OF (Anti-Ban)
- **Risc critic:**
  1. Promisiunea de întâlniri fizice în schimbul banilor (*escorting / prostitution solicitation*) este ilegală și duce la închiderea contului.
  2. Acceptarea sau menționarea plăților în afara platformei (*CashApp, Venmo, PayPal, Crypto, Telegram*) în DM-urile de pe Fanvue/OnlyFans declanșează **ban automat cu confiscarea soldului**.
- **Regula Agentului (`PLATFORM_TOS_SHIELD`):**
  - Orice mesaj de la fan care conține *"meet up"*, *"how much for a night"*, *"cashapp"*, *"paypal"*, *"venmo"*, *"telegram"* este interceptat de `LegalGuardian`, iar chatbot-ul primește instrucțiune strictă să mențină interacțiunea **100% online și exclusiv prin sistemul de plăți Fanvue (Apple Pay / Card)**.

### Pilonul D: Protecție Anti-Chargeback & Fraudă Financiară (Whale Audit Trail)
- **Risc critic:** Dacă rata de *chargeback* (refuz la plată) depășește **1.0%**, contul agenției poate fi suspendat de procesatorii bancari.
- **Regula Agentului (`CHARGEBACK_EVIDENCE_LOGGER`):**
  - Pentru orice fan care devine **Whale (>$250)** sau cumpără PPV-uri High-Ticket (>$75), agentul salvează în baza de date un **Hash de Confirmare a Livrării & Consimțământului** (mesajul în care fanul confirmă că a deblocat și i-a plăcut clipul în `CH5` / `CH6`), probă imbatabilă în caz de dispută bancară.

### Pilonul E: Transparență AI & Conformitate EU AI Act / FTC
- Pe platformele de monetizare care cer marcarea creatorilor sintetici (precum categoria *AI Creators* de pe Fanvue), contul este înregistrat oficial ca model AI verificat, evitând acuzațiile de fraudă comercială, în timp ce experiența din chat rămâne imersivă (roleplay / entertainment).
