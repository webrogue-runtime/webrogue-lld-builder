ARG ARCH
FROM quay.io/pypa/musllinux_1_2_${ARCH}
ARG ARCH

RUN apk add gcc git make cmake llvm
RUN mkdir /app
RUN git -C /app clone --single-branch --depth=1 https://github.com/llvm/llvm-project.git -b main
COPY build.py /app/build.py
COPY CMakeLists.txt /app/CMakeLists.txt
COPY lldAsLib.cpp /app/lldAsLib.cpp
RUN cd /app/ && python3 build.py ${ARCH}
