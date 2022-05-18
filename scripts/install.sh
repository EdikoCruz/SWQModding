if [ -f .env ]
then
    echo "INFO: Loading .env"
    source .env
else
    echo "INFO: Loading .env.default"
    source .env.default
fi


if [ ! -d "$GAME_FOLDER" ]
then
    echo "ERROR: GAME_FOLDER dir not exists, check .env"
    exit 1
fi

echo "INFO: Decompressing .impak files if any"
find "$GAME_FOLDER/game/Bundle" -name "*.impak" | sed -e's/ /\\ /g' | xargs --no-run-if-empty -n1 ./scripts/impakFile.py

echo "INFO: Decompressing .z files if any"
find "$GAME_FOLDER/game/Bundle" -name "*.z" | sed -e's/ /\\ /g' | xargs --no-run-if-empty -n1 ./scripts/zFile.py
