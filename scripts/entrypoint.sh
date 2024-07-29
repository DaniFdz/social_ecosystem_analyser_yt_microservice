#!/usr/bin/env bash

set -e

if [ ! -d "$HOME/.logs" ]; then
    mkdir $HOME/.logs
fi

$HOME/.local/bin/poetry run python3 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser 2> $HOME/.logs/yt_service_error.log | tee $HOME/.logs/yt_service.log
$HOME/.local/bin/poetry run python3 -m src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser_examination 2> $HOME/.logs/vt_service_error.log | tee $HOME/.logs/vt_service.log
