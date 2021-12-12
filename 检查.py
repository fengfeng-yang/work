import os,sys
import time

list_all = [1, 3, 5, 7]
def get_staus():
    STATUS = '0'
    for i in list_all:
        if i == 7:
            STATUS = '1'
    # print(STATUS)
    return STATUS

def initial_docker():
    cmd = "yum install docker -y && cp -a daemon.json /etc/docker/daemon.json "
    os.system(cmd)


def initial_yum():
    cmd = "cp yum.repo /etc/yum.repos.d/yum.repo"
    os.system(cmd)


def initial_test(k):
    # cmd = 'echo "环境检测失败后执行初始化"'
    # os.system(cmd)
    cmd = init_cmds[k]
    print(cmd)



def chk_env(*args):
    chk_status = '1'
    cmd = args[0]
    res = os.system(cmd)
    if str(res) == '0':
        # print('状态正常！！')
        chk_status = '0'
        # sys.exit()
    else:
        key = args[2]
        args[1](key)
        chk_status = '0'
    return chk_status


# def chk_py():
#     py_status = '1'
#     cmd1 = '[ `python -V | grep 3 | wc -l` == 1 ] && echo "right"'
#     res = os.system(cmd1)
#     if res == 'right':
#         py_status = '1'
#         print('状态正常！！')
#         sys.exit()
#     else:
#         initial_py()
#     return py_status
#
#
# def chk_docker():
#     pass

init_cmds = {
    'py': 'yum install python3 -y',
    'pip': 'yum install pip3 -y',
    'yum': 'cp yum.repo /etc/yum.repos.d/yum.repo',
    'docker': 'service docker restart'
}

chk_cmds = {
    'py_cmd': 'python -V | grep 3',
    'docker_cmd': 'pd',
    'yum_cmd': 'pd',
    'pip_cmd': ''
}

def main():
    py_cmd = chk_cmds.get('py_cmd')
    py_status = chk_env(py_cmd, initial_test, 'py')

    docker_cmd = chk_cmds.get('docker_cmd')
    docker_status = chk_env(docker_cmd, initial_test, 'docker')

    yum_cmd = chk_cmds.get('yum_cmd')
    yum_status = chk_env(yum_cmd, initial_test, 'yum')

    pip_cmd = chk_cmds.get('pip_cmd')
    pip_status = chk_env(pip_cmd, initial_test, 'pip')

    if (py_status == '0' and docker_status == '0' and yum_status == '0' and pip_status == '0'):
        print('执行释放资源池的操作')


if __name__ == '__main__':
    get_staus()
    if get_staus() == '1':
        main()



