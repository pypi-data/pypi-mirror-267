

import time
import librosa
import sys,os
from os import  path
sys.path.append(os.path.dirname(path.dirname(__file__)))
from formatConvert.wav_pcm import wav2pcm,pcm2wav
from POLQA.polqa_client import  polqa_client_test
from PEAQ.PEAQ import cal_peaq
import os
import wave
from SNR_ESTIMATION.MATCH_SIG import match_sig
from SNR_ESTIMATION.SNR_MUSIC import cal_snr_music
from AGC_EVALUATION.CAL_MUSIC_STABILITY import cal_music_stablility
from FUNCTION.audioFunction import isSlience,audioFormat,get_effective_spectral,cal_pitch,cal_EQ,get_rms_level_by_float
from CLIPPING_DETECTION.audio_clip_detection import cal_clip_index
from commFunction import get_data_by_sf,make_out_file_sf
import pyloudnorm

allMetrics = ['ALL','POLQA','PEAQ','LUFS','MUSIC','MATCH','MUSICSTA','SLIENCE','FORMAT','RMS','CLIP','DELAY','SPEC','EQ']


class computeAudioQuality():
    def __init__(self,**kwargs):
        """
        :param kwargs:
        """
        #print(**kwargs)
        self.__parse_para(**kwargs)
        self.__chcek_valid()
        pass

    def __parse_para(self,**kwargs):
        """
        :param kwargs:
        :return:
        """
        self.mertic = kwargs['metrics']
        self.testFile = kwargs['testFile']
        self.refFile = kwargs['refFile']
        self.outFile = kwargs['outFile']
        self.audioType = kwargs["audioType"]
        self.calSection = kwargs["calSection"]
        self.polqaMode = kwargs["polqaMode"]
        self.rmsFrameDuration = kwargs["rmsFrameDuration"]
        self.rmsShiftDuration = kwargs["rmsShiftDuration"]

        self.data,self.samrate,self.channel = get_data_by_sf(self.testFile)

        self.refdata,self.reffs,self.refch = get_data_by_sf(self.refFile)

        #assert  self.samrate == self.reffs
        #assert  self.channel == self.refch

        self.usedata = self.data[int(self.calSection[0] * self.samrate):int(self.calSection[1] * self.samrate)]

        # self.testFile_L,self.testFile_R = self.Extract_Mono(self.testFile)
        #
        # self.refFile_L, self.refFile_R = self.Extract_Mono(self.refFile)
        # if self.outFile is not None:
        #     self.outFile_L, self.outFile_R = self.outFile[:-4] + '_L.wav',self.outFile[:-4] + '_R.wav'
        # else:
        #     self.outFile_L, self.outFile_R = None,None
        # if self.refFile is not None:
        #     self.__double_end_check()
    def Extract_Mono(self,audioFile):
        """
        :return:
        """
        # try:
        #     stereo_data,frame,nchanel = get_data_array(audioFile)
        #     left_data = stereo_data[::2]
        #     right_data = stereo_data[1::2]
        #     l_name,r_name = audioFile[:-4] + '_L.wav',audioFile[:-4] + '_R.wav'
        #     make_out_file(l_name, left_data, frame, 1)
        #     make_out_file(r_name, right_data, frame, 1)
        #     return  l_name,r_name
        # except:
        #     return None,None



    def __chcek_valid(self):
        """
        :return:
        """
        if self.mertic not in allMetrics:
            raise ValueError('matrix must betwin ' + str(allMetrics))

    def __check_format(self,curWav):
        """
        :param curWav:
        :return:
        """
        curType = os.path.splitext(curWav)[-1]
        if curType !='.wav':
            raise TypeError('audio format must be wav ')
        wavf = wave.open(curWav,'rb')
        curChannel = wavf.getnchannels()
        cursamWidth = wavf.getsampwidth()
        cursamplerate = wavf.getframerate()
        wavf.close()
        if curChannel != 2:
            raise ValueError('wrong type of channel' + curWav)
        if cursamWidth != 2:
            raise ValueError('wrong type of samWidth' + curWav)
        if cursamplerate != 48000:
            raise ValueError('wrong type of samplerate' + curWav)
        return curChannel,cursamWidth,cursamplerate

    def __double_end_check(self):
        """
        :return:
        """
        if  self.refFile is None or self.testFile is None:
            raise EOFError('lack of inputfiles!')
        if self.__check_format(self.testFile) != self.__check_format(self.refFile):
            raise TypeError('there are different parametre in inputfiles!')


    def POLQA(self):
        """
        #POLQA  窄带模式  8k   超宽带模式 48k
        # pcm输入
        :return:
        """

        curCH,curBwidth,curSR = self.__check_format(self.testFile)
        result_l =  polqa_client_test(wav2pcm(self.refFile_L),wav2pcm(self.testFile_L),curSR,mode=self.polqaMode)
        result_r = polqa_client_test(wav2pcm(self.refFile_R), wav2pcm(self.testFile_R), curSR, mode=self.polqaMode)
        time.sleep(2)
        return  result_l,result_r


    def PEAQ(self):
        """
        # wav输入
        :return:
        """
        #TODO 计算peaq
        return cal_peaq(self.refFile,self.testFile)
        pass



    def MUSIC(self):
        """
        # MUSIC SNR
        # 无采样率限制
        # WAV/PCM 输入
        :return:
        """
        return cal_snr_music(refFile=self.refFile_L,testFile=self.testFile_L),cal_snr_music(refFile=self.refFile_R,testFile=self.testFile_R)


    def MATCH(self):
        """
        # MATCH SIG
        # 无采样率限制
        # 可选择是否输出文件
        # WAV/PCM 输入
        :return:
        """
        src_temp = 'src.wav'
        test_temp = 'test.wav'
        target_amplerate  = 8000
        for i in range(self.channel):
            cursrc = librosa.resample(self.refdata[:, i], orig_sr=self.samrate, target_sr=target_amplerate)
            curdata = librosa.resample(self.data[:, i], orig_sr=self.reffs, target_sr=target_amplerate)
            make_out_file_sf(src_temp,cursrc,target_amplerate)
            make_out_file_sf(test_temp, curdata, target_amplerate)
            delay = match_sig(src_temp, test_temp)
            if delay is not None:
                return delay

        return None


    def LUFS(self):
        """
        Returns
        -------

        """

        # TODO
        # data, rate,channel = get_data_array(test,datatype=np.float64)
        # data2, rate = sf.read(test)
        # data_l = data2[:, 1]
        # # print(data)
        # print(data2)
        # print(data_l)
        # # 计算LUFS值
        meter = pyloudnorm.Meter(self.samrate)  # 创建Meter对象
        loudness = meter.integrated_loudness(self.usedata)  # 计算音频的整体响度
        return loudness


    def MUSICSTA(self):
        """
        AGC PARA 3
        计算music 信号稳定性
        :return:
        """
        return cal_music_stablility(refFile=self.refFile_L,testFile=self.testFile_L),cal_music_stablility(refFile=self.refFile_R,testFile=self.testFile_R)



    def SLIENCE(self):
        """
        Returns
        -------

        """
        return isSlience(self.testFile_L,section=self.calSection),isSlience(self.testFile_R,section=self.calSection)

    def FORMAT(self):
        """
        Returns
        -------

        """
        return audioFormat(self.testFile)


    def RMS(self):
        """
        Returns
        -------
        # (wavFileName=None,rmsMode='total',startTime=0,endTime=1):
        """
        # TODO 重新改造

        return get_rms_level_by_float(self.usedata,self.samrate,self.rmsFrameDuration,self.rmsShiftDuration)


    def CLIP(self):
        """
        Returns
        -------

        """
        return cal_clip_index(self.usedata,samplerate=self.samrate)



    def SPEC(self):
        """
        Returns
        -------

        """
        spec_list = []
        for i in range(self.channel):
            curdata = self.usedata[:, i]
            spec = get_effective_spectral(curdata,self.samrate)
            spec_list.append(spec)

        return spec_list


    def EQ(self):
        """
        Returns
        -------

        """
        self.__double_end_check()
        return cal_EQ(self.refFile_L,self.testFile_L),cal_EQ(self.refFile_R,self.testFile_R)


    def FR(self):
        pass

    def PLAY_DELAY(self):
        pass

    def VISQOL(self):
        pass

    def L_R_Cons(self):
        pass

    def ALL(self):

        pass


if __name__ == '__main__':
    pass


