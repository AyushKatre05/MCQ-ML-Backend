#!/bin/bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
# Install maturin and Rust
pip install maturin
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export MATURIN_BUILD_DIR=/tmp
