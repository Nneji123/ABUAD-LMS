#!/bin/bash
for i in {1..20}; do
    python init.py
done | tqdm --desc "SETTING UP APPLICATION..." --colour 'green' >/dev/null
echo "APPLICATION SETUP COMPLETE"
