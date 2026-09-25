# Report ambiente Python e strumenti collegati

> Data analisi: 2026-09-25 · Macchina: Windows 11 Home 10.0.26200 · CPU AMD (8 thread) · RAM 7,2 GB · GPU AMD Radeon (integrata)
> Utilizzo dichiarato: data science, sviluppo app/web, script e automazione.

---

## 1. Sintesi

| Area | Stato | Nota principale |
|---|---|---|
| Interprete Python | 🟡 | Uno solo attivo: **Python 3.13.14 dal Microsoft Store**. Nessun `py` launcher. |
| Ambienti virtuali | 🔴 | **Nessun venv/conda trovato.** Tutti i 185 pacchetti sono installati in un unico ambiente globale (~2,5 GB). |
| Comandi installati da pip | 🔴 | La cartella `Scripts` dei pacchetti **non è nel PATH**: `jupyter`, `uvicorn`, `fastapi`, `spacy`, `whisper`, `ipython`… non si avviano da terminale. |
| Variabile PATH | 🟡 | Il PATH utente **duplica 11 voci** del PATH di sistema. |
| Long paths di Windows | 🔴 | `LongPathsEnabled = 0` → rischio di errori con pip su pacchetti grandi (torch, jupyter). |
| Pacchetti | 🟡 | `pip check` OK, ma **67 pacchetti obsoleti** (alcuni aggiornamenti "major": pandas 3, thinc 9). |
| Jupyter | 🟡 | Kernel presente (usato da VS Code), ma **JupyterLab/Notebook non installati**. |
| Riproducibilità progetto | 🔴 | Il progetto `11_potfolio` non ha `requirements.txt`/`pyproject.toml`. |
| Strumenti collegati | 🟡 | Resti di `uv` (Python 3.13.5 orfano), `fnm` non inizializzato, 3 installazioni Java. |
| Segreti nelle variabili | 🟢 | Nessuna API key/token trovata nelle variabili d'ambiente. |

---

## 2. Variabili d'ambiente

### 2.1 Variabili utente (`HKCU\Environment`)

| Variabile | Valore |
|---|---|
| `KAGGLEHUB_CACHE` | `C:\Users\napol\Documents\SECOND BRAIN\10_Projects\11_potfolio` |
| `OneDrive` | `C:\Users\napol\OneDrive` |
| `TEMP` / `TMP` | `C:\Users\napol\AppData\Local\Temp` |
| `Path` | vedi §2.3 |

### 2.2 Variabili di sistema (`HKLM`)

