"""
@author:cmcc
@file: leidian.py
@time: 2024/4/10 21:43
"""
import os
import time
from leidianhelper.utils.leidian_util import LeidianUtil
from leidianhelper.utils.adb_util import AdbUtil


class LeiDian:

    def __init__(self, name):
        self.leidian_helper = LeidianUtil
        self.name = name
        self.serial = None
        self.adb = None

    def wait_running(self):
        """
        等待模拟器启动，进入android状态
        :return:
        """
        btime = time.time()
        while not self.is_running():
            if time.time() - btime > 60:
                raise RuntimeError("等待模拟器启动超时")
            time.sleep(5)
        self.serial = self.get_serial()
        self.adb = AdbUtil(self.serial)

    def get_serial(self):
        """
        获取模拟器adb序列号
        :return:
        """
        ro_serial = LeidianUtil.get_ro_serial(self.name)
        for serial, status in self.get_adb_serial().items():
            if status == "device":
                tmp_serial = AdbUtil(serial).cmd("shell", "getprop ro.serialno").communicate()[0].decode("utf-8").strip()
                if tmp_serial == ro_serial:
                    return serial

    @classmethod
    def get_adb_serial(cls):
        return LeidianUtil.adb_serial()

    @classmethod
    def get_device_list(cls):
        """
        模拟器列表
        :return:
        """
        return LeidianUtil.get_device_list()

    def is_running(self):
        return LeidianUtil.is_running(self.name)

    def install_app(self, file_path):
        if os.path.isfile(file_path):
            LeidianUtil.install_app(self.name, file_path)
        elif os.path.isdir(file_path):
            for item in os.listdir(file_path):
                LeidianUtil.install_app(self.name, os.path.join(file_path, item))

    def launch(self):
        LeidianUtil.launch(self.name)

    def uninstall_app(self, package_name):
        LeidianUtil.uninstall_app(self.name, package_name)

    def run_app(self, package_name):
        LeidianUtil.run_app(self.name, package_name)

    def stop_app(self, package_name):
        LeidianUtil.stop_app(self.name, package_name)

    def reboot(self):
        LeidianUtil.reboot(self.name)

    def quit(self):
        """
        退出模拟器
        :return:
        """
        LeidianUtil.quit(self.name)

    def modify(self, **kwargs):
        """
        lsconsole.exe modify --index 0 --resolution 600,360,160 --cpu 1 --memory 1024 --imei auto
        注：调用modify需要在模拟器启动前，不然可能不生效
        :param kwargs:
        :return:
        """
        LeidianUtil.modify(self.name, **kwargs)

    def create(self):
        """
        新增模拟器
        :return:
        """
        LeidianUtil.create(self.name)

    def copy(self, _from):
        """
        复制模拟器
        注意：from参数既可以是名字也可以是索引，判断规则为如果全数字就认为是索引，否则是名字
        :param _from:
        :return:
        """
        LeidianUtil.copy(self.name, _from)

    def remove(self):
        """
        删除模拟器
        :return:
        """
        LeidianUtil.remove(self.name)

    def backup(self, file_path):
        """
        backup <--name mnq_name | --index mnq_idx> --file
        :param file_path:
        :return:
        """
        LeidianUtil.backup(self.name, file_path)

    def restore(self, file_path):
        """
        restore <--name mnq_name | --index mnq_idx> --file
        :param file_path:
        :return:
        """
        LeidianUtil.restore(self.name, file_path)

    def rename(self, title):
        """
        修改名字
        :param title:
        :return:
        """
        LeidianUtil.rename(self.name, title)


if __name__ == '__main__':
    a = LeiDian(0).get_device_list()
    print(a)
    # a.wait_running()
    # print(a.serial, a.name)