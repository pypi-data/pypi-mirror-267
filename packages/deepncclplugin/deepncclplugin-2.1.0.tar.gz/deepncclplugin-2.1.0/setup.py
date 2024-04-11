#
# Copyright (C) Alibaba Cloud Ltd. 2021-2024.  ALL RIGHTS RESERVED.
#

import os
import subprocess
from setuptools import setup
from setuptools.command.install import install

version = "2.1.0"
package_name = "deepncclplugin"
package_version = "1.1.0" # TODO: sync version
_root_path_deepgpu = "https://mirrors.aliyun.com/deepgpu/"
_root_path_deepncclplugin = f"{_root_path_deepgpu}/deepncclplugin/aiacc-nccl-plugin-{package_version}" # TODO: sync filename
_temp_path = f"{os.environ['HOME']}/.deepncclplugin/"
_temp_log = f"{_temp_path}/log"

def get_os_name():
    # return 'debian'
    cmd = ["pip3", "install", "--no-deps", "--quiet", "distro"]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        os.system(f'echo "Install distro failed with {res.stderr}" >> {_temp_log}')
    import distro
    return distro.id()

class post_install(install):
    def run(self):
        install.run(self)

        # create if not existed
        dst_path = "/usr/local/lib"
        if not os.path.exists(dst_path): os.system(f'mkdir -p {dst_path}')
        if not os.path.exists(f'{_temp_path}'): os.system(f'mkdir -p {_temp_path}')

        # backup if already existed, and backup once
        if os.path.isfile(f'{dst_path}/libnccl-net.so.0.0.0') and not os.path.isfile(f'{dst_path}/libnccl-net.bak'):
            os.system(f'cp {dst_path}/libnccl-net.so.0.0.0 {dst_path}/libnccl-net.bak')

        # download and install rpm/deb by os type
        if os.path.isfile(f'{_temp_log}'):
            os.system(f'echo "Install ..." > {_temp_log}')
        os_name = get_os_name()
        if os_name.lower() == "centos":
            cmd = ["wget", "--quiet", "-P", _temp_path, f"{_root_path_deepncclplugin}.rpm"]
            subprocess.run(cmd)
            cmd = ["rpm", "-i", f"{_temp_path}/aiacc-nccl-plugin-{package_version}.rpm"]
            res = subprocess.run(cmd)
            if res.returncode != 0:
                os.system(f'echo "Install failed with {res.stderr}" >> {_temp_log}')
        elif os_name.lower() == "ubuntu":
            cmd = ["wget", "--quiet", "-P", _temp_path, f"{_root_path_deepncclplugin}.deb"]
            subprocess.run(cmd)
            cmd = ["dpkg", "-i", f"{_temp_path}/aiacc-nccl-plugin-{package_version}.deb"]
            res = subprocess.run(cmd)
            if res.returncode != 0:
                os.system(f'echo "Install failed with {res.stderr}" >> {_temp_log}')
        else:
            os.system(f'echo "Not suported OS!" >> {_temp_log}')


setup(
    name=package_name,
    version=f"{version}",
    description=("DEEP-NCCL-PLUGIN is a plugin of AI-Accelerator communication framework for NVIDIA-NCCL. "\
                 "It has been optimized to achieve high bandwidth on aliyun machines using InfiniBand Verbs, eRDMA or TCP/IP sockets."),
    author="Alibaba Cloud",
    license="Copyright (C) Alibaba Group Holding Limited",
    keywords="Distributed, Deep Learning, Communication, NCCL, DEEPGPU",
    url="https://help.aliyun.com/document_detail/462422.html?spm=a2c4g.462031.0.0.c5f96b4drcx52F",
    cmdclass={
      'install': post_install
    },
    python_requires=">=3.8",
)