| Variabile               | Valore                                                  | Commento                                                                               |
| ----------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `Classpath`             | `C:\LINGO64_21\Lingo21.jar`                             | Usata da LINGO (Java). Una CLASSPATH globale può interferire con altri programmi Java. |
| `ComSpec`               | `C:\WINDOWS\system32\cmd.exe`                           | Standard                                                                               |
| `DriverData`            | `C:\Windows\System32\Drivers\DriverData`                | Standard                                                                               |
| `NUMBER_OF_PROCESSORS`  | `8`                                                     | Standard                                                                               |
| `OS`                    | `Windows_NT`                                            | Standard                                                                               |
| `PATHEXT`               | `.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC` | Standard                                                                               |
| `PROCESSOR_*`           | AMD64 Family 23 Model 160 (Zen 2)                       | Standard                                                                               |
| `PSModulePath`          | moduli PowerShell standard                              | Standard                                                                               |
| `PT8HOME`               | `C:\Program Files\Cisco Packet Tracer 8.2.2`            | Cisco Packet Tracer                                                                    |
| `TEMP` / `TMP`          | `C:\WINDOWS\TEMP`                                       | Standard                                                                               |
| `USERNAME`              | `SYSTEM`                                                | Normale a livello macchina                                                             |
| `VBOX_MSI_INSTALL_PATH` | `C:\Users\napol\Documents\`                             | ⚠️ Anomala: residuo di VirtualBox che punta a Documenti                                |
| `windir`                | `C:\WINDOWS`                                            | Standard                                                                               |

**Variabili Python rilevanti:** `PYTHONPATH`, `PYTHONHOME`, `VIRTUAL_ENV`, `CONDA_*`, `PIP_*`, `UV_*` **non sono impostate** (bene: nessuna configurazione "nascosta").

Nel terminale di VS Code compaiono in più `PYTHONSTARTUP`, `PYTHONIOENCODING=utf-8:surrogateescape`, `PYTHON_BASIC_REPL=1`, `BUNDLED_DEBUGPY_PATH`, `PYDEVD_DISABLE_FILE_VALIDATION=1`: sono iniettate **solo per la sessione** dall'estensione Python di VS Code, non sono permanenti. È normale.

### 2.3 PATH

**PATH di sistema** (in ordine):
1. `C:\Program Files\Common Files\Oracle\Java\javapath`
2. `C:\Program Files (x86)\Common Files\Oracle\Java\java8path`
3. `C:\Program Files (x86)\Common Files\Oracle\Java\javapath`
4. `C:\WINDOWS\system32`
5. `C:\WINDOWS`
6. `C:\WINDOWS\System32\Wbem`
7. `C:\WINDOWS\System32\WindowsPowerShell\v1.0\`
8. `C:\WINDOWS\System32\OpenSSH\`
9. `C:\Program Files\MATLAB\R2024b\bin`
10. `C:\LINGO64_21\`
11. `C:\Program Files\Git\cmd`
12. `C:\Program Files\Docker\Docker\resources\bin`
13. `C:\Program Files\nodejs\`

**PATH utente** (in ordine) — le voci 1-12 sono **duplicati** del PATH di sistema:

| # | Voce | Stato |
|---|---|---|
| 1-12 | Java ×3, System32, Windows, Wbem, PowerShell, OpenSSH, MATLAB, LINGO, Docker, Git | 🔁 duplicate |
| 13 | `C:\Users\napol\AppData\Local\Microsoft\WindowsApps` | Alias Python Store (qui si risolve `python`) |
| 14 | `...\WinGet\Packages\Schniz.fnm_...` | fnm (gestore versioni Node) |
| 15 | `...\Programs\Microsoft VS Code\bin` | `code` |
| 16 | `C:\Users\napol\flutter\bin` | Flutter |
| 17 | `C:\Users\napol\ffmpeg-2026-04-09-git-...-full_build\bin` | ffmpeg (versione nel nome cartella) |
| 18 | `C:\Users\napol\.local\bin` | Claude Code |
| 19 | `...\Programs\Ollama` | Ollama |
| 20 | `C:\Users\napol\AppData\Roaming\npm` | pacchetti npm globali |
| 21 | `...\GitHubDesktop\bin` | GitHub Desktop |

**Manca:** `C:\Users\napol\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts` (dove pip mette gli eseguibili).

---

## 3. Installazioni Python

### 3.1 Interprete attivo

| Voce | Valore |
|---|---|
| Versione | **3.13.14** (MSC v.1944, 64 bit) |
| Origine | Microsoft Store — pacchetto `PythonSoftwareFoundation.Python.3.13` v3.13.3824.0 |
| Eseguibile risolto | `C:\Users\napol\AppData\Local\Microsoft\WindowsApps\python.exe` (App Execution Alias) |
| Installazione reale | `C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.13_3.13.3824.0_x64__qbz5n2kfra8p0` (sola lettura) |
| Pacchetti utente (site-packages) | `C:\Users\napol\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages` (~2,5 GB) |
| pip | 26.2.1 (nel site-packages utente) |
| Cache pip | `...\LocalCache\local\pip\cache` (~1,2 GB) |
| Config pip (`pip.ini`) | Nessuna |
| OpenSSL / SQLite | 3.0.21 / 3.50.4 |
| Alias registrati | `python`, `python3`, `python3.13`, `pythonw*`, `pip`, `pip3`, `pip3.13`, `idle*` |

### 3.2 Altre installazioni trovate

| Cosa | Percorso | Stato |
|---|---|---|
| CPython 3.13.5 gestito da **uv** | `C:\Users\napol\AppData\Roaming\uv\python\cpython-3.13.5-windows-x86_64-none` | Orfano: `uv` non è installato/nel PATH. Probabilmente scaricato da un tool che usa `uvx`. |
| Cache uv | `C:\Users\napol\AppData\Local\uv\cache` (~29 MB) | Residuo |
| `py` launcher | — | **Non installato** (il Python dello Store non lo include) |
| python.org, Anaconda/Miniconda, pyenv, pipx, poetry | — | Non presenti |

### 3.3 Ambienti virtuali

Nessun `pyvenv.cfg` trovato in Documenti, Desktop, OneDrive (profondità 6). Nessun kernel Jupyter registrato a mano. **Tutto gira nell'ambiente globale.**

---

## 4. Pacchetti installati (riepilogo ragionato)

185 pacchetti totali — lista completa in **Appendice A**. Raggruppati per funzione:

| Gruppo                   | Pacchetti principali                                                                                                                                                                                 |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data science**         | numpy 2.3.1, pandas 2.3.3, pyarrow 25.0.1, scipy 1.17.1, matplotlib 3.10.3, plotly 7.1.0, sympy 1.14, networkx 3.6.1, numba 0.65, openpyxl 3.1.5, pandasgui 0.2.15, wordcloud 1.9.6, kagglehub 1.0.2 |
| **Jupyter**              | ipykernel 7.3.0, ipython 9.17.1, ipywidgets 8.1.9, jupyter_server 2.21.1, nbconvert 7.17.1 — *senza* jupyterlab e notebook                                                                           |
| **NLP / AI**             | spacy 3.8.14 + modello `it_core_news_lg` 3.8.0, thinc 8.3.13, torch 2.11.0 (**solo CPU**), openai-whisper 20250625, tiktoken 0.12, wordfreq, ftfy                                                    |
| **Web / API**            | fastapi 0.136.3, starlette 1.2.1, uvicorn 0.49.0, pydantic 2.13.4, httpx 0.28.1, requests 2.32.4, websockets 16.0, python-multipart, python-dotenv                                                   |
| **PDF / OCR / immagini** | ocrmypdf 16.11.1, pikepdf 10.0.0, PyMuPDF 1.27.2.3, pdfminer.six, img2pdf, pillow 12.2.0, pi_heif, imageio, glmocr 0.1.5                                                                             |
| **GUI / automazione**    | PyQt5 5.15.11 + PyQtWebEngine, pynput 1.8.2, pywin32 311, psutil, Send2Trash                                                                                                                         |
| **Scraping**             | beautifulsoup4 4.15.0, lxml 6.0.2                                                                                                                                                                    |

**Stato dipendenze:** `pip check` → *No broken requirements found*. **67 aggiornamenti disponibili** (Appendice B).

**Cosa usa davvero il progetto `11_potfolio`:** solo `pandas` e `numpy` (+ `openpyxl` per `titoli_to_excel.py`, + `ipykernel` per i notebook).

---

## 5. Strumenti collegati

| Strumento | Versione | Percorso / note |
|---|---|---|
| VS Code | — | Estensioni: Python 2026.4.0, Python Environments 1.38.0, Debugpy 2026.6.0, Jupyter 2025.9.1 (+ keymap, renderers, cell-tags, slideshow), Data Wrangler 1.24.2 |
| Git | 2.52.0 | `C:\Program Files\Git\cmd` |
| Docker | 29.5.3 | `C:\Program Files\Docker\Docker\resources\bin` |
| Node.js | 24.18.0 (sistema) | `C:\Program Files\nodejs`. **fnm** 1.37.2 ha default v22.11.0 ma non è attivato (nessun profilo PowerShell) |
| Java | `java` → JDK **11.0.30** | Installati anche JRE 8u481 (32 e 64 bit) + Java Auto Updater; 3 voci `javapath` nel PATH |
| R / RStudio | 4.5.2 / 2026.09.0 | — |
| MATLAB | R2024b | nel PATH |
| LINGO | 21 | nel PATH + `Classpath` |
| Ollama | — | `...\Programs\Ollama` |
| Flutter, ffmpeg | — | cartelle nella home |
| Claude Code | — | `C:\Users\napol\.local\bin` (c'è anche un `claude.exe.old...` da ~240 MB) |
| Visual C++ Redistributable | 2013 e 2015-2022 (14.50) | Necessari per molte wheel Python — OK |
| Visual C++ **Build Tools** | — | **Non installati** (servono solo per compilare pacchetti senza wheel) |
| PowerShell | 5.1, ExecutionPolicy `RemoteSigned` | OK per attivare i venv (`Activate.ps1`) |

---

## 6. Problemi possibili con questa configurazione

### 🔴 P1 — Un unico ambiente globale per tutto
Data science, web, NLP, torch, PyQt5, OCR convivono nello stesso site-packages.
- **Conflitti di versione:** aggiornare un pacchetto per un progetto può rompere un altro (es. `pip install -U pandas` porta pandas 3.0, che ha cambi incompatibili; `thinc` 9 non è compatibile con spacy 3.8; `numpy` vincolato da numba/whisper).
- **Non riproducibile:** un progetto di portfolio che un recruiter/collega vuole eseguire non ha una lista di dipendenze. Tu stesso non potrai ricrearlo su un altro PC.
- **Difficile da pulire:** non sai più quali pacchetti servono a cosa.

### 🔴 P2 — Comandi pip non raggiungibili (Scripts fuori dal PATH)
Digitando `jupyter`, `uvicorn main:app`, `fastapi dev`, `spacy download`, `whisper file.mp3`, `ipython` → *"termine non riconosciuto"*. Anche `jupyter kernelspec list` fallisce internamente. Workaround attuale: `python -m <modulo>`.

### 🟡 P3 — Limiti del Python del Microsoft Store
- **Sandbox/virtualizzazione:** scritture in `%APPDATA%`/`%LOCALAPPDATA%` fatte da Python possono finire nella cartella virtualizzata `...\Packages\PythonSoftwareFoundation...\LocalCache` e risultare "invisibili" ad altri programmi.
- **Aggiornamenti automatici** dallo Store: la versione patch cambia senza avviso e il percorso reale contiene il numero di versione.
- **Percorsi lunghissimi** (vedi P4) e niente `py` launcher (non puoi scegliere facilmente la versione).
- Alcuni strumenti (PyInstaller, servizi Windows, task pianificati, alcuni IDE) gestiscono male gli *App Execution Alias*.
- Se in futuro installi Python da python.org, gli alias `python.exe` in `WindowsApps` possono "vincere" o confondere quale Python stai usando.

### 🔴 P4 — Long paths disabilitati
Con `LongPathsEnabled = 0` il limite è 260 caratteri. Il site-packages è già a ~130 caratteri: pacchetti con alberi profondi (jupyter, torch, spacy model) possono fallire con `OSError: [Errno 2] No such file or directory` o `could not install packages due to an OSError`.

### 🟡 P5 — PATH utente duplicato
11 voci del PATH di sistema sono ricopiate nel PATH utente (tipico di un vecchio `setx PATH "%PATH%;..."`). Effetti: PATH più lungo (rischio di troncamento a 1024 caratteri se in futuro usi `setx`), ricerca comandi più lenta e confusa, modifiche fatte in un solo posto che "non funzionano".

### 🟡 P6 — Pacchetti obsoleti
67 aggiornamenti disponibili, tra cui `certifi` (2025.6 → 2026.7: certificati SSL vecchi → possibili errori `CERTIFICATE_VERIFY_FAILED`), `cryptography` 46 → 50, `urllib3`, `requests`, `starlette`/`fastapi` (fix di sicurezza). Aggiornare tutto in blocco nell'ambiente globale però è rischioso (P1).

### 🟡 P7 — Jupyter incompleto
Il kernel c'è e VS Code funziona, ma `jupyter lab` / `jupyter notebook` non esistono. Senza venv, tutti i notebook usano lo stesso kernel globale.

### 🟡 P8 — Dati pesanti e poca RAM
Nella cartella del progetto ci sono ~2,9 GB di CSV (es. `guardian_articles.csv` 739 MB) e hai 7,2 GB di RAM. `pd.read_csv` su un file da 700 MB può occupare 3-5 GB in memoria → `MemoryError` o swap molto lento. Inoltre `KAGGLEHUB_CACHE` punta proprio a questa cartella del "Second Brain": ogni dataset scaricato con kagglehub finisce qui, gonfiando il vault (backup/sincronizzazione lenti, Obsidian che indicizza file enormi).

### 🟢/🟡 P9 — Nessuna accelerazione GPU
torch è la build **CPU** (`2.11.0+cpu`) e la GPU è AMD integrata (CUDA non disponibile). Whisper e modelli torch saranno lenti. Non è un errore di configurazione, ma è un limite da conoscere.

### 🟡 P10 — Residui e incoerenze negli strumenti collegati
- Python 3.13.5 di `uv` orfano: se un giorno installi `uv`, riusa quello (differente dallo Store 3.13.14).
- `fnm` installato ma non inizializzato → `node` è sempre la 24.18 di sistema, non la 22.11 che fnm considera default.
- 3 Java (JDK 11, JRE 8 ×2) e `Classpath` globale: rilevante solo se userai PySpark/tabula-py/JPype (servono Java 11+/17).
- `VBOX_MSI_INSTALL_PATH` punta a Documenti (residuo innocuo).
- Spazio recuperabile: cache pip ~1,2 GB, `claude.exe.old…` ~240 MB.

### 🟢 P11 — Sicurezza variabili
Non ci sono segreti nelle variabili d'ambiente. Nota però: `python-dotenv` è installato, quindi se usi file `.env` nei progetti assicurati che siano in `.gitignore`.

---

## 7. Modifiche consigliate (in ordine di priorità) e come farle

> Esegui i comandi in **PowerShell**. Quelli marcati *(admin)* richiedono "Esegui come amministratore". Prima di tutto fai il backup (passo 0).

### Passo 0 — Backup della situazione attuale
```powershell
# Backup lista pacchetti globali
python -m pip freeze > "$HOME\Documents\backup_pip_globale_2026-09-25.txt"

