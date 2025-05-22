#!/data/data/com.termux/files/usr/bin/bash

FILE_ID="1oSs8h4gtM0160DC5DzSHRHI4X4nDLtfP"
DEST="$HOME/storage/shared/Download/predictions.json"
TMP="temp_dl.html"

termux-setup-storage
echo "⏳ Fetching clean predictions.json..."

# Download raw content
curl -L -o "$TMP" "https://drive.google.com/uc?export=download&id=$FILE_ID"

# Extract raw JSON if wrapped in <pre> tags (as Drive sometimes does)
JSON=$(cat "$TMP" | sed -n '/<pre.*>/,/<\/pre>/p' | sed 's/<[^>]*>//g')

# Fallback: if still empty, log and skip
if [ -z "$JSON" ]; then
  echo "{}" > "$DEST"
  echo "⚠️ No valid JSON found. Empty {} written to $DEST"
else
  echo "$JSON" > "$DEST"
  echo "✅ Clean JSON saved to $DEST"
fi

rm -f "$TMP"
