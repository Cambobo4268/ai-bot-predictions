#!/data/data/com.termux/files/usr/bin/bash
termux-setup-storage
curl -L -o ~/ai_trading_bot/predictions.json "https://drive.google.com/uc?export=download&id=1oSs8h4gtlM016DOC5DcZSHRHIl4XaIDf"
echo
cat ~/ai_trading_bot/predictions.json
