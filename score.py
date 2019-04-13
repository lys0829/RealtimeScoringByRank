import gevent
import time
import json
import logging
#import pprint #debug
from queue import Queue
from datetime import datetime

#from mod import config
from mod import ServiceCoord
from mod.rpc import RemoteServiceClient
from mod import config
from mod.rank import RankingWebServer
from mod.calc import GetRank

logger = logging.getLogger(__name__)
#pp = pprint.PrettyPrinter(indent=4)

RWS = RankingWebServer(config.RWSurl, config.RWSuser, config.RWSpass)

def WaitJudgeQueueEmpty(EvaluationService, Time):
    '''
    0. save subminssion id in worker
    1. check no compile in queue
    2. check no compile in worker
    3. check no evaluation in queue
    4. check no evaluation in worker
    5. check no step0 submission id in worker
    '''
    SubIDJustStart = []
    worker_status = EvaluationService.workers_status().result()
    for (wid,w) in worker_status.items():
        if w['connected']==False:
            continue
        if not type(w['operations'])==list:
            continue
        for op in w['operations']:
            if not op['object_id'] in SubIDJustStart:
                SubIDJustStart += [op['object_id']]
    
    SubIDCompInQueue = []
    checknciq = 0
    while checknciq<5:
        logger.info('Wait to no compile in queue')
        queue_status = EvaluationService.queue_status().result()
        check = True
        for job in queue_status:
            if (job['timestamp']<=float(Time)) and (job['item']['type']=='compile'):
                check = False
                if not job['item']['object_id'] in SubIDCompInQueue:
                    SubIDCompInQueue += [job['item']['object_id']]
        if check:
            checknciq+=1
        time.sleep(1)
    
    while len(SubIDCompInQueue)>0:
        logger.info('Wait to no compile in worker')
        worker_status = EvaluationService.workers_status().result()
        tmp = []
        for (wid,w) in worker_status.items():
            if w['connected']==False:
                continue
            if not type(w['operations'])==list:
                continue
            for op in w['operations']:
                if op['type'] == 'compile':
                    if not op['object_id'] in tmp:
                        tmp += [op['object_id']]
        nl = []
        for subid in SubIDCompInQueue:
            if subid in tmp:
                nl += [subid]
        SubIDCompInQueue = nl.copy()
        time.sleep(1)
    
    checkneiq = 0
    SubIDEvalInQueue = []
    while checkneiq<5:
        logger.info('Wait to no evaluate in queue')
        queue_status = EvaluationService.queue_status().result()
        check = True
        for job in queue_status:
            if (job['timestamp']<=float(Time)) and (job['item']['type']=='evaluate'):
                check = False
                if not job['item']['object_id'] in SubIDEvalInQueue:
                    SubIDEvalInQueue += [job['item']['object_id']]
        if check:
            checkneiq+=1
        time.sleep(1)

    while len(SubIDEvalInQueue)>0:
        logger.info('Wait to no evaluate in worker')
        worker_status = EvaluationService.workers_status().result()
        tmp = []
        for (wid,w) in worker_status.items():
            if not w['connected']:
                continue
            if not type(w['operations'])==list:
                continue
            for op in w['operations']:
                if op['type'] == 'evaluate':
                    if not op['object_id'] in tmp:
                        tmp += [op['object_id']]
        nl = []
        for subid in SubIDEvalInQueue:
            if subid in tmp:
                nl += [subid]
        SubIDEvalInQueue = nl.copy()
        time.sleep(1)
    while len(SubIDJustStart)>0:
        logger.info('Wait to no evaluate in worker')
        worker_status = EvaluationService.workers_status().result()
        tmp = []
        for (wid,w) in worker_status.items():
            if not w['connected']:
                continue
            if not type(w['operations'])==list:
                continue
            for op in w['operations']:
                if not op['object_id'] in tmp:
                    tmp += [op['object_id']]
        nl = []
        for subid in SubIDJustStart:
            if subid in tmp:
                nl += [subid]
        SubIDJustStart = nl.copy()
        time.sleep(1)
    return


ES = RemoteServiceClient(ServiceCoord("EvaluationService",0), auto_retry=0.5)
AS = RemoteServiceClient(ServiceCoord("AdminWebServer",0), auto_retry=0.5)

ES.connect()
AS.connect()
while True:
    if ES.connected and AS.connected:
        #logger.info("EvaluationService,0 connected")
        break
    gevent.sleep(0)

#pp.pprint(GetScore(RWS.get("/history"),time.time(),5))

