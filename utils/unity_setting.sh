wget https://github.com/Unity-Technologies/ml-agents/archive/release_18.zip
unzip release_18.zip
cd ml-agents-release_18
pip install -e ./ml-agents-envs
pip install -e ./ml-agents
pip install -e ./gym-unity
pip install pyvirtualdisplay
pip install portpicker
