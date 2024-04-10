import sys
sys.path.append('../')
import os,time
import socket
import paramiko
from stat import S_ISDIR as isdir
import  copy
from ctypes import *
import wave
import numpy as np
import math
import librosa


import numpy as np

import  soundfile as sf

def get_data_by_sf(file):
    """
    """
    data, rate = sf.read(file)
    return data,rate,len(data[0])




windowLen = 0.05

class emxArray_real_T(Structure):
 _fields_ = [
          ("pdata", POINTER(c_double)),  # c_byte
          ("psize", POINTER(c_int)),  # c_byte
          ("allocSize", c_int),  #  c_byte
          ("NumDimensions", c_int),  # c_byte
          ("canFreeData", c_uint),
]

def convert_error_header(wavfile,channels=1, bits=16, sample_rate=16000):
    suffix = os.path.splitext(wavfile)[-1]
    assert suffix == '.wav'

    newFileName = wavfile[:-4] + '_convertHeader.wav'
    pcmf = open(wavfile, 'rb')
    pcmdata = pcmf.read()
    pcmf.close()
    if bits % 8 != 0:
        raise ValueError("bits % 8 must == 0. now bits:" + str(bits))
    wavfile = wave.open(newFileName, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(bits // 8)
    wavfile.setframerate(sample_rate)
    wavfile.writeframes(pcmdata)
    wavfile.close()
    time.sleep(1)
    #os.remove(pcm_file)
    return newFileName

def get_data_array(filename,datatype=np.int16):
    """

    """
    f = wave.open(filename, "rb")
    # 读取格式信息
    # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    # 读取波形数据
    # 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）
    str_data = f.readframes(nframes)
    f.close()
    return np.frombuffer(str_data, dtype=datatype),framerate,nchannels

def get_data_array_double(filename,datatype=np.int16):
    """

    """
    f = wave.open(filename, "rb")
    # 读取格式信息
    # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    # 读取波形数据
    # 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）
    str_data = f.readframes(nframes)
    f.close()
    return np.frombuffer(str_data, dtype=datatype).astype(np.double),framerate,nchannels



def get_data_of_ctypes_(inWaveFile=None,int2float=False,datatype=np.int16):
    wavf = wave.open(inWaveFile, 'rb')
    refChannel,refsamWidth,refsamplerate,refframeCount = wavf.getnchannels(),wavf.getsampwidth(),wavf.getframerate(),wavf.getnframes()

    # if (refChannel,refsamWidth) != (1,2):
    #     raise TypeError('Different format of ref and test files!')
    pcmdata = wavf.readframes(refframeCount)

    ref = np.frombuffer(pcmdata,dtype=datatype)

    ref = ref.astype(np.float64)
    if int2float:
        ref = ref/32768
    datastruct = emxArray_real_T()

    datastruct.pdata = (c_double * refframeCount)(*ref)
    datastruct.psize = (c_int * 1)(*[refframeCount])
    wavf.close()
    return  datastruct,refsamplerate,refframeCount

def get_data_of_ctypes_from_datablock(inData=None,datalen=96000,int2float=False):

    ref = np.frombuffer(inData,dtype=np.int16)

    ref = ref.astype(np.float64)
    if int2float:
        ref = ref/32768
    datastruct = emxArray_real_T()
    datastruct.pdata = (c_double * datalen)(*ref)
    datastruct.psize = (c_int * 1)(*[datalen])

    return  datastruct

def get_none_data_of_ctypes_(dataLength=0):

    data =  np.array([0.0 for _ in range(dataLength)])
    data = data.astype(np.float64)

    outStruct = emxArray_real_T()
    #outStruct = create_string_buffer(20)
    outStruct.pdata =  (c_double * dataLength)(*data)
    outStruct.psize = (c_int * 1)(*[dataLength])
    outStruct.allocSize = dataLength
    outStruct.NumDimensions = 1
    outStruct.canFreeData = 1
    return outStruct



def write_ctypes_data_2_file_(outFile,outStruct,refsamplerate):
    outf = wave.open(outFile, 'wb')
    outf.setnchannels(1)
    outf.setsampwidth(2)
    outf.setframerate(refsamplerate)
    # 将wav_data转换为二进制数据写入文件
    outlist = []
    for a in range(outStruct.psize[0]):
        outlist.append(int(outStruct.pdata[a]))
    outarray = np.array(outlist)
    outarray = outarray.astype(np.int16)
    outf.writeframes(bytes(outarray))
    outf.close()
constMosResult = {'delay':'No Result','mos':'-0.0','Speech Level Gain':'','Noise Level Gain':'','err':'No error'}

class commondata():
    def __init__(self):
        self.mosResult = copy.deepcopy(constMosResult)
        self.HOST = '10.219.36.124'
        self.machost = '10.219.36.124' #'10.242.167.159'
        self.username = 'netease'
        self.password = 'Nora3390'
        self.PORT = 2159
        self.sftpPort = 22
    @staticmethod
    def get_data():
        return {"type": "command",
        "module": "clientA",
        "method": "requestA",
        "samplerate":16000,
        "token": "",
        "job":None,
        "srcFile":'',
        "testFile":'',
        "result":{},
        "err":"No error"}

global_result = commondata()
def log_time():
    time_tup = time.localtime(time.time())
    # format_time = '%Y-%m-%d_%a_%H-%M-%S'
    format_time = '%Y-%m-%d-%H-%M-%S'

    cur_time = time.strftime(format_time, time_tup)
    return cur_time

def getip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        vqtip = s.getsockname()[0]
    finally:
        s.close()

    return vqtip


def exec_shell_command(cmd):
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=serverIP, port=port, username=username, password=password, allow_agent=False,
                look_for_keys=False)
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
    result = stdout.read()
    ssh.close()
    return result



def sftp_connect(username,password,host,port=22):
    client = None
    sftp = None
    try:
        client = paramiko.Transport((host,port))
    except Exception as error:
        print(error)
    else:
        try:
            client.connect(username=username, password=password)
        except Exception as error:
            print(error)
        else:
            sftp = paramiko.SFTPClient.from_transport(client)
    return client,sftp


def sftp_disconnect(client):
    try:
        client.close()
    except Exception as error:
        print(error)





def _check_local(local):
    if not os.path.exists(local):
        try:
            os.mkdir(local)
        except IOError as err:
            print(err)


def sftp_get(sftp, remote, local):
    # 检查远程文件是否存在
    try:
        result = sftp.stat(remote)
    except IOError as err:
        error = '[ERROR %s] %s: %s' % (err.errno, os.path.basename(os.path.normpath(remote)), err.strerror)
        print(error)
    else:
        # 判断远程文件是否为目录
        if isdir(result.st_mode):
            dirname = os.path.basename(os.path.normpath(remote))
            local = os.path.join(local, dirname)
            _check_local(local)
            for file in sftp.listdir(remote):
                sub_remote = os.path.join(remote, file)
                sub_remote = sub_remote.replace('\\', '/')
                sftp_get(sftp, sub_remote, local)
        else:
            # 拷贝文件
            if os.path.isdir(local):
                local = os.path.join(local, os.path.basename(remote))
            try:
                sftp.get(remote, local)
            except IOError as err:
                print(err)
            else:
                print('[get]', local, '<==', remote)


def sftp_put(sftp, local, remote):
    # 检查路径是否存在
    def _is_exists(path, function):
        path = path.replace('\\', '/')
        try:
            function(path)
        except Exception as error:
            return False
        else:
            return True

    # 拷贝文件
    def _copy(sftp, local, remote):
        # 判断remote是否是目录
        if _is_exists(remote, function=sftp.chdir):
            # 是，获取local路径中的最后一个文件名拼接到remote中
            filename = os.path.basename(os.path.normpath(local))
            remote = os.path.join(remote, filename).replace('\\', '/')
        # 如果local为目录
        if os.path.isdir(local):
            # 在远程创建相应的目录
            _is_exists(remote, function=sftp.mkdir)
            # 遍历local
            for file in os.listdir(local):
                # 取得file的全路径
                localfile = os.path.join(local, file).replace('\\', '/')
                # 深度递归_copy()
                _copy(sftp=sftp, local=localfile, remote=remote)
        # 如果local为文件
        if os.path.isfile(local):
            try:
                sftp.put(local, remote)
            except Exception as error:
                print(error)
                print('[put]', local, '==>', remote, 'FAILED')
            else:
                print('[put]', local, '==>', remote, 'SUCCESSED')

    # 检查local
    if not _is_exists(local, function=os.stat):
        print("'" + local + "': No such file or directory in local")
        return False
    # 检查remote的父目录
    remote_parent = os.path.dirname(os.path.normpath(remote))
    if not _is_exists(remote_parent, function=sftp.chdir):
        print("'" + remote + "': No such file or directory in remote")
        return False
    # 拷贝文件
    _copy(sftp=sftp, local=local, remote=remote)


def get_file_path(root_path,file_list,dir_list):
    #获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            #递归获取所有文件和目录的路径
            get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)


