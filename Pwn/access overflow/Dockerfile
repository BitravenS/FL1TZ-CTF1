FROM ubuntu:latest

RUN apt-get update && apt-get install -y socat
RUN apt-get install -y lib32z1 libseccomp-dev

WORKDIR /ctf

RUN useradd -m user

COPY challenge/accessOverflow challenge/flag.txt ./

RUN chown -R root:user /ctf && \
    chmod 750 /ctf/accessOverflow && \
    chmod 440 /ctf/flag.txt

USER user

EXPOSE 1337

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'timeout 20 ./accessOverflow'
