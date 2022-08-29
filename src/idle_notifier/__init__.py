import json
import os.path
import shutil
import sys
import subprocess


def idle_notifier_setup():
    if True or os.geteuid() == 0:
        run_setup()
    else:
        python_path = sys.executable
        result = input('You need sudo to run this setup script. Run with sudo rights? [y/n]')
        while result not in ['y', 'n']:
            result = input('Invalid response. Run setup script with sudo? [y/n]')
        if result == 'y':
            subprocess.call(['sudo', python_path, *sys.argv])
            sys.exit()
        else:
            print('Terminating...')


def run_setup():
    print('Setting up idle notifier...')

    install_path = os.path.dirname(os.path.realpath(__file__))
    python_path = sys.executable
    script_path = os.path.join(install_path, 'main.py')
    print(f'Will use the following python interpreter: {python_path}.')

    api_key = input('Please enter SimplePush API key:')
    device_name = input('Please enter device name:')
    with open(os.path.join(install_path, '_config.json')) as fid:
        cfg = json.load(fid)
        cfg['key'] = api_key
        cfg['Computer']['Device name'] = device_name
    with open(os.path.join(install_path, 'config.json'), 'w') as fid:
        json.dump(cfg, fid, indent=4)

    with open(os.path.join(install_path, 'idle_notifier.service'), 'r') as fid:
        service_str = fid.read()
    service_str = service_str.replace('{PYTHON_PATH}', python_path)
    service_str = service_str.replace('{SCRIPT_PATH}', script_path)

    dst_path = '/etc/systemd/system/idle_notifier.service'
    with open(dst_path, 'w') as fid:
        fid.write(service_str)
    os.chmod(dst_path, 744)

    print(f'Installation complete. Written service to {dst_path}')
    print("Run 'sudo systemctl enable idle_notifier' to enable service upon boot")


def run_uninstall():
    dst_path = '/etc/systemd/system/idle_notifier.service'
    if os.path.exist(dst_path):
        os.remove(dst_path)
        print(f'Removed {dst_path}')
        subprocess.call(['systemctl', 'disable', 'idle_notifier'])
        print('Uninstalled idle_notifier')
    else:
        print('Not installed')


def idle_notifier_remove():
    if os.geteuid() == 0:
        run_uninstall()
    else:
        python_path = sys.executable
        result = input('You need sudo to run this setup script. Run with sudo rights? [y/n]')
        while result not in ['y', 'n']:
            result = input('Invalid response. Run setup script with sudo? [y/n]')
        if result == 'y':
            subprocess.call(['sudo', python_path, *sys.argv])
            sys.exit()
        else:
            print('Terminating...')