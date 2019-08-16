#!/usr/bin/env node

export FLASK_APP=server \
export FLASK_ENV=development \

if [ "${@}" == "run-flask" ]; then
    flask run
    elif [ "${@}" != "" ]; then
    bash ${@}
    echo "Что нужно ? Куда бежать ?"
else
    echo "Говори что хотел !"
fi