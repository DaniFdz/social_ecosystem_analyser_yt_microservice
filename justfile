install:
    pip install -r requirements.txt

db:
    docker.exe compose up -d

run:
    python3.10 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser