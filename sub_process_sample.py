from apscheduler.schedulers.background  import BackgroundScheduler
from subprocess                         import PIPE, Popen
from subprocess                         import call
import os, sys
import time
import argparse
import subprocess
import logging, logging.config

# define
from config              import config
from utils.get_logger    import logger_type

logger = logger_type("root")

class SubProcessObj:
    
    def __init__(self, env, alarm_type):
        
        self.env            = env
        self.alarm_type     = alarm_type
        self.process_id     = None
        self.start_subprocess()
        
    def start_subprocess(self):
        try:
            exec_cmd = f"{os.path.join('python3 ./', sys.argv[0])} --type {self.alarm_type}"
            self.process_id = subprocess.Popen(exec_cmd, shell=True)
        except Exception as e:
            logger.error(f"{self.alarm_type} Start Subprocess Fail.. {e}")
    
    def poll_subprocess(self):
        try:
            if self.process_id.poll() is not None or self.process_id is None:
                logger.warning(f"{self.alarm_type} Subprocess Restart..")
                self.start_subprocess()
        except Exception as e:
            logger.error(f"{self.alarm_type} Checking Subprocess Fail.. {e}")
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Event_Worker_Env')
    parser.add_argument('--type', default='main', help='main(부모프로세스)')
    args    = parser.parse_args()
    # 작업 모드
    working_env = config.working_env if config.working_env == "oper" else "test"
    
    # alarmManager Main
    if args.type == 'main':
        
        logger.info(f"=================== Alarm Manager {working_env} Starting ==================")
        logger.info(f"Send Alarm Types -> {config.alarm_types}")
        
        # start subprocess
        # config.py file 내부에 alarm_types 리스트에 모든 알림 타입에 대한것을 정의 해야한다.
        subprocess_obj = list()
        for alarm_type in config.alarm_types:
            subprocess_obj.append(SubProcessObj(working_env, alarm_type))
            
        time.sleep(1)
        logger.info(f"==================== Alarm Manager {working_env} Started ==================")
        
        while True:
            time.sleep(10)
            for obj in subprocess_obj:
                obj.poll_subprocess()
    
    # Sub Process (Alarm Sender)
    else:
        
        if args.type in config.alarm_types:
            
            try:
                if args.type == 'kakao':
                    from alarm_types   import kakao_alarm
                    kakao_alarm.run(working_env, args.type, logger_type(args.type))
                    
                elif args.type == 'slack':
                    from alarm_types   import slack_alarm
                    slack_alarm.run(working_env, args.type, logger_type(args.type))
                    
            except Exception as e:
                logger.error(f"[{args.type}] Subprocess Error {e}")