﻿# -*- coding: UTF-8 -*-
from setuptools import setup
import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
    name='musicAlgLib',
    version='1.1.8',
    packages=setuptools.find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='MIT',
    author=' MA JIANLI',
    author_email='majianli@corp.netease.com',
    description='audio algorithms to compute and test music quality',
    long_description="""
        Audio test libs to compute audio quality and 3A performance by objective metrics
    pcm,wav inputfiles is allowed,support different samplerate (invalid params are simply corrected to valid ones)
    
    # How to install ?
    #Install with pip:
    
    simply use pip to install this toolkit
    
    "pip install algorithmLib"
    
    # How to use?
    
        #just see ./demos/ 	
    
    #  PESQ example
    src = "a.pcm"
    test = "b.pcm"
    
    score = compute_audio_quality('PESQ',testFile=test,refFile=src,samplerate=16000)
    
    or
    
    src = "a.wav"
    test = "b.wav"
    
    score = compute_audio_quality('PESQ',testFile=test,refFile=src)
    #  G160 example
    src = "a.wav"
    test = "b.wav"
    cle = "c.wav"
    tnlr,nplr,snri,dsn  = compute_audio_quality("G160",testFile=test,refFile=src,cleFile=cle)
    or 
    src = "a.pcm"
    test = "b.pcm"
    cle = "c.pcm"
    tnlr,nplr,snri,dsn  = compute_audio_quality("G160",testFile=test,refFile=src,cleFile=cle,samplerate=48000)
    #p563 example
    test = "a.wav"
    Mos,SpeechLevel,Snr,NoiseLevel = compute_audio_quality('P563',testFile=test)
    :param metrics: /POLQA/PEAQ/LOUDNESS/MUSIC/MATCH/
                    /MUSICSTA/
                    /SLIENCE/FORMAT/TRMS/ARMS/PRMS/SRMS/CLIP/DELAY/ECHO/SPEC/PITCH/EQ，必选项
    # POLQA 窄带模式  8k  超宽带模式 48k ；WAV/PCM输入 ；双端输入：ref、test；时长 < 20s；
    # PEAQ 无采样率限制；WAV/PCM输入 ；双端输入：ref、test；无时间长度要求；
    # MATCH 无采样率限制; WAV/PCM输入;三端输入：ref、test、out； 无时间长度要求；
    # MUSIC 无采样率限制;WAV/PCM输入;双端输入：ref、test；无时间长度要求；
    # MUSICSTA 无采样率限制,WAV/PCM输入;双端输入：ref、test；无时间长度要求；
    # SLIENCE 无采样率限制 WAV/PCM/MP4输入;单端输入：test；无时间长度要求；
    # FORMAT 无采样率限制 WAV/MP4输入;单端输入：test；无时间长度要求；
    # TRMS 无采样率限制 WAV/PCM输入 ；单端输入：test；无时间长度要求；
    # ARMS 无采样率限制 WAV/PCM输入 ；单端输入：test；无时间长度要求；
    # PRMS 无采样率限制 WAV/PCM输入 ；单端输入：test；无时间长度要求；
    # SRMS 无采样率限制 WAV/PCM输入 ；单端输入：test；无时间长度要求；
    # CLIP 无采样率限制 WAV/PCM输入 ；单端输入：test；无时间长度要求；
    # DELAY 无采样率限制; WAV/PCM输入;双端输入：ref、test； 无时间长度要求；
    # SPEC 无采样率限制; WAV/PCM输入;单端输入：test； 无时间长度要求；
    # PITCH 无采样率限制；WAV/PCM输入;双端输入：ref、test； 无时间长度要求；
    # EQ 无采样率限制；WAV/PCM输入;双端输入：ref、test； 无时间长度要求；
    # MATCH2 无采样率限制; WAV/PCM输入;三端输入：ref、test、out； 无时间长度要求；
    # MATCH3 无采样率限制; WAV/PCM输入;三端输入：ref、test、out； 无时间长度要求；
    不同指标输入有不同的采样率要求，如果传入的文件不符合该指标的要求，会自动变采样到合法的区间
    :param testFile: 被测文件，必选项
    :param refFile:  参考文件，可选项，全参考指标必选，比如POLQA/PESQ/PEAQ
    :param outFile 输出文件，可选项，对齐文件可选
    :param audioType  输入音频的模式 0：语音 1：音乐 MATCH/GAINTABLE需要
    :param rmsCalsection 计算rms的区间 TRMS和ARMS需要，时间单位s，比如：[1,20]
    :param polqaMode 计算polqa的模式 0:默认模式  1: 理想模式：排除小声音的影响，把声音校准到理想点平 -26db
    :param pitchLogMode 计算pitch的模式 0：线性模式，用于SetLocalVoicePitch接口; 1：对数模式,用于SetAudioMixingPitch接口；默认为1
    :param fineDelaySection 精准计算延时(MTACH3)，需要手动标出语音块的位置，比如有三段：speech_section=[[2.423,4.846],[5.577,7.411],[8,10.303]]
    :return:
    """,
    long_description_content_type="text/markdown",
    install_requires=[
    'numpy',
    'wave',
    'matplotlib',
    'datetime',
    'scipy',
    'pystoi',
    'paramiko',
    'pyloudnorm',
    'soundfile'
    'torch',
    'torchaudio',
    'librosa',
    'requests',
    'pandas',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[
        ('', ['musicAlgLib/DLLS/cygwin1.dll']),
        ('', ['musicAlgLib/DLLS/peaqb.exe']),
        ('', ['musicAlgLib/DLLS/peaqb']),
        ('', ['musicAlgLib/DLLS/matchsig.dll']),
        ('', ['musicAlgLib/DLLS/snr_music.dll']),
        ('', ['musicAlgLib/DLLS/musicStability.dll']),
        ('', ['musicAlgLib/DLLS/pcc.dll']),
        ('', ['musicAlgLib/DLLS/matchsig.dylib']),
        ('', ['musicAlgLib/DLLS/snr_music.dylib']),
        ('', ['musicAlgLib/DLLS/musicStability.dylib']),
        ('', ['musicAlgLib/DLLS/pcc.dylib']),
        ('', ['musicAlgLib/DLLS/matchsig.so']),
        ('', ['musicAlgLib/DLLS/snr_music.so']),
        ('', ['musicAlgLib/DLLS/musicStability.so']),
        ('', ['musicAlgLib/DLLS/pcc.so']),
        ('', ['musicAlgLib/DLLS/silero_vad.jit'])],

    python_requires='>=3.6',
)



