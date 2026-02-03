FROM quay.io/pypa/manylinux_2_28_x86_64

RUN dnf -y install gcc git-core make cmake llvm

COPY build.py /app/build.py
COPY CMakeLists.txt /app/CMakeLists.txt
COPY lldAsLib.cpp /app/lldAsLib.cpp
RUN cd /app/ && python3 build.py x64
