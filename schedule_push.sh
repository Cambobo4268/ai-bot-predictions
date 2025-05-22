#!/data/data/com.termux/files/usr/bin/bash
termux-job-scheduler --job-id 777 \
  --script ~/ai_trading_bot/git_push.sh \
  --period-ms 1800000 \
  --persisted true
