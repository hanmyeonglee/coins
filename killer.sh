#!/bin/bash

PROCESS_NAME="multi-trader.py"

# 프로세스 이름으로 PID 찾기
PIDS=$(ps -ef | grep "$PROCESS_NAME" | grep -v "grep" | awk '{print $2}')

# PID가 존재하는지 확인
if [ -z "$PIDS" ]; then
  echo "No process found with name: $PROCESS_NAME"
  exit 1
fi

# 찾은 PID를 종료
for PID in $PIDS; do
  echo "Killing process $PID"
  kill -2 $PID
done

# nohup 파일 삭제
rm /home/root/coins/nohup.out

echo "Done."
