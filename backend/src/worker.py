import os,time,json,logging
from pathlib import Path
import redis
from src.config.database import Session
from src.models.entities import Run
from src.services.analysis import choose
r=redis.Redis.from_url(os.environ['REDIS_URL'])
with Session() as recovery:
 for pending in recovery.query(Run).filter(Run.state.in_(['queued','running'])).all():
  pending.state='queued';r.rpush('airpower:runs',pending.id)
 recovery.commit()
while True:
 Path('/tmp/heartbeat').touch()
 try:
  item=r.blpop('airpower:runs',timeout=3)
  if not item:continue
  with Session() as s:
   row=s.get(Run,int(item[1]))
   if not row or row.state!='queued':continue
   snapshot=row.result['snapshot'];row.state='running';s.commit()
   try:
    row.result={**choose(snapshot,row.features,row.alphas),'snapshot':snapshot};row.state='done'
    Path('/artifacts/'+str(row.id)+'.json').write_text(json.dumps(row.result,ensure_ascii=False))
   except Exception as e:row.state='failed';row.error=str(e)
   s.commit()
 except Exception:logging.exception('worker');time.sleep(2)
