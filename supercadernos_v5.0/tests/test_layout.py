import os, json

def test_repo_layout():
    assert os.path.exists("src/supercadernos/cli.py")
    assert os.path.exists("prompts/extractor.jinja.md")
    assert os.path.exists("config.yaml")
