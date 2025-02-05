FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    socat \
    lib32z1 \
    libseccomp-dev \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ctf

RUN useradd -m user

COPY challenge/echoChamber-v2 challenge/flag.txt challenge/libc.so.6 challenge/ld-linux-x86-64.so.2 ./

RUN patchelf --set-interpreter ./ld-linux-x86-64.so.2 ./echoChamber-v2 && \
    patchelf --set-rpath . ./echoChamber-v2

RUN chown -R root:user /ctf && \
    chmod 750 /ctf/echoChamber-v2 && \
    chmod 440 /ctf/flag.txt && \
    chmod 550 /ctf/libc.so.6 /ctf/ld-linux-x86-64.so.2

USER user

EXPOSE 1342

CMD socat TCP-LISTEN:1342,reuseaddr,fork EXEC:'timeout 120 ./echoChamber-v2'
