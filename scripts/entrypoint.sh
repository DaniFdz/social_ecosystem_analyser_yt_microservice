#!/usr/bin/env bash

set -e

/root/.local/bin/poetry run python3 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser > /root/.logs/yt_service.log 2> /root/.logs/yt_service_error.log
/root/.local/bin/poetry run python3 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser_examination > /root/.logs/vt_service.log 2> /root/.logs/vt_service_error.log
