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


echo "INFO: Compressing .z files if any"
find "$GAME_FOLDER/game/Bundle" -name "*.z.lock" | sed -e's/ /\\ /g' | xargs --no-run-if-empty -n1 ./scripts/zFile.py

echo "INFO: Compressing .impak files if any"
find "$GAME_FOLDER/game/Bundle" -name "*.impak.lock" | sed -e's/ /\\ /g' | xargs --no-run-if-empty -n1 ./scripts/impakFile.py