def project_root_path(project_name=None):

    """

    获取当前项目根路径

    :param project_name:

    :return: 根路径

    """

    PROJECT_NAME = 'audiotestalgorithm' if project_name is None else project_name

    project_path = os.path.abspath(os.path.dirname(__file__))

    root_path = project_path[:project_path.find("{}\\".format(PROJECT_NAME)) + len("{}\\".format(PROJECT_NAME))]

    #print('当前项目名称：{}\r\n当前项目根路径：{}'.format(PROJECT_NAME, root_path))

    return root_path

def make_out_file_sf(tarFile,data,fs,datatpye='PCM_16'):
    """

    """
    sf.write(tarFile,data,fs,datatpye)
def make_out_file(tarFile,data,fs,channel,datatpye=np.int16,databitnum=2):
    """

    """
    outData =np.ndarray([int(num*32767) for num in data])
    wavfile = wave.open(tarFile, 'wb')
    wavfile.setnchannels(channel)
    wavfile.setsampwidth(databitnum)
    wavfile.setframerate(fs)
    wavfile.writeframes(outData.tobytes())
    wavfile.close()

def get_ave_rms(data,fs,frameDuration=0.05,shiftduration=0.05):
    '''
    Parameters
    ----------
    data

    Returns
    -------
    '''
    frameLen = frameDuration * fs
    frameshift = shiftduration * fs
    nFrames = int((len(data)-frameLen)//frameshift)
    totalRms,cnt = 0,0
    maxRms,minRms = -199,199
    rms_list = []
    for a in range(nFrames):
        curRms = get_rms(data[int(a*frameshift):int(a*frameshift+frameLen)])
        if curRms > maxRms:
            maxRms = curRms
        if curRms < minRms:
            minRms = curRms
        totalRms += curRms
        cnt += 1
        rms_list.append(curRms)
    return totalRms/cnt,maxRms,minRms,maxRms-minRms,np.std(rms_list, ddof=1)

def get_std_rms(data,fs,frameDuration=0.05,shiftduration=0.05):
    '''
    Parameters
    ----------
    data

    Returns
    -------
    '''
    frameLen = frameDuration * fs
    frameshift = shiftduration * fs
    nFrames = len(data)//frameLen
    curRms = 0
    rms_list = []
    for a in range(nFrames):
        curRms = get_rms(data[a*frameLen:(a+1)*frameLen])
        rms_list.append(curRms)
    return np.std(rms_list, ddof=1)
def get_duration_above_specific_rms(data,fs,frameDuration=0.05,shiftduration=0.05):
    '''
    Parameters
    ----------
    data

    Returns
    -------
    '''
    frameLen = frameDuration * fs
    frameshift = shiftduration * fs
    nFrames = len(data)//frameLen
    threshold = -45
    maxcnt,validcnt = 0,0
    for a in range(nFrames):
        maxcnt += 1
        curRms = get_rms(data[a*frameLen:(a+1)*frameLen])
        if curRms > threshold:
            validcnt += 1

    return validcnt/maxcnt



def get_rms(records):
    '''
    Parameters
    ----------
    records

    Returns
    -------
    '''
    #return math.sqrt(sum([x * x for x in records])/len(records))
    if len(records) == 0:
        return -99.9
    rms = math.sqrt(sum([(x) * (x) for x in records])/len(records))
    dBrmsValue = 20*math.log10(rms + 1.0E-6)
    return dBrmsValue


def get_peak_rms(records):
    '''
    Parameters
    ----------
    records

    Returns
    -------
    '''
    #return math.sqrt(sum([x * x for x in records])/len(records))

    maxdata = max(records)
    maxRms = 20 * math.log10(maxdata + 1.0E-6)
    return maxRms

def get_max_rms(records,fs,frameDuration=0.05,shiftduration=0.05):
    '''
    Parameters
    ----------
    records

    Returns
    -------
    '''
    #return math.sqrt(sum([x * x for x in records])/len(records))
    frameLen = frameDuration * fs
    frameshift = shiftduration * fs
    nFrames = int((len(records) - frameLen) // frameshift)
    maxRms = -99
    for a in range(nFrames):
        curRms = get_rms(records[int(a*frameshift):int(a*frameshift+frameLen)])
        if curRms > maxRms:
            maxRms = curRms
    return maxRms


def get_min_rms(records,fs,frameDuration=0.05,shiftduration=0.05):
    '''
    Parameters
    ----------
    records

    Returns
    -------
    '''
    #return math.sqrt(sum([x * x for x in records])/len(records))
    frameLen = frameDuration * fs
    frameshift = shiftduration * fs
    nFrames = int((len(records) - frameLen) // frameshift)
    minrms = 100
    for a in range(nFrames):
        curRms = get_rms(records[int(a*frameshift):int(a*frameshift+frameLen)])
        if curRms < minrms:
            minrms = curRms
    return minrms

def get_one_channel_data(infile):
    """
    :return:
    """
    data, fs, chn = get_data_array(infile)
    if fs == 48000 and chn == 1:
        return data
    if chn != 1:
        data = np.array([data[n] for n in range(len(data)) if n % chn == 0]).astype(np.int16)
    return resample(data,fs,48000)

def resample(data,fs,tarfs,datatype=np.int16):
    """
    :return:
    """
    if fs == tarfs:
        return data
    new_signal = librosa.resample(data.astype(np.float32), fs, tarfs)
    # augmenter = Resample(min_sample_rate=4000, max_sample_rate=48000, p=1.0)
    # samples = augmenter(samples=data.astype(np.float32), sample_rate=tarfs)
    return new_signal.astype(datatype)

def get_file_duration(filename):
    """
    :param filename:
    :return:
    """
    f = wave.open(filename, "rb")
    # 读取格式信息
    # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    # 读取波形数据
    # 读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）
    f.close()
    return nframes/framerate/nchannels,framerate