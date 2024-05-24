# coding: UTF-8

import argparse
import os
##########################################
## Options and defaults
##########################################
def getOptions():
    parser = argparse.ArgumentParser(description='python *.py [option]')
    parser.add_argument('--prog', dest='prog', help="prog", required=True)
    parser.add_argument('--dir', dest='dir', help="dir", required=True)
    parser.add_argument('--ip', dest='ip', help="ip", default="127.0.0.1")
    parser.add_argument('--wpath', dest='wpath', help="write dir", required=True)
    parser.add_argument('--ports', dest='ports', help="port start",type=int, required=True)
    parser.add_argument('--porte', dest='porte', help="port end",type=int, required=True)
    args = parser.parse_args()

    return args

def main():
    options = getOptions()
    print(options)
    content = '''
[program:programname]
command= gunicorn -w 4 --keep-alive 120 --timeout 120  -k gevent -b ipaddress:port_int model_service:app --reload; the program (relative uses PATH, can take args)
startsecs=1                     ; # of secs prog must stay up to be running (def. 1)
startretries=3                  ; max # of serial start failures when starting (default 3)
process_name=%(program_name)s  ; process_name expr (default %(program_name)s)
;;numprocs=1                    ; number of processes copies to start (def 1)
directory=directoryname ; directory to cwd to before exec (def no cwd)
;;umask=022                     ; umask for process (default None)
;;priority=999                  ; the relative start priority (default 999)
autostart=true                  ; start at supervisord start (default: true)
autorestart=true                ; when to restart if exited after running (def: unexpected)
;;exitcodes=0,2                 ; 'expected' exit codes used with autorestart (default 0,2)
;;stopsignal=QUIT               ; signal used to kill process (default TERM)
;;stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
stopasgroup=true                ; send stop signal to the UNIX process group (default false)
killasgroup=true                ; SIGKILL the UNIX process group (def false)
;;user=chrism                   ; setuid to this UNIX account to run the program
;;redirect_stderr=true          ; redirect proc stderr to stdout (default false)
stdout_logfile=/www/supervisor/logs/%(program_name)s-out.log ; stdout log path, NONE for none; default AUTO
stdout_logfile_maxbytes=10MB   ; max # logfile bytes b4 rotation (default 50MB)
stdout_logfile_backups=10      ; # of stdout logfile backups (default 10)
stdout_capture_maxbytes=1MB    ; number of bytes in 'capturemode' (default 0)
stdout_events_enabled=false    ; emit events on stdout writes (default false)
stderr_logfile=/www/supervisor/logs/%(program_name)s-err.log ; stderr log path, NONE for none; default AUTO
stderr_logfile_maxbytes=10MB    ; max # logfile bytes b4 rotation (default 50MB)
stderr_logfile_backups=10      ; # of stderr logfile backups (default 10)
stderr_capture_maxbytes=1MB    ; number of bytes in 'capturemode' (default 0)
stderr_events_enabled=false    ; emit events on stderr writes (default false)
;;environment=JAVA_HOME="/usr" ; process environment additions (def no adds)
;;serverurl=AUTO



    '''
    for port in range(options.ports, options.porte+1):
        filename = options.prog + str(port) + ".ini"
        program = options.prog + str(port)
        filefull = os.path.join(options.wpath, filename)
        contents = content.replace("programname",program) \
            .replace("port_int",str(port)) \
            .replace("ipaddress",options.ip) \
            .replace("directoryname",options.dir)
        with open(filefull,'w') as f:
            f.write(contents)

if __name__ == "__main__":
    main()
