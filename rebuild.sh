#!/bin/bash
set -e

echo "🔄 Cleaning all build artifacts..."
find . -type f \( \
  -name "*.o" \
  -o -name "*.a" \
  -o -name "*.moc" \
  -o -name "moc_*.cpp" \
  -o -name "Makefile" \
  -o -name ".qmake.stash" \
  -o -name "server" \
  -o -name "client" \
  -o -name "tests" \
\) -delete

echo "⚙️ Regenerating build system..."
qmake6 ClientServerSystem.pro

echo "🔨 Building project..."
make

echo "✅ Rebuild complete!"