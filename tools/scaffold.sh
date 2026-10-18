#!/usr/bin/env bash
# Copies the shared MVC core from project 01 into a new project folder.
# Usage: bash tools/scaffold.sh 02-ai-automation
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/01-business-management-saas"
DST="$ROOT/$1"

mkdir -p "$DST/backend/app/core" "$DST/backend/app/modules" \
         "$DST/frontend/src/core" "$DST/frontend/src/components/ui" "$DST/frontend/src/layouts" "$DST/frontend/src/router" "$DST/frontend/src/modules"

# Backend core (repository + helpers)
cp "$SRC/backend/app/__init__.py" "$DST/backend/app/"
cp "$SRC/backend/app/core/"*.py "$DST/backend/app/core/"
cp "$SRC/backend/requirements.txt" "$DST/backend/"

# Frontend core, UI kit, layout, router, entry
cp "$SRC/frontend/src/core/"*.js "$DST/frontend/src/core/"
cp "$SRC/frontend/src/components/ui/"*.vue "$DST/frontend/src/components/ui/"
cp "$SRC/frontend/src/layouts/AppLayout.vue" "$DST/frontend/src/layouts/"
cp "$SRC/frontend/src/router/index.js" "$DST/frontend/src/router/"
cp "$SRC/frontend/src/App.vue" "$SRC/frontend/src/main.js" "$DST/frontend/src/"
echo "Scaffolded $1"
