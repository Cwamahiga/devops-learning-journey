#!/bin/bash
# Setup script for DevOps Gamification System

echo ""
echo "🎮 DevOps Gamification System - Setup"
echo "====================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check Python version
echo "🐍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x "$SCRIPT_DIR/xp"
chmod +x "$SCRIPT_DIR/xp_tracker_v2.py"
chmod +x "$SCRIPT_DIR/quick_log.py"
chmod +x "$SCRIPT_DIR/progress_updater.py"
chmod +x "$SCRIPT_DIR/git_integration.py"
echo "✅ Scripts are now executable"
echo ""

# Create symlink for easy access
echo "🔗 Creating command alias..."
if [ -d "$HOME/.local/bin" ]; then
    BIN_DIR="$HOME/.local/bin"
elif [ -d "$HOME/bin" ]; then
    BIN_DIR="$HOME/bin"
else
    mkdir -p "$HOME/.local/bin"
    BIN_DIR="$HOME/.local/bin"
fi

# Create symlink
ln -sf "$SCRIPT_DIR/xp" "$BIN_DIR/xp" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Command 'xp' installed to $BIN_DIR"
    echo ""
    echo "⚠️  Make sure $BIN_DIR is in your PATH!"
    echo "   Add this to your ~/.bashrc or ~/.zshrc:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
else
    echo "⚠️  Could not create symlink. You can still use ./xp"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Quick Start:"
echo "   ./xp help          # Show all commands"
echo "   ./xp log           # Quick daily log"
echo "   ./xp status        # View your stats"
echo ""
echo "Or if symlink worked:"
echo "   xp help"
echo "   xp log"
echo "   xp status"
echo ""
echo "🎮 Start earning XP! Your journey begins now! 🚀"
echo ""
