#!/usr/bin/env bash
# Visual check: starts a project's API + web server, screenshots the given routes with headless Chrome, stops both.
# Usage: bash tools/shoot.sh 02-ai-automation OUT_DIR "" app app/chatbot ...
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
P="$1"; OUT="$2"; shift 2
N=$((10#${P:0:2}))
API=$((8000 + N)); WEB=$((5170 + N))
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
mkdir -p "$OUT"

(cd "$ROOT/$P/backend" && exec "$ROOT/.venv/Scripts/python.exe" -m uvicorn main:app --port $API >"$OUT/api$N.log" 2>&1) &
API_PID=$!
(cd "$ROOT/$P/frontend" && exec npx vite --port $WEB --strictPort >"$OUT/web$N.log" 2>&1) &
WEB_PID=$!
for i in $(seq 1 30); do curl -sf "http://localhost:$WEB/api/health" >/dev/null && break; sleep 1; done

for route in "$@"; do
  name="p${N}-$(echo "${route:-home}" | tr '/' '_')"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1000 --virtual-time-budget=7000 \
    --screenshot="$OUT/$name.png" "http://localhost:$WEB/$route" 2>/dev/null
done

kill $API_PID $WEB_PID 2>/dev/null
# free ports in case child processes survived
for port in $API $WEB; do
  pid=$(netstat -ano | grep "LISTENING" | grep ":$port " | awk '{print $5}' | head -1)
  [ -n "$pid" ] && taskkill //F //PID "$pid" >/dev/null 2>&1
done
ls "$OUT" | grep "^p${N}-"
