# install conda
set -e
wget "https://repo.anaconda.com/miniconda/Miniconda3-py37_4.10.3-Linux-x86_64.sh" -O ~/miniconda.sh
bash ~/miniconda.sh -b -p /opt/miniconda3
/opt/miniconda3/bin/conda init $(echo $SHELL | awk -F '/' '{print $NF}')
echo 'Successfully installed miniconda...'
echo -n 'Conda version: '
/opt/miniconda3/bin/conda --version
echo -e '\n'
source ~/.bashrc
export PATH="/opt/miniconda3/bin:$PATH"
# install ubuntu
export DEBIAN_FRONTEND=noninteractive
apt-get update && apt-get -o Dpkg::Options::="--force-confold" upgrade -q -y --force-yes && apt-get -o Dpkg::Options::="--force-confold" dist-upgrade -q -y --force-yes
apt remove vim-common -y
apt -y install unzip vim git nginx

# www
mkdir /www
mkdir /www/supervisor
mkdir /www/supervisor/logs
cd /www
git clone https://Kai.Wang23:Milo2009**@gitlab.geely.com/f-geelyecology/bdp/emotion_server.git

# bcecmd
cd /opt
wget https://sdk.bce.baidu.com/console-sdk/linux-bcecmd-0.3.0.zip
unzip linux-bcecmd-0.3.0.zip
cd /opt/linux-bcecmd-0.3.0
printf '31cb8d24568d4cf7aca733f50d82c223\n1f154ddb3caf4ad7bff53ff0d107da57\n\nbj\nbcebos.cloud.geely.com\nno\n8\nyes\n11\n11\n11\n' | ./bcecmd -c

./bcecmd bos cp bos:/bdp-i3-dev/emotionmodel.tar.gz /www/emotion_server
cd  /www/emotion_server/
cp logs/model_prodenv.py modelUtils/model_env.py
tar -zxvf emotionmodel.tar.gz

# pip
cd /www/emotion_server
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
pip install supervisor gunicorn -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
pip install -U gevent  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
# supervisor
cp  /www/emotion_server//logs/supervisor.conf  /www/supervisor/supervisor.conf
cd /www/emotion_server/
ip=`hostname -I`
python logs/writeSupervisor.py --prog=emotion_server --dir=/www/emotion_server --wpath=/www/supervisor/ --ports=1001 --porte=1008 --ip=$ip
supervisord -c /www/supervisor/supervisor.conf
#supervisorctl -c /www/supervisor/supervisor.conf reload
supervisorctl -c /www/supervisor/supervisor.conf restart all