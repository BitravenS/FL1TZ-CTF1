FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    socat \
    lib32z1 \
    libseccomp-dev \
    patchelf \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /ctf

# Create a non-root user
RUN useradd -m user

# Copy challenge files
COPY challenge/blind /ctf/blind
COPY challenge/flag.txt /ctf/flag.txt

# Set permissions
RUN chown -R root:user /ctf && \
    chmod 750 /ctf/blind && \
    chmod 440 /ctf/flag.txt

# Switch to the non-root user
USER user

# Expose the port
EXPOSE 1017

# Run the challenge
CMD socat TCP-LISTEN:1017,reuseaddr,fork EXEC:'timeout 180 ./blind'
