from subprocess import call

# 更新所有的jar包
if __name__ == '__main__':
    # 查看其版本
    print('查看其版本')
    call('node -v', shell=True)
    call('npm -v', shell=True)

    # 更新 npm
    print('更新 npm')
    call('npm install -g npm', shell=True)

    # 更新node版本
    # 先清除npm缓存
    # print('先清除npm缓存')
    # call('npm cache clean --force', shell=True)
    # 安装n模块
    # print('安装n模块')
    # call('npm install -g n', shell=True)
    # 升级node.js到最新稳定版
    # print('升级node.js到最新稳定版')
    # call('n stable', shell=True)
    # call('ncu', shell=True)
    # call('ncu -u', shell=True)
    # 更新所有包
    print('更新所有包')
    call('npm update', shell=True)
