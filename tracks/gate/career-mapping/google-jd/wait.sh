#!/bin/bash
# usage: wait.sh <seconds> ; returns early if STOP exists, COMMANDS.md changes (vs mtime at start), or the download exits
cd ./tracks/gate/career-mapping/google-jd/
m=$(stat -c %Y COMMANDS.md); s=$(date +%s)
while [ ! -e STOP ] && [ "$(stat -c %Y COMMANDS.md)" = "$m" ] && [ $(( $(date +%s) - s )) -lt ${1:-580} ]; do sleep 5; done
[ -e STOP ] && echo "STOP EXISTS"; [ "$(stat -c %Y COMMANDS.md)" = "$m" ] || echo "COMMANDS CHANGED"
pgrep -f "python3.*c3_download.py" >/dev/null && echo "job running" || echo "JOB NOT RUNNING"
python3 -c "import json;p=json.load(open('c3_progress.json'));print(p['updated'],p['status'],p['stored_total'],p['stored_by_description_year'],p['ledgered_by_reason'],'remaining',p['remaining_requestable'])"
tail -1 requests.jsonl