# Backup PATH utente e di sistema
[Environment]::GetEnvironmentVariable('Path','User')    | Out-File "$HOME\Documents\backup_PATH_user.txt"
[Environment]::GetEnvironmentVariable('Path','Machine') | Out-File "$HOME\Documents\backup_PATH_machine.txt"
```

### Passo 1 — Abilitare i long path *(admin)* → risolve P4
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name LongPathsEnabled -Value 1 -PropertyType DWORD -Force
```
Riavvia il PC. (In alternativa: `gpedit.msc` non c'è su Windows Home, quindi usa il comando sopra.)

### Passo 2 — Pulire il PATH utente dai duplicati → risolve P5
```powershell
$machine = [Environment]::GetEnvironmentVariable('Path','Machine') -split ';' | Where-Object { $_ } | ForEach-Object { $_.TrimEnd('\').ToLower() }
$user    = [Environment]::GetEnvironmentVariable('Path','User')    -split ';' | Where-Object { $_ }
$clean   = $user | Where-Object { $machine -notcontains $_.TrimEnd('\').ToLower() } | Select-Object -Unique
$clean                                   # controlla l'anteprima prima di salvare
[Environment]::SetEnvironmentVariable('Path', ($clean -join ';'), 'User')
```
Oppure a mano: *Start → "Modifica le variabili di ambiente relative al sistema" → Variabili d'ambiente → Path (utente) → Modifica* ed elimina le voci che già compaiono nel Path di sistema. Chiudi e riapri terminali e VS Code.

### Passo 3 — Installare `uv` come gestore di Python e ambienti → base per P1, P2, P3
`uv` sostituisce pip + venv + pyenv + pipx, è molto veloce e ne hai già dei residui.
```powershell
winget install --id=astral-sh.uv -e
# riapri il terminale
uv --version
uv python install 3.13        # Python "pulito" (non Store) gestito da uv
uv python list                # vedi quali interpreti conosce
```
Da qui in avanti la regola è: **un ambiente per progetto, niente installazioni globali.**

### Passo 4 — Creare l'ambiente del progetto `11_potfolio` → risolve P1, P7 e la riproducibilità
```powershell
cd "C:\Users\napol\Documents\SECOND BRAIN\10_Projects\11_potfolio"
uv init --bare                 # crea pyproject.toml
uv add pandas numpy openpyxl pyarrow
uv add --dev ipykernel jupyterlab
uv run jupyter lab             # oppure: .\.venv\Scripts\Activate.ps1
```
In VS Code: `Ctrl+Shift+P → Python: Select Interpreter → .venv` e, nei notebook, seleziona il kernel `.venv`.
Crea anche un `.gitignore` con almeno:
```
.venv/
*.csv
.env
```
(con `pyproject.toml` + `uv.lock` chiunque ricrea l'ambiente con `uv sync`).

Per gli altri usi fai lo stesso in cartelle separate, ad esempio:
- **Web/API:** `uv add fastapi uvicorn[standard] httpx python-dotenv` → `uv run uvicorn main:app --reload`
- **NLP:** `uv add spacy` → `uv run python -m spacy download it_core_news_lg`
- **Trascrizione/OCR:** ambiente dedicato con `openai-whisper` / `ocrmypdf` (torch è pesante: tenerlo isolato).

### Passo 5 — Strumenti da riga di comando globali → risolve P2
Per i comandi che vuoi sempre disponibili, usa `uv tool` (ogni tool nel suo ambiente isolato, eseguibile nel PATH):
```powershell
uv tool install jupyterlab     # se vuoi `jupyter lab` ovunque
uv tool install ruff           # linter/formatter consigliato
uv tool update-shell           # aggiunge la cartella dei tool al PATH
```
**Soluzione rapida alternativa** (se per ora vuoi restare sull'ambiente globale): aggiungi Scripts al PATH utente.
```powershell
$scripts = "$env:LOCALAPPDATA\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts"
$p = [Environment]::GetEnvironmentVariable('Path','User')
[Environment]::SetEnvironmentVariable('Path', "$p;$scripts", 'User')
```

### Passo 6 — Ridurre l'ambiente globale (dopo che i progetti hanno il loro venv)
Una volta verificato che i progetti funzionano nei loro `.venv`:
```powershell
python -m pip freeze > "$HOME\Documents\da_rimuovere.txt"
python -m pip uninstall -y -r "$HOME\Documents\da_rimuovere.txt"
python -m pip cache purge      # libera ~1,2 GB
```
Poi puoi valutare di disinstallare il Python dello Store (*Impostazioni → App → Python 3.13 → Disinstalla*) e disattivare gli alias (*Impostazioni → App → Impostazioni app avanzate → Alias di esecuzione app* → spegni `python.exe`/`python3.exe`), usando solo i Python di `uv`.
> Non aggiornare in blocco i 67 pacchetti nel globale: aggiornali dentro i singoli venv (`uv lock --upgrade`), dove un problema resta confinato.

### Passo 7 — Spostare la cache di kagglehub fuori dal vault → risolve parte di P8
```powershell
New-Item -ItemType Directory -Force "$env:LOCALAPPDATA\kagglehub" | Out-Null
[Environment]::SetEnvironmentVariable('KAGGLEHUB_CACHE', "$env:LOCALAPPDATA\kagglehub", 'User')
```
Valuta di tenere i CSV grandi in una cartella `data/` esclusa da git e da Obsidian (*Impostazioni → File e link → File esclusi*).

### Passo 8 — Lavorare con CSV grandi con 7 GB di RAM → P8
```python
import pandas as pd
# carica solo le colonne che servono e usa il backend Arrow (meno memoria)
df = pd.read_csv("guardian_articles.csv", usecols=["title", "date", "section"],
                 engine="pyarrow", dtype_backend="pyarrow")
# oppure a blocchi
for chunk in pd.read_csv("guardian_articles.csv", chunksize=200_000):
    ...
# salva i dati puliti in Parquet: ~3-5x più piccolo e molto più veloce da rileggere
df.to_parquet("guardian_articles_cleaned.parquet")
```
Per query su file enormi senza caricarli tutti valuta `duckdb` o `polars` (da aggiungere al venv del progetto).

### Passo 9 — Sistemare gli strumenti collegati → P10
```powershell
# fnm: crea il profilo PowerShell e attivalo
if (-not (Test-Path $PROFILE)) { New-Item -ItemType File -Force $PROFILE | Out-Null }
Add-Content $PROFILE 'fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression'

# rimuovere la variabile residua di VirtualBox (admin)
[Environment]::SetEnvironmentVariable('VBOX_MSI_INSTALL_PATH', $null, 'Machine')

# vecchio binario di Claude Code
Remove-Item "$HOME\.local\bin\claude.exe.old.*"
```
- Il Python 3.13.5 orfano di uv verrà gestito da `uv python list` / `uv python uninstall 3.13.5` dopo il Passo 3.
- Java: se non ti serve Java 8 (vecchie app), disinstalla "Java 8 Update 481" (entrambe) e "Java Auto Updater" da *Impostazioni → App*; resteranno JDK 11. Per PySpark futuro servirebbe JDK 17.
- Node: scegli **o** fnm **o** Node di sistema; tenerli entrambi crea ambiguità.

### Passo 10 (opzionale) — Build Tools
Solo se un `pip install` fallisce con *"Microsoft Visual C++ 14.0 or greater is required"*:
```powershell
winget install Microsoft.VisualStudio.2022.BuildTools --override "--quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

---

## 8. Checklist finale

- [ ] Backup pip freeze e PATH (Passo 0)
- [ ] Long paths abilitati + riavvio (Passo 1)
- [ ] PATH utente senza duplicati (Passo 2)
- [ ] `uv` installato e `uv python install 3.13` (Passo 3)
- [ ] `.venv` + `pyproject.toml` + `.gitignore` in `11_potfolio` (Passo 4)
- [ ] Interprete/kernel `.venv` selezionato in VS Code (Passo 4)
- [ ] Tool globali via `uv tool` (Passo 5)
- [ ] Ambiente globale ripulito, cache pip svuotata (Passo 6)
- [ ] `KAGGLEHUB_CACHE` spostata (Passo 7)
- [ ] fnm nel profilo, variabile VBOX rimossa, file `.old` eliminato (Passo 9)

---

## Appendice A — Pacchetti installati (ambiente globale, Python 3.13.14 Store)

```
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.13.0
appdirs==1.4.4
argon2-cffi==25.1.0
argon2-cffi-bindings==26.1.0
arrow==1.4.0
astor==0.8.1
asttokens==3.0.2
async-lru==2.3.0
attrs==26.1.0
babel==2.18.0
beautifulsoup4==4.15.0
bleach==6.4.0
blis==1.3.3
catalogue==2.0.10
certifi==2025.6.15
cffi==2.0.0
charset-normalizer==3.4.2
click==8.3.3
cloudpathlib==0.24.0
colorama==0.4.6
comm==0.2.3
confection==1.3.3
contourpy==1.3.2
cryptography==46.0.3
cycler==0.12.1
cymem==2.0.13
debugpy==1.8.22
defusedxml==0.7.1
Deprecated==1.3.1
deprecation==2.1.0
et_xmlfile==2.0.0
executing==2.2.1
fastapi==0.136.3
fastjsonschema==2.22.2
filelock==3.25.2
fonttools==4.58.5
fqdn==1.5.1
fsspec==2026.3.0
ftfy==6.3.1
glmocr==0.1.5
h11==0.16.0
httpcore==1.0.9
httptools==0.8.0
httpx==0.28.1
idna==3.10
ImageIO==2.37.3
img2pdf==0.6.3
ipykernel==7.3.0
ipython==9.17.1
ipython_pygments_lexers==1.1.1
ipywidgets==8.1.9
isoduration==20.11.0
it_core_news_lg==3.8.0
jedi==0.20.0
Jinja2==3.1.6
json5==0.15.0
jsonpointer==3.1.1
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
jupyter_builder==1.2.3
jupyter_client==8.10.0
jupyter-console==6.6.3
jupyter_core==5.9.1
jupyter-events==0.12.1
jupyter-lsp==2.3.1
jupyter_server==2.21.1
jupyter_server_terminals==0.5.4
jupyterlab_pygments==0.3.0
jupyterlab_server==2.28.1
jupyterlab_widgets==3.0.17
kagglehub==1.0.2
kagglesdk==0.1.37
kiwisolver==1.4.8
langcodes==3.5.1
lark==1.3.1
llvmlite==0.47.0
locate==1.1.1
lxml==6.0.2
markdown-it-py==4.0.0
MarkupSafe==3.0.3
matplotlib==3.10.3
matplotlib-inline==0.2.2
mdurl==0.1.2
mistune==3.3.4
more-itertools==11.0.2
mpmath==1.3.0
msgpack==1.1.2
murmurhash==1.0.15
narwhals==2.26.0
nbclient==0.11.0
nbconvert==7.17.1
nbformat==5.11.1
nest-asyncio2==1.7.3
networkx==3.6.1
notebook_shim==0.2.4
numba==0.65.0
numpy==2.3.1
ocrmypdf==16.11.1
openai-whisper==20250625
openpyxl==3.1.5
packaging==25.0
pandas==2.3.3
pandasgui==0.2.15
pandocfilters==1.5.1
parso==0.8.7
pdfminer.six==20250506
pi_heif==1.1.1
pikepdf==10.0.0
pillow==12.2.0
pip==26.2.1
platformdirs==4.11.12
plotly==7.1.0
pluggy==1.6.0
portalocker==3.2.0
preshed==3.0.13
prometheus_client==0.26.0
prompt_toolkit==3.0.53
protobuf==7.36.2
psutil==7.2.2
pure_eval==0.2.4
pyarrow==25.0.1
pycparser==2.23
pydantic==2.13.4
pydantic_core==2.46.4
Pygments==2.19.2
PyMuPDF==1.27.2.3
pynput==1.8.2
pyparsing==3.2.3
PyQt5==5.15.11
PyQt5-Qt5==5.15.2
PyQt5_sip==12.19.0
PyQtWebEngine==5.15.7
PyQtWebEngine-Qt5==5.15.2
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
python-json-logger==4.2.0
python-multipart==0.0.32
pytz==2025.2
pywin32==311
pywinpty==3.0.5
PyYAML==6.0.3
pyzmq==27.2.0
qtstylish==0.1.5
referencing==0.37.0
regex==2026.4.4
requests==2.32.4
rfc3339-validator==0.1.4
rfc3986-validator==0.1.1
rfc3987-syntax==1.1.0
rich==14.2.0
rpds-py==2026.6.3
scipy==1.17.1
Send2Trash==2.1.0
setuptools==81.0.0
shellingham==1.5.4
six==1.17.0
smart_open==7.6.1
soupsieve==2.10
spacy==3.8.14
spacy-legacy==3.0.12
spacy-loggers==1.0.5
srsly==2.5.3
stack-data==0.6.3
starlette==1.2.1
sympy==1.14.0
tabulate==0.10.0
terminado==0.18.1
thinc==8.3.13
tiktoken==0.12.0
tinycss2==1.5.1
torch==2.11.0
tornado==6.5.10
tqdm==4.67.3
traitlets==5.16.1
typer==0.25.1
typing_extensions==4.15.0
typing-inspection==0.4.2
tzdata==2025.2
uri-template==1.3.0
urllib3==2.5.0
uvicorn==0.49.0
wasabi==1.1.3
watchfiles==1.2.0
wcwidth==0.7.0
weasel==1.0.0
webcolors==25.10.0
webencodings==0.6.1
websocket-client==1.9.2
websockets==16.0
widgetsnbextension==4.0.16
wordcloud==1.9.6
wordfreq==3.1.1
wrapt==2.0.0
```

## Appendice B — Pacchetti obsoleti (67)

| Pacchetto | Installato | Ultima | Attenzione |
|---|---|---|---|
| annotated-doc | 0.0.4 | 0.0.5 | |
| annotated-types | 0.7.0 | 0.8.0 | |
| anyio | 4.13.0 | 4.15.1 | |
| certifi | 2025.6.15 | 2026.7.22 | ⚠️ certificati SSL |
| cffi | 2.0.0 | 2.1.1 | |
| charset-normalizer | 3.4.2 | 3.5.1 | |
| click | 8.3.3 | 8.5.0 | |
| cloudpathlib | 0.24.0 | 0.25.0 | |
| contourpy | 1.3.2 | 1.4.0 | |
| cryptography | 46.0.3 | 50.0.1 | ⚠️ sicurezza, major |
| fastapi | 0.136.3 | 0.141.1 | |
| filelock | 3.25.2 | 4.0.3 | major |
| fonttools | 4.58.5 | 4.66.0 | |
| fsspec | 2026.3.0 | 2026.9.0 | |
| idna | 3.10 | 3.20 | |
| ImageIO | 2.37.3 | 2.37.4 | |
| kiwisolver | 1.4.8 | 1.5.1 | |
| llvmlite | 0.47.0 | 0.49.0 | legato a numba |
| lxml | 6.0.2 | 6.1.3 | |
| markdown-it-py | 4.0.0 | 4.2.0 | |
| matplotlib | 3.10.3 | 3.11.2 | |
| more-itertools | 11.0.2 | 11.1.0 | |
| mpmath | 1.3.0 | 1.4.1 | |
| msgpack | 1.1.2 | 1.2.2 | |
| networkx | 3.6.1 | 3.7 | |
| numba | 0.65.0 | 0.67.0 | |
| numpy | 2.3.1 | 2.5.3 | ⚠️ vincolato da numba/whisper |
| ocrmypdf | 16.11.1 | 17.12.1 | major |
| packaging | 25.0 | 26.3 | |
| pandas | 2.3.3 | 3.0.6 | ⚠️ major: cambi incompatibili (Copy-on-Write, stringhe) |
| pdfminer.six | 20250506 | 20260107 | |
| pi_heif | 1.1.1 | 1.4.0 | |
| pikepdf | 10.0.0 | 10.13.0.post1 | |
| pillow | 12.2.0 | 12.3.0 | |
| platformdirs | 4.11.12 | 4.11.13 | |
| portalocker | 3.2.0 | 4.4.0 | major |
| pycparser | 2.23 | 3.0 | major |
| pydantic | 2.13.4 | 2.13.5 | |
| pydantic_core | 2.46.4 | 2.49.0 | legato a pydantic |
| Pygments | 2.19.2 | 2.21.0 | |
| PyMuPDF | 1.27.2.3 | 1.28.2 | |
| pyparsing | 3.2.3 | 3.3.3 | |
| python-dotenv | 1.2.2 | 1.2.3 | |
| pytz | 2025.2 | 2026.4 | |
| pywin32 | 311 | 312 | |
| regex | 2026.4.4 | 2026.9.10 | |
| requests | 2.32.4 | 2.34.2 | |
| rich | 14.2.0 | 15.0.0 | major |
| scipy | 1.17.1 | 1.18.1 | |
| setuptools | 81.0.0 | 84.0.0 | |
| smart_open | 7.6.1 | 8.0.1 | major |
| spacy | 3.8.14 | 3.8.16 | |
| starlette | 1.2.1 | 1.7.0 | legato a fastapi |
| thinc | 8.3.13 | 9.1.1 | ⚠️ non aggiornare: spacy 3.8 richiede thinc 8.x |
| tiktoken | 0.12.0 | 0.14.0 | |
| torch | 2.11.0 | 2.14.0 | pesante (~200 MB+) |
| tqdm | 4.67.3 | 4.70.1 | |
| typer | 0.25.1 | 0.27.2 | |
| typing_extensions | 4.15.0 | 4.16.0 | |
| typing-inspection | 0.4.2 | 0.4.4 | |
| tzdata | 2025.2 | 2026.4 | |
| urllib3 | 2.5.0 | 2.8.0 | ⚠️ sicurezza |
| uvicorn | 0.49.0 | 0.54.0 | |
| watchfiles | 1.2.0 | 1.3.0 | |
| wcwidth | 0.7.0 | 0.9.1 | |
| websockets | 16.0 | 17.1 | major |
| wrapt | 2.0.0 | 2.4.1 | |
