# Idle Notifier

This script notifies the user using SimplePush when the computer is idle. 

Note: This repo is for internal use only. No support will be provided, use at your own risk.

## Pre-requisites

Install [SimplePush](https://simplepush.io) on your phone. [[Android](https://play.google.com/store/apps/details?id=io.simplepush)] [[iOS](https://apps.apple.com/us/app/simplepush-notifications/id1569978086)]

Take note of your API key. 

## Installation

1. First install the python package. Either
   
   * Clone and install in develop mode
     
     ```bash
     git clone https://github.com/yewzijian/idle_notifier.git
     pip install --upgrade -e ./idle_notifier
     ```
   
   * or directly install from this git repository
     
     ```bash
     pip install https+https://github.com/yewzijian/idle_notifier.git
     ```

Then run the setup tool:

```bash
idle_notifier_setup
```

Follow the instructions and enter the machine name and api key when prompted.

## Uninstall

1. Run the uninstall tool:
   
   ```bash
   idle_notifier_remove
   ```

2. Then optionally remove the python package
   
   ```bash
   pip uninstall idle_notifier
   ```

## Additional notes

* By default, the script checks CPU/GPU usage every minute. If it falls below both thresholds of 10% CPU and GPU usage for over 30min, a notification will be sent. Currently there is no functionality to easily configure these parameters, but they can be edited manually in `config.json`.