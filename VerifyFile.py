import os
import sys
import hashlib


class FileGetDigest:
    '''该类利用 MD5 和 SHA1 算法生成文件的摘要
    '''

    def __init__(self, filename):
        self.filename = filename
        self.md5 = self.cal_md5()
        self.sha1 = self.cal_sha1()

    def cal_md5(self):
        '''生成文件的 MD5 摘要
        '''
        md5 = hashlib.md5()
        with open(self.filename, 'rb') as f:
            md5.update(f.read())
            return md5.hexdigest()

    def cal_sha1(self):
        '''生成文件的 SHA1 摘要
        '''
        sha1 = hashlib.sha1()
        with open(self.filename, 'rb') as f:
            sha1.update(f.read())
            return sha1.hexdigest()

    def compare_digest(self, digest):
        '''判断摘要是否与文件的摘要相同
        '''
        # 如果参数长度为 32 ，表示这是 MD5 摘要信息
        if len(digest) == 32:
            print('Identical:', self.md5 == digest)
        # 如果参数长度为 40 ，表示这是 SHA1 摘要信息
        elif len(digest) == 40:
            print('Identical:', self.sha1 == digest)
        # 否则，打印异常信息
        else:
            print('[Error] Invalid digest:', digest)


    def __call__(self):
        '''将类的实例变成可执行对象，打印摘要信息
        '''
        print('File Name:', self.filename)
        print('\tMD5:', self.md5)
        print('\tSHA1:', self.sha1)


def main():
    '''主函数，处理参数，执行核心功能
    '''

    # 如果除了脚本文件之外，只有一个参数
    # 那么该参数须是文件名，打印文件的摘要信息即可
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        # 如果参数文件存在
        if os.path.isfile(arg):
            # 调用 FileGetDigest 类创建实例，打印摘要信息
            fd = FileGetDigest(arg)
            fd()
        # 如果参数文件不存在，打印异常信息
        else:
            print('[Error] Invalid file name:', arg)

    # 如果除了脚本文件之外，有两个参数
    # 那么第一个参数须为文件名，第二个参数可能是文件名，也可能是摘要信息
    if len(sys.argv) == 3:
        arg1, arg2 = sys.argv[1:]
        # 如果第一个参数不是文件名，打印异常信息并退出程序
        if not os.path.isfile(arg1):
            print('[Error] Invalid file name:', arg1)
            sys.exit()
        # 如果第一个参数是文件名，创建实例
        fd1 = FileGetDigest(arg1)
        # 打印文件的摘要信息
        fd1()
        # 如果第二个参数不是文件名，那就是摘要信息
        if not os.path.isfile(arg2):
            # 比对摘要信息，然后退出程序
            fd1.compare_digest(arg2)
            sys.exit()
        # 如果第二个参数是文件名
        fd2 = FileGetDigest(arg2)
        # 打印文件的摘要信息
        fd2()
        # 比较两个实例的 SHA1 或 MD5 值
        print('Identical:', fd1.sha1 == fd2.sha1)


if __name__ == '__main__':
    main()
