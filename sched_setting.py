"""
Checked Scheduler Trigger Config
config value -> 
  "redishealthcheck": {
    "trigger": "interval",
    "seconds": "31"
  },
  "loadcellheartbreak": {
    "trigger": "cron",
    "hour": "9",
    "minute": "2"
  },
  "loadcellheartbreakcustom": {
    "trigger": "interval",
    "seconds": "300"
  },
  "camanglecheck": {
    "trigger": "cron",
    "hour": "*",
    "minute": "*/1"
  }
"""
def check_sched_config():
    
    for job_id in evt_obj.keys():
        
        try:
            if sched_config[job_id] != now_config[job_id]:
                
                worker = sched.get_job(job_id)
                
                if now_config[job_id]['trigger']== "interval":
                    seconds = int(now_config[job_id]["seconds"])
                    worker.reschedule("interval", seconds=seconds)
                    logger.warning(f"Changed [{job_id}] Scheduler Worker \n Before : {sched_config[job_id]} \n Now : {now_config[job_id]}")
                    sched_config[job_id] = now_config[job_id]
                    
                elif now_config[job_id]['trigger']== "cron":
                    hour = now_config[job_id]["hour"]
                    minute = now_config[job_id]["minute"]
                    worker.reschedule("cron", hour=hour, minute=minute)
                    logger.warning(f"Changed [{job_id}] Scheduler Worker \n Before : {sched_config[job_id]} \n Now : {now_config[job_id]}")
                    sched_config[job_id] = now_config[job_id]
                    
                else:
                    logger.warning(f"Need Check [{job_id}] Changed Scheduler Worker Config \n Before : {sched_config[job_id]} \n Now : {now_config[job_id]}")
                    
        except Exception as e:
            logger.error(f"[{job_id}] Scheduler Config Update Error")