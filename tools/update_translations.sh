#!/usr/bin/env bash
# ==============================================================================
# Script de Atualização e Compilação de Traduções (GNU Gettext)
# Logi Options+ GTK
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT_DIR"

echo "🌐 1. Extraindo strings do código-fonte para po/logi-options-gtk.pot..."
mkdir -p po
xgettext --from-code=UTF-8 \
         --language=Python \
         --keyword=_ \
         --keyword=ngettext:1,2 \
         --output=po/logi-options-gtk.pot \
         main.py \
         app/*.py \
         app/views/*.py \
         app/widgets/*.py \
         app/backend/*.py

echo "🔄 2. Atualizando arquivos .po existentes via msgmerge..."
for pofile in po/*.po; do
    if [ -f "$pofile" ]; then
        lang=$(basename "$pofile" .po)
        echo "   -> Atualizando $pofile..."
        msgmerge --update --backup=none "$pofile" po/logi-options-gtk.pot
    fi
done

echo "📦 3. Compilando catálogos binários (.mo)..."
for pofile in po/*.po; do
    if [ -f "$pofile" ]; then
        lang=$(basename "$pofile" .po)
        outdir="app/locale/$lang/LC_MESSAGES"
        mkdir -p "$outdir"
        echo "   -> Compilando $pofile para $outdir/logi-options-gtk.mo..."
        msgfmt -o "$outdir/logi-options-gtk.mo" "$pofile"
    fi
done

echo "✅ Traduções atualizadas e compiladas com sucesso!"
