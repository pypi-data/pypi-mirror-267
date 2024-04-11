import os
import subprocess
import logging

logger = logging.getLogger(__name__)


class LeidianUtil:
    LDCONSOLE_CMD = os.path.join(os.getenv("LEIDIAN_DIR", r"D:\leidian\LDPlayer9"), "ldconsole.exe")

    @classmethod
    def get_device_list(cls):
        header = "index,title,top_window_handler,binding_window_handler,is_startup,PID,VBox_PID"
        out = cls.raw_cmd("list2").communicate()[0].decode("gbk")
        return [dict(zip(header.split(","), s.split(","))) for s in out.strip().splitlines() if s.strip()]

    @classmethod
    def raw_cmd(cls, *args):
        """ldconsole command. return the subprocess.Popen object."""
        cmd_line = [cls.LDCONSOLE_CMD] + list(args)
        if os.name != "nt":
            cmd_line = [" ".join(cmd_line)]
        logger.debug(cmd_line)
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @classmethod
    def adb_shell(cls, name_or_index, cmd_line):
        return cls.raw_cmd(*f"adb {cls._format_cmd(name_or_index)} --command".split(" "), "shell " + cmd_line)

    @classmethod
    def adb_serial(cls):
        match = "List of devices attached"
        out = cls.raw_cmd(*f"adb {cls._format_cmd(0)} --command".split(" "), "devices")\
            .communicate()[0].decode("utf-8").strip()
        index = out.find(match)
        return dict([s.split("\t") for s in out[index + len(match):].strip().splitlines() if s.strip()])

    @classmethod
    def get_ro_serial(cls, name_or_index):
        return cls.adb_shell(name_or_index, "getprop ro.serialno").communicate()[0].decode("utf-8").strip()

    @classmethod
    def _format_cmd(cls, name_or_index):
        if isinstance(name_or_index, str):
            cmd = f"--name {name_or_index}"
        else:
            cmd = f"--index {name_or_index}"
        return cmd

    @classmethod
    def quit(cls, name_or_index):
        cls.raw_cmd(f"quit {cls._format_cmd(name_or_index)}").wait()

    @classmethod
    def quit_all(cls):
        cls.raw_cmd("quitall").wait()

    @classmethod
    def launch(cls, name_or_index):
        cls.raw_cmd(f"launch {cls._format_cmd(name_or_index)}").wait()

    @classmethod
    def install_app(cls, name_or_index, file_path):
        cls.raw_cmd(*f"installapp {cls._format_cmd(name_or_index)} --filename {file_path}".split(" ")).wait()

    @classmethod
    def uninstall_app(cls, name_or_index, package_name):
        cls.raw_cmd(*f"uninstallapp  {cls._format_cmd(name_or_index)} --packagename {package_name}".split(" ")).wait()

    @classmethod
    def run_app(cls, name_or_index, package_name):
        cls.raw_cmd(*f"runapp {cls._format_cmd(name_or_index)} --packagename {package_name}".split(" ")).wait()

    @classmethod
    def stop_app(cls, name_or_index, package_name):
        cls.raw_cmd(*f"killapp  {cls._format_cmd(name_or_index)} --packagename {package_name}".split(" ")).wait()

    @classmethod
    def reboot(cls, name_or_index):
        cls.raw_cmd(f"reboot {cls._format_cmd(name_or_index)}").wait()

    @classmethod
    def modify(cls, name_or_index, **kwargs):
        """
        lsconsole.exe modify --index 0 --resolution 600,360,160 --cpu 1 --memory 1024 --imei auto
        注：调用modify需要在模拟器启动前，不然可能不生效
        :param name_or_index:
        :param kwargs:
        :return:
        """
        format_cmd = []
        for key, value in kwargs:
            format_cmd.append(f"--{key} value")
        cls.raw_cmd(f"modify {cls._format_cmd(name_or_index)} {' '.join(format_cmd)}").wait()

    @classmethod
    def create(cls, name):
        """
        新增模拟器
        :param name:
        :return:
        """
        cls.raw_cmd(f"add {name}").wait()

    @classmethod
    def copy(cls, name,  _from):
        """
        复制模拟器
        注意：from参数既可以是名字也可以是索引，判断规则为如果全数字就认为是索引，否则是名字
        :param name:
        :param _from:
        :return:
        """
        cls.raw_cmd(f"copy --name {name} --from {_from}").wait()

    @classmethod
    def remove(cls, name_or_index):
        """
        删除模拟器
        :param name_or_index:
        :return:
        """
        cls.raw_cmd(f"remove {cls._format_cmd(name_or_index)}").wait()

    @classmethod
    def backup(cls, name_or_index, file_path):
        """
        backup <--name mnq_name | --index mnq_idx> --file
        :param file_path:
        :param name_or_index:
        :return:
        """
        cls.raw_cmd(f"backup {cls._format_cmd(name_or_index)} --file {file_path}").wait()

    @classmethod
    def restore(cls, name_or_index, file_path):
        """
        restore <--name mnq_name | --index mnq_idx> --file
        :param file_path:
        :param name_or_index:
        :return:
        """
        cls.raw_cmd(f"remove {cls._format_cmd(name_or_index)} --file {file_path}").wait()

    @classmethod
    def rename(cls, name_or_index, title):
        """
        修改名字
        :param name_or_index:
        :param title:
        :return:
        """
        cls.raw_cmd(f"remove {cls._format_cmd(name_or_index)} --title {title}").wait()

    @classmethod
    def is_running(cls, name_or_index):
        """
        模拟器运行状态，是否进入android
        :param name_or_index:
        :return:
        """
        for device in cls.get_device_list():
            if str(name_or_index) == device["index"] or str(name_or_index) == device["title"]:
                return device["is_startup"] == "1"
        return False

