import subprocess, config


if config.debug() == True:
    subprocess.run(f"venv/bin/uvicorn main:app --reload --port {config.getport()}")

else:
    subprocess.run(f"venv/bin/uvicorn main:app --port {config.getport()}")

