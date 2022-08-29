# Idle Notifier

This script notifies the user using SimplePush when the computer is idle.

## Installation
First install the python package:
```bash
git clone https://github.com/yewzijian/idle_notifier.git
pip install --upgrade -e ./idle_notifier
```

Then run the setup tool:
```bash
idle_notifier_setup
```
Input the machine name and api key when prompted. Then enable the system service with:
```bash
sudo systemctl enable idle_notifier
```


## Uninstall
Run the uninstall tool:
```bash
idle_notifier_remove
```
Then optionally remove the python package
```bash
pip uninstall idle_notifier
```