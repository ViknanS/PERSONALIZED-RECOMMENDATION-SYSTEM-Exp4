#!/bin/bash
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:/Applications/Ollama.app/Contents/Resources:$PATH"
export PYTHONUNBUFFERED=1
source "$HOME/.ecomgpt-venv/bin/activate"
mkdir -p screenshots outputs models
printf "\e[8;46;100t"
sleep 1

clear
echo "Checking environment ..."
ollama --version
curl -s -m 5 http://localhost:11434/api/version >/dev/null || {
  echo "Starting Ollama ..."; nohup ollama serve >/dev/null 2>&1 & sleep 8; }
curl -s -m 5 http://localhost:11434/api/version >/dev/null && echo "Ollama running." || {
  echo "ERROR: Ollama unreachable."; exit 1; }
ollama list | grep -q "llama3.2" && echo "llama3.2 installed." || {
  echo "ERROR: llama3.2 missing. Run: ollama pull llama3.2"; exit 1; }
python -c "import utils; utils.check_model(); utils.ask('Reply briefly.','hi')" || exit 1
echo "Ready."
sleep 2

exec > >(tee demos.log) 2>&1
shot () { sleep 2; screencapture -x -o "screenshots/$1"; }
PROFILE='Arun\n20\nComputer Science\nArtificial Intelligence, Python\nBeginner\nOnline Courses\nLearn AI\n5\n'

clear
printf '9\n' | python main.py
shot 01_home.png

clear
printf "1\n$PROFILE\n9\n" | python main.py
shot 02_user_profile_input.png

clear
python -c "
import utils, input_module
input_module.display_profile(utils.load_profile())"
shot 03_collected_profile.png

clear
python profile_module.py
shot 04_preference_analysis.png

clear
python prompt_module.py
shot 05_prompt_generation.png

clear
python recommendation_module.py
shot 06_recommendation.png

clear
python ranking_module.py
shot 07_ranking.png

clear
python explanation_module.py
shot 08_explanation.png

clear
printf 'I prefer Artificial Intelligence and do not want Web Development resources.\n' | python feedback_module.py
shot 09_user_feedback.png

clear
python -c "
import utils, recommendation_module
recommendation_module.display(utils.load_result()['items'], 'REFINED RECOMMENDATIONS')"
shot 10_refined_recommendations.png

clear
python intent_module.py
shot 11_intent_detection.png

clear
python save_module.py
shot 12_saved_successfully.png

clear
echo "=== verification ==="
ls -l screenshots/
echo
wc -l outputs/recommendations.txt
head -12 outputs/recommendations.txt
echo
echo "DEMOS4_FINISHED_OK"
