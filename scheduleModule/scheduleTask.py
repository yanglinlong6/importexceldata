import schedule
import time
import pymysql


# 定义你要周期运行的函数
def job():
    conn = pymysql.connect(host='192.168.3.222',
                           port=3307,
                           user='root',
                           password='Msd^*$@online',
                           database='newgps',
                           charset='utf8')
    cursor = conn.cursor()
    sql01 = "update d_device_login set lastRtTrack = sysdate(),lastGprsTime = sysdate() where sn = '1591126165';"
    cursor.execute(sql01)
    # 提交事务
    conn.commit()
    sql02 = "select sn ,lastRtTrack,lastGprsTime from d_device_login where sn = 1591126165;"
    cursor.execute(sql02)
    timeData = cursor.fetchall()
    print("I'm working...",timeData)
    # 提交事务
    conn.commit()
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()


if __name__ == '__main__':
    # schedule.every(4).minutes.do(job)                  # 每隔 10 分钟运行一次 job 函数
    schedule.every(5).seconds.do(job)  # 每隔 10 分钟运行一次 job 函数
    # schedule.every().hour.do(job)                    # 每隔 1 小时运行一次 job 函数
    # schedule.every().day.at("10:30").do(job)         # 每天在 10:30 时间点运行 job 函数
    # schedule.every().monday.do(job)                  # 每周一 运行一次 job 函数
    # schedule.every().wednesday.at("13:15").do(job)   # 每周三 13：15 时间点运行 job 函数
    # schedule.every().minute.at(":17").do(job)        # 每分钟的 17 秒时间点运行 job 函数

    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)