JobQueue = Queue()
StartTime = int(time.mktime(datetime.strptime(config.start,"%Y-%m-%d %H:%M:%S").timetuple()))
EndTime = int(time.mktime(datetime.strptime(config.end,"%Y-%m-%d %H:%M:%S").timetuple()))
SkipTime = int(time.mktime(datetime.strptime(config.skipwaituntil,"%Y-%m-%d %H:%M:%S").timetuple()))
Interval = int(config.interval)*60

for t in range(StartTime, EndTime+1, Interval):
    #print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(t))))
    JobQueue.put(t)
logger.info("Job Queue has been set")

AllTaskG = RWS.get("tasks")
AllTask = {}
for tname in AllTaskG:
    if not tname==config.taskname:
        AllTask[tname] = AllTaskG[tname]

Extra_Headers = [""]*len(AllTask)
TaskOrder = {}
for (tname,t) in AllTask.items():
    Extra_Headers[t['order']] = t['name']
    TaskOrder[tname] = t['order']

RWScontest = {"name": config.taskname,
                "begin": StartTime,
                "end": EndTime+1,
                "score_precision": config.score_precision
                }

RWStask = {"name": config.taskname,
            "short_name": config.taskname,
            "contest": config.taskname,
            "max_score": config.maxscore,
            "extra_headers": Extra_Headers,
            "order": 100,
            "score_mode": "max",
            "score_precision": config.score_precision
            }
RWS.put("contests/"+config.taskname,json.dumps(RWScontest))
RWS.put("tasks/"+config.taskname,json.dumps(RWStask))

OldSubmissionList = RWS.get("submissions")
OldSubchangeList = RWS.get("subchanges")
OldSubmissionIDList = []
for (sid,s) in OldSubmissionList.items():
    if s['task'] == config.taskname:
        RWS.delete("submissions/"+str(sid))
        OldSubmissionIDList += [sid]
for (sid,s) in OldSubchangeList.items():
    if int(s['submission']) in OldSubmissionIDList:
        RWS.delete("subchanges/"+sid)

userlist = RWS.get("users")
UserScoreTemplate = {}
UserSubID = {}
SubID = config.MinSubID
SubmissionTemplate = {"user": "", "task": config.taskname, "time": StartTime}
SubchangeTemplate = {"submission": "", "time": StartTime, "score": 0.0, "extra": [""]}
UserExtraTemplate = {}

for (user,ud) in userlist.items():
    UserScoreTemplate[user] = 0
    UserExtraTemplate[user] = [""]*len(AllTask)
    UserSubID[user] = SubID
    US = SubmissionTemplate.copy()
    US['user'] = user
    #RWS.put("submissions/"+str(UserSubID[user]+i), json.dumps(US))
    #RWS.delete("submissions/"+str(UserSubID[user]+i))
    SubID+=JobQueue.qsize()


UserScoreTotal = UserScoreTemplate.copy()
ScoreSet = config.scoreset

History = RWS.get("history")

RoundCount = 0
while not JobQueue.empty():
    Time = JobQueue.get()
    while int(time.time())<Time+10:
        time.sleep(1)
    if Time > SkipTime:
        WaitJudgeQueueEmpty(ES, Time)
        History = RWS.get("history")
    logger.info("Start calculate "+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(Time))))

    UserScoreRound = UserScoreTemplate.copy()
    RankData = GetRank(History, Time, len(ScoreSet))
    UserExtra = UserExtraTemplate.copy()
    for (tname,ranklist) in RankData.items():
        if tname==config.taskname:
            continue
        for (r,ul) in ranklist.items():
            for user in ul:
                UserScoreRound[user] += ScoreSet[int(r)-1]
                UserScoreTotal[user] += ScoreSet[int(r)-1]
                UserExtra[user][TaskOrder[tname]] = str(ScoreSet[int(r)-1])
                
    
    for (user,ud) in userlist.items():
        SubmissionID = str(UserSubID[user]+RoundCount)
        Submission = SubmissionTemplate.copy()
        Submission['user'] = user
        Submission['time'] = Time
        RWS.put("submissions/"+SubmissionID, json.dumps(Submission))
        Subchanged = SubchangeTemplate.copy()
        Subchanged['submission'] = str(SubmissionID)
        Subchanged['score'] = float(UserScoreTotal[user])
        #Subchanged['extra'][0] = str(UserScoreRound[user])
        Subchanged['extra'] = UserExtra[user]
        Subchanged['time'] = Time
        SubchangeID = str(Time)+SubmissionID+"s"
        RWS.put("subchanges/"+SubchangeID, json.dumps(Subchanged))
        #RWS.delete("subchanges/"+SubchangeID)
    RoundCount+=1
    time.sleep(1)
    
#pp.pprint(UserScoreTotal)