import json
import os.path
import shutil
import sys
import subprocess


def setup_wrapper(mode='install'):

    if not os.path.exists('/etc/systemd/system'):
        print('Error: Unable to find /etc/systemd/system folder. This tool is only for Linux systems. Terminating...')
        exit(-1)

    if os.geteuid() != 0:
        python_path = sys.executable
        result = input('This script requires sudo rights to modify /etc/systemd. '
                       'Alternatively, you can run without sudo rights and follow the '
                       'displayed commands to modify it yourself. '
                       'Run with sudo [y/n]: ')
        while result not in ['y', 'n']:
            result = input('Invalid response. Run setup script with sudo? [y/n] ')
        if result == 'y':
            subprocess.call(['sudo', python_path, *sys.argv])
            sys.exit()

    if mode == 'install':
        run_setup(has_sudo=os.geteuid() == 0)
    elif mode == 'uninstall':
        run_uninstall(has_sudo=os.geteuid() == 0)


def run_setup(has_sudo):
    print('Setting up idle notifier...')

    install_path = os.path.dirname(os.path.realpath(__file__))
    python_path = sys.executable
    script_path = os.path.join(install_path, 'main.py')
    print(f'Will use the following python interpreter: {python_path}.')

    api_key = input('Please enter SimplePush API key: ')
    device_name = input('Please enter device name: ')
    with open(os.path.join(install_path, '_config.json')) as fid:
        cfg = json.load(fid)
        cfg['key'] = api_key
        cfg['Computer']['Device name'] = device_name
    with open(os.path.join(install_path, 'config.json'), 'w') as fid:
        json.dump(cfg, fid, indent=4)

    with open(os.path.join(install_path, '_idle_notifier.service'), 'r') as fid:
        service_str = fid.read()
    service_str = service_str.replace('{PYTHON_PATH}', python_path)
    service_str = service_str.replace('{SCRIPT_PATH}', script_path)

    dst_path = os.path.join(install_path, 'idle_notifier.service')
    with open(dst_path, 'w') as fid:
        fid.write(service_str)

    systemd_path = os.path.join('/etc/systemd/system/', 'idle_notifier.service')

    if has_sudo:
        os.chmod(dst_path, 0o777)
        os.symlink(dst_path, systemd_path)
        subprocess.call(['systemctl', 'enable', 'idle_notifier'])
        subprocess.call(['systemctl', 'start', 'idle_notifier'])
        print(f'Installation complete.')
    else:
        print('Config file written. Note that installation is not complete. Run the following commands '
              'to write to the systemd folder to start the service and enable startup on bot\n')
        print(f"  sudo ln -s {dst_path} {systemd_path}")
        print( "  sudo systemctl enable idle_notifier")
        print( "  sudo systemctl start idle_notifier")


def run_uninstall(has_sudo):
    systemd_path = '/etc/systemd/system/idle_notifier.service'
    if os.path.exists(systemd_path):
        if has_sudo:
            subprocess.call(['systemctl', 'stop', 'idle_notifier'])
            subprocess.call(['systemctl', 'disable', 'idle_notifier'])
            print('Uninstalled idle_notifier')

        else:
            print('Follow the following instructions to uninstall\n')
            print('sudo systemctl stop idle_notifier')
            print('sudo systemctl disable idle_notifier')
    else:
        print('idle_notifier was not installed. Not proceeding with uninstallation.')


def idle_notifier_setup():
    setup_wrapper('install')

def idle_notifier_remove():
    setup_wrapper('uninstall')