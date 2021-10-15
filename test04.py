import os


def dir_size(d):
    if os.path.isfile(d):
        fileSize = os.path.getsize(d)
        if fileSize > 10737418240:
            print(d, fileSize)

    if os.path.isdir(d):
        dir_list = os.listdir(d)
        for f in dir_list:
            file = os.path.join(d, f)
            if os.path.isfile(file):
                fileSize = os.path.getsize(file)
                if fileSize > 10737418240:
                    print(d, fileSize)
            if os.path.isdir(file):
                dir_size(file)  # 递归统计
    # return dirSize


def dir_size01(d):
    if os.path.isfile(d):
        fileSize = os.path.getsize(d)
        print(d, fileSize)

    if os.path.isdir(d):
        dir_list = os.listdir(d)
        for f in dir_list:
            file = os.path.join(d, f)
            if os.path.isfile(file):
                fileSize = os.path.getsize(file)
                print(file, fileSize)
            if os.path.isdir(file):
                dir_size(file)  # 递归统计
    # return dirSize


if __name__ == '__main__':
    # dir_size('D:\JAVAAPP\PowerDesigner 15\\bpm.chm')
    dir_size01('D:\JAVAAPP\PowerDesigner 15')
