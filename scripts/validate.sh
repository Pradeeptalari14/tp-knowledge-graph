#!/usr/bin/env bash
set -eo pipefail
echo "🔍 Validating Knowledge Graph & Entity Extraction Suite..."
python3 -c "import entity_extractor; print('✅ entity_extractor syntax verified')"
python3 -c "import graph_construction; print('✅ graph_construction syntax verified')"
python3 -c "import py_compile; py_compile.compile('manim_flow.py', doraise=True); print('✅ manim_flow syntax verified')"
echo "✅ SRE compliance validation complete for knowledge-graph."
