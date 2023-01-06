from cx_Freeze import setup, Executable
import os

base = os.path.abspath(__file__).replace("/setup.py", "").replace("__main__", "").replace("\setup.py", "")
req_path = os.path.join(base, "requirements.txt")
handler_path = os.path.join(base, "backuphandler.py")

with open(req_path, 'r') as f:
    install_requires = f.read().splitlines()

setup(
    name="Rapit CLI Application",
    version="0.1",
    description="A Command-line Application that interacts with the Rapit API to upload your messages, calls and calendar events.",
    author="Jan de Wit",
    author_email="jeddewit@gmail.com",
    install_requires=install_requires,
    executables=[Executable(handler_path, target_name='win64')], # python setup.py build
)