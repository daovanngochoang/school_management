FROM ubuntu:latest
LABEL authors="andreas"

ENTRYPOINT ["top", "-b"]