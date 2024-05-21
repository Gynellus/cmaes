import subprocess
import json

def run_java_game(level_path, timer=20, mario_state=0, visuals=False):
    java_executable = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
    argfile_path = "/home/guido/coding/LVEPCGDRL/Mario-AI-Framework/src/java.args"
    command = [java_executable, f"@{argfile_path}", level_path, str(timer), str(mario_state), str(visuals).lower()]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception("Java program failed with error: " + result.stderr)

    lines = result.stdout.strip().split('\n')
    json_output = lines[-1]  # The JSON output is expected to be the last line
    return json.loads(json_output)