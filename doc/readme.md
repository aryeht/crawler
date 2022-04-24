Presentation created with MARP

    # Convert slide deck into PDF (using Chromium in Docker)
    chmod 777 .
    `docker run --rm --init -v $PWD:/home/marp/app/ -e LANG=$LANG marpteam/marp-cli presentation.md --pdf`
