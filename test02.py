from subprocess import call

from pip._internal.utils.misc import get_installed_distributions

# 更新所有的jar包
if __name__ == '__main__':
    # call('python -m pip install --upgrade pip', shell=True)
    # 升级所有依赖包含如下两个命令
    for dist in get_installed_distributions():
        if dist.project_name != 'pip':
            call('pip install --upgrade ' + dist.project_name + ' --user --use-feature=2020-resolver', shell=True)

    # pip install pip-review --user  # 先安装pip-review函数
    # pip-review --local --interactive  # 成功升级所有的依赖包
    # call('pip install pip-review --user', shell=True)
    # call('pip-review --local --interactive --user', shell=True)
