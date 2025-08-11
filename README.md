### Batch IP Resolver

Resolve IP addresses for a list of domains in bulk and save results to a timestamped TSV file.

### Features
- **Batch input**: read domains from `input.txt` (one per line)
- **Deduplicates**: removes duplicate domains while preserving order
- **Robust resolution**: strips http/https prefixes; handles errors gracefully
- **Timestamped output**: writes to `results_YYYYMMDD.txt` (tab-separated with header)

### Requirements
- **Python 3.11+** (project targets 3.11 by default)  
  No external dependencies required.

### Quickstart (CLI)
1) Clone the repo
2) (Optional) Create and activate a virtual environment
3) Create an `input.txt` (or copy `input.sample.txt` to `input.txt`)
4) Run the script

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
copy input.sample.txt input.txt
python ip_resolver.py
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
cp input.sample.txt input.txt
python ip_resolver.py
```

Output will be saved as a file like `results_20250528.txt` in the project root.

### Web UI
You can also use a minimal web interface.

Start the app:

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser. Paste domains or upload a `.txt` file, then click Resolve. You can also download results as a TSV file.

### Input format
- One domain per line
- You can include `http://` or `https://` prefixes; they will be stripped automatically

Example (`input.sample.txt`):

```
example.com
openai.com
python.org
```

### License
This project is licensed under the MIT License. See `LICENSE` for details.


