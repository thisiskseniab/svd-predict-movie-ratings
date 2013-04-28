#!/bin/bash
#

PROJECT_NAME='Project'

echo "running model in interactive mode"
python -i model.py

echo "creating sqlite db"
engine = create_engine("sqlite:///ratings.db", echo=True)
Base.metadata.create_all(engine)


echo "planting a seed"
python seed.py
echo "running tipsy"
python tipsy.py