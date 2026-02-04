FROM quay.io/pypa/manylinux_2_28_x86_64

RUN dnf -y install gcc git-core make cmake llvm
RUN mkdir /app
RUN git -C /app clone --single-branch --depth=1 https://github.com/llvm/llvm-project.git -b main
COPY build.py /app/build.py
COPY CMakeLists.txt /app/CMakeLists.txt
COPY lldAsLib.cpp /app/lldAsLib.cpp
RUN cd /app/ && python3 build.py x64
