FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    socat \
    lib32z1 \
    libseccomp-dev \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ctf

RUN useradd -m user

COPY challenge/blind challenge/flag.txt ./

RUN chown -R root:user /ctf && \
    chmod 750 /ctf/blind && \
    chmod 440 /ctf/flag.txt && \

USER user

EXPOSE 1344

CMD socat TCP-LISTEN:1344,reuseaddr,fork EXEC:'timeout 180 ./blind'
