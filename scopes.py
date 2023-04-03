from enum import Enum

class TrackingScope(Enum):
    '''Enum containing tracking scopes'''
    # Function returning *
    ALL = []
    ENV = 'env'
    OS_NAME = 'os_name'
    OS_VERSION = 'os_version'
    OS_ARCH = 'os_arch'
    OS_RELEASE = 'os_release'
    OS_DIST = 'os_dist'
    OS_DIST_VERSION = 'os_dist_version'
    USERNAME = 'username'
    HOSTNAME = 'hostname'
    IP = 'ip'
    MAC = 'mac'
    CPU = 'cpu'
    GPU = 'gpu'
    GPU_COUNT = 'gpu_count'
    RAM = 'ram'
    RAM_USED = 'ram_used'
    DISK_USED = 'disk_used'
    DISK_MAX = 'disk_max'