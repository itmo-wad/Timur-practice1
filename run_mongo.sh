docker run --name some-mongo -p 127.0.0.1:27017:27017 -v $(pwd)/data:/data/db -d mongo
