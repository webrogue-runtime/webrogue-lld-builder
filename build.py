import os
import subprocess
import sys

arg = sys.argv[1]

def find_llvm_tool(name, version_arg):
    try:
        if subprocess.run([name, version_arg]).returncode == 0:
            return name
    except FileNotFoundError:
        pass
    for version in range(26, 16, -1):
        versioned_name = f"{name}-{version}"
        try:
            if subprocess.run([versioned_name, version_arg]).returncode == 0:
                return versioned_name
        except FileNotFoundError:
            pass
    raise ValueError(f"{name} not found")

llvm_ar = find_llvm_tool("llvm-ar", "--version")

repo_dir = os.path.dirname(os.path.realpath(__file__))
build_dir = os.path.join(repo_dir, "build")
if not os.path.exists(os.path.join(repo_dir, "llvm-project")):
    subprocess.run(
        [
            "git", 
            "clone",
            "--single-branch",
            "--depth=1",
            "https://github.com/llvm/llvm-project.git"
        ],
        cwd=repo_dir
    ).check_returncode()

args = [
    "cmake",
    "-S",
    str(repo_dir),
    "-B",
    str(build_dir),
]

def define(key: str, value: str):
    args.append(f"-D{key}={value}")


define("LLVM_ENABLE_PROJECTS", "lld")
define("BUILD_SHARED_LIBS", "OFF")
define("LLVM_ENABLE_LIBXML2", "OFF")
define("LLVM_ENABLE_ZLIB", "OFF")
define("LLVM_ENABLE_ZSTD", "OFF")
define("LLVM_ENABLE_TERMINFO", "OFF")
define("LLVM_TARGETS_TO_BUILD", "")
define("CMAKE_BUILD_TYPE", "Release")

if os.name == 'nt':
    # Windows
    define("CMAKE_C_FLAGS_DEBUG", "/Zi /Ob0 /Od /RTC1 -MT")
    define("CMAKE_C_FLAGS_RELEASE", "/O2 /Ob2 /DNDEBUG -MT")
    define("CMAKE_C_FLAGS_MINSIZEREL", "/O1 /Ob1 /DNDEBUG -MT")
    define("CMAKE_C_FLAGS_RELWITHDEBINFO", "/Zi /O2 /Ob1 /DNDEBUG -MT")
    define("CMAKE_CXX_FLAGS_DEBUG", "/Zi /Ob0 /Od /RTC1 -MT")
    define("CMAKE_CXX_FLAGS_RELEASE", "/O2 /Ob2 /DNDEBUG -MT")
    define("CMAKE_CXX_FLAGS_MINSIZEREL", "/O1 /Ob1 /DNDEBUG -MT")
    define("CMAKE_CXX_FLAGS_RELWITHDEBINFO", "/Zi /O2 /Ob1 /DNDEBUG -MT")
    define("CMAKE_MSVC_RUNTIME_LIBRARY", "MultiThreaded")
    define("LLVM_DISABLE_ASSEMBLY_FILES", "ON")
    args.append("-A")
    args.append(arg)
    args.append("-T")
    args.append("ClangCL")
elif sys.platform == "darwin":
    # macOS
    define("CMAKE_OSX_ARCHITECTURES", arg)
else:
    # linux
    pass

subprocess.run(args).check_returncode()

args = [
    "cmake",
    "--build",
    str(build_dir),
    "--parallel",
    f"{os.cpu_count()}"
]
if os.name == 'nt':
    args.append(f"--config=Release")

subprocess.run(args).check_returncode()

lib_search_paths = [
    build_dir,
    os.path.join(build_dir, "llvm-project", "llvm", "lib"),
    os.path.join(build_dir, "llvm-project", "llvm", "lib64")
]

libs = []

with open(os.path.join(build_dir, "lldAsLib_deps.txt"), "r") as file:
    for lib_name in file.read().strip().split(";"):
        found = False
        for lib_search_path in lib_search_paths:
            lib = os.path.join(lib_search_path, f"lib{lib_name}.a")
            if os.path.exists(lib):
                libs.append(lib)
                found = True
                break
        if not found:
            raise ValueError(f"{lib_name} not found")

out_path = os.path.join(repo_dir, "out")
if os.path.exists(out_path):
    os.remove(out_path)

args = [
    llvm_ar,
    "qLcs",
    str(out_path),
] + list(map(str, libs))
subprocess.run(args).check_returncode()
