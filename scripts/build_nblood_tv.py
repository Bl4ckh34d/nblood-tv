"""Cross-build the native NBlood libretro adapter for ARMv7 Android."""
from pathlib import Path
import os, subprocess, shutil

from source_setup import ROOT, SOURCES, NDK, prepare
SOURCE=SOURCES/'nblood-libretro'
OUTPUT=ROOT/'build/nblood-tv'
def main():
    prepare()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    tool=NDK/'toolchains/llvm/prebuilt/windows-x86_64/bin'
    env=os.environ.copy()
    env['PATH']='C:/Program Files/Git/usr/bin;C:/Program Files/Git/bin;'+env['PATH']
    args=[str(NDK/'prebuilt/windows-x86_64/bin/make.exe'),'-f','Makefile.libretro',
          'SHELL='+os.environ.get('GIT_SH','C:/Progra~1/Git/bin/sh.exe'),'GAME=blood','platform=android-arm',
          'CC='+str(tool/'clang.exe')+' --target=armv7a-linux-androideabi21',
          'CXX='+str(tool/'clang++.exe')+' --target=armv7a-linux-androideabi21',
          'LDFLAGS=-static-libstdc++','LIBS=-ldl -lm -llog',
          'TESTS=1','OUT_DIR='+OUTPUT.as_posix(),'-j6']
    with (OUTPUT/'build.log').open('w',encoding='utf-8') as log:
        p=subprocess.Popen(args,cwd=SOURCE,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        for line in p.stdout:
            log.write(line)
            if any(s in line for s in ['error:','undefined reference','Error ']): print(line.strip(),flush=True)
        result=p.wait()
    print('NBlood build exit',result,flush=True)
    if not result:
        (ROOT/'release').mkdir(exist_ok=True)
        shutil.copyfile(OUTPUT/'nblood_libretro.so',ROOT/'release/blood_libretro_android.so')
    return result
if __name__=='__main__': raise SystemExit(main())
