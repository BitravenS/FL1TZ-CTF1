FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    socat \
    lib32z1 \
    libseccomp-dev \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ctf

RUN useradd -m user

COPY challenge/echoChamber challenge/flag.txt challenge/libc.so.6 challenge/ld-linux.so.2 ./

RUN patchelf --set-interpreter ./ld-linux.so.2 ./echoChamber && \
    patchelf --set-rpath . ./echoChamber

RUN chown -R root:user /ctf && \
    chmod 750 /ctf/echoChamber && \
    chmod 440 /ctf/flag.txt && \
    chmod 550 /ctf/libc.so.6 /ctf/ld-linux.so.2

USER user

EXPOSE 1341

CMD socat TCP-LISTEN:1341,reuseaddr,fork EXEC:'timeout 120 ./echoChamber'
