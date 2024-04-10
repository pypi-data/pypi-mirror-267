from operator import methodcaller
from computeAudioQuality.mainProcess import computeAudioQuality
from ctypes import  *

def compute_music_quality(metrics,testFile=None,refFile=None,outFile=None,audioType=1,
                         calSection=None,polqaMode=0,rmsFrameDuration=0.05,rmsShiftDuration=0.05):
    """
    :param metrics: ['ALL','POLQA','PEAQ','LUFS','MUSIC','MATCH','MUSICSTA','SLIENCE','FORMAT','RMS','CLIP','DELAY','SPEC','EQ']

    #
    # POLQA 窄带模式  8k  超宽带模式 48k ；WAV/PCM输入 ；双端输入：ref、test；时长 < 20s；
    # PEAQ 无采样率限制；WAV/PCM输入 ；双端输入：ref、test；无时间长度要求；
    # MATCH 无采样率限制; WAV/PCM输入;三端输入：ref、test、out； 无时间长度要求；
    # MUSIC 无采样率限制;WAV/PCM输入;双端输入：ref、test；无时间长度要求；
    # MUSICSTA 无采样率限制,WAV/PCM输入;双端输入：ref、test；无时间长度要求；
    # SLIENCE 无采样率限制 WAV/PCM/MP4输入;单端输入：test；无时间长度要求；
    # FORMAT 无采样率限制 WAV/MP4输入;单端输入：test；无时间长度要求；
    # RMS 无采样率限制 WAV/PCM输入 ；单端输入：test；无时间长度要求；
    # NOISE 无采样率限制 WAV/PCM输入 ；双端输入：ref、test；无时间长度要求；
    # CLIP 无采样率限制 WAV/PCM输入 ；单端输入：test；无时间长度要求；
    # DELAY 无采样率限制; WAV/PCM输入;双端输入：ref、test； 无时间长度要求；
    # SPEC 无采样率限制; WAV/PCM输入;单端输入：test； 无时间长度要求；
    # EQ 无采样率限制；WAV/PCM输入;双端输入：ref、test； 无时间长度要求；
    不同指标输入有不同的采样率要求，如果传入的文件不符合该指标的要求，会自动变采样到合法的区间
    :param testFile: 被测文件，必选项
    :param refFile:  参考文件，可选项，全参考指标必选，比如POLQA/PESQ/PEAQ
    :param outFile 输出文件，可选项，对齐文件可选
    :param audioType  输入音频的模式 0：语音 1：音乐 MATCH/GAINTABLE需要
    :param calSection 计算区间 ，时间单位s，比如：[1,20]
    :param polqaMode 计算polqa的模式 0:默认模式  1: 理想模式：排除小声音的影响，把声音校准到理想点平 -26db
    :param rmsFrameDuration 计算rms的帧长度 默认50ms
    :param rmsShiftDuration 计算rms的帧移 默认50ms
    :return:
    """
    paraDicts = {
        'metrics':metrics,
        'testFile':testFile,
        'refFile':refFile,
        'outFile':outFile,
        "audioType":audioType,
        'calSection':calSection,
        'polqaMode':polqaMode,
        'rmsFrameDuration' : rmsFrameDuration,
        'rmsShiftDuration' : rmsShiftDuration
    }
    comAuQUA = computeAudioQuality(**paraDicts)
    return methodcaller(metrics)(comAuQUA)

if __name__ == '__main__':
    file = r'android_sp_yinxiang.wav'
    test = r'andorid_huanrao.wav'
    delay = compute_music_quality('PEAQ',refFile=file,testFile=file,calSection=[10,20])
    print(delay)
