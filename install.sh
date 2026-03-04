#!/bin/bash
# ClipFusion Viral Pro — Instalação (Debian pós-formatação)
set -e
GRN='\033[0;32m'; YEL='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()  { echo -e "${GRN}[✓]${NC} $1"; }
warn(){ echo -e "${YEL}[!]${NC} $1"; }

echo ""
echo "╔═════════════════════════════════════════╗"
echo "║    ClipFusion Viral Pro — Instalação   ║"
echo "╚═════════════════════════════════════════╝"
echo ""

sudo apt install -y python3 python3-pip python3-venv python3-tk \
    ffmpeg git curl wget 2>/dev/null || true
ok "Dependências do sistema"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip --quiet
pip install openai-whisper numpy --quiet
ok "Pacotes Python"

command -v ffmpeg &>/dev/null && ok "FFmpeg: $(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')" || warn "FFmpeg não encontrado"
python3 -c "import whisper" 2>/dev/null && ok "Whisper OK" || warn "Whisper não instalado"

# VA-API
if command -v vainfo &>/dev/null && vainfo 2>&1 | grep -q "iHD\|i965"; then
    ok "VA-API Intel disponível"
else
    warn "VA-API não detectado — render usará CPU"
fi

mkdir -p ~/.clipfusion output/prompts output/scripts output/reports config/profiles
touch core/__init__.py gui/__init__.py viral_engine/__init__ 2>/dev/null || true

cat > run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py
EOF
chmod +x run.sh
ok "run.sh criado"

echo ""
echo "╔═════════════════════════════════════════╗"
echo "║  ✅  PRONTO — para iniciar:            ║"
echo "║     ./run.sh                           ║"
echo "╚═════════════════════════════════════════╝"
echo ""
