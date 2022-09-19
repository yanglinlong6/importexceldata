# dc1 = {'XDG_SESSION_ID': '2', 'SPARK_HOME': '/usr/local/spark', 'TERM': 'xterm', 'SHELL': '/bin/bash', 'SSH_CLIENT': '192.168.249.223 50296 22', 'CONDA_SHLVL': '1', 'CONDA_PROMPT_MODIFIER': '(base) ', 'SSH_TTY': '/dev/pts/0', 'USER': 'root', 'LS_COLORS': 'rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:', 'CONDA_EXE': '/root/anaconda3/bin/conda', '_CE_CONDA': '', 'MAIL': '/var/mail/root', 'PATH': '/root/anaconda3/bin:/root/anaconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/spark/bin:/usr/local/spark/sbin:/usr/local/spark/bin:/usr/local/spark/sbin', 'CONDA_PREFIX': '/root/anaconda3', 'PWD': '/usr/lib/jvm/default-java', 'JAVA_HOME': '/usr/lib/jvm/default-java', 'LANG': 'en_US.UTF-8', '_CE_M': '', 'SHLVL': '1', 'HOME': '/root', 'LANGUAGE': 'en_US:', 'CONDA_PYTHON_EXE': '/root/anaconda3/bin/python', 'LOGNAME': 'root', 'SSH_CONNECTION': '192.168.249.223 50296 192.168.249.147 22', 'CONDA_DEFAULT_ENV': 'base', 'LESSOPEN': '| /usr/bin/lesspipe %s', 'XDG_RUNTIME_DIR': '/run/user/0', 'PYTHON_HOME': '/root/anaconda3/bin', 'LESSCLOSE': '/usr/bin/lesspipe %s %s', '_': '/root/anaconda3/bin/python', 'OLDPWD': '/usr/local/spark', 'PYSPARK_PYTHON': '/root/anaconda3/bin/python', 'SPARK_AUTH_SOCKET_TIMEOUT': '15', 'SPARK_BUFFER_SIZE': '65536'}
import os

# dc ={}
# for k,v in dc1.items():
#     if k in ['SPARK_HOME', 'PYTHON_HOME','PYSPARK_PYTHON', ]:
# os.environ[k] = v
os.environ['HADOOP_HOME'] = 'D:\JAVAAPP\hadoop-2.8.3'
os.environ['hadoop.home.dir'] = 'D:\JAVAAPP\hadoop-2.8.3'
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext

conf = SparkConf().setMaster('spark://112.74.125.238:7077')
conf.setAppName('kafka-app6')  # 名称
conf.set('spark.serializer', 'org.apache.spark.serializer.KryoSerializer')
conf.set('spark.sql.shuffle.partitions', '200')
conf.set('spark.default.parallelism', '200')
conf.set('spark.executor.memory', '512m')
conf.set("spark.driver.memory", "512m")

# spark.executor.cores：顾名思义这个参数是用来指定executor的cpu内核个数，分配更多的内核意味着executor并发能力越强，能够同时执行更多的task
# executor memory是每个节点上占用的内存。每一个节点可使用内存
sc = SparkContext.getOrCreate(conf)
print(sc)

w = sc.parallelize(['scala', 'java'])
b = w.first()

sc.sql("show tables").show()
print(b)
