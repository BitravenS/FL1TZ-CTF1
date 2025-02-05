FROM ubuntu:latest

RUN apt-get update && apt-get install -y socat
RUN apt-get install -y lib32z1 libseccomp-dev

WORKDIR /ctf

RUN useradd -m user

COPY challenge/reviewHub challenge/flag.txt ./

RUN chown -R root:user /ctf && \
    chmod 750 /ctf/reviewHub && \
    chmod 440 /ctf/flag.txt

USER user

EXPOSE 1340

CMD socat TCP-LISTEN:1340,reuseaddr,fork EXEC:'timeout 120 ./reviewHub'
