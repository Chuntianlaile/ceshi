import argparse
import os
import sys
from chardet.universaldetector import UniversalDetector


# 创建 ArguemntParser 实例
parser = argparse.ArgumentParser(description='文本文件编码检测与转换')

# 使用实例的 add_argument 方法增加三个参数规则

# 'filename' 不带减号，表示该参数为位置参数，位置参数不带选项
# nargs 设置参数数量，'+' 表示参数数量为正整数，help 为参数说明
parser.add_argument('filenames', nargs='+', help='被检测或转换的文件名称')
# 带一个减号为短选项，带两个减号为长选项
# nargs='?' 表示参数数量为 1 或 0 
parser.add_argument('-e', '--encoding', nargs='?',
    help='''目标编码。支持的编码有：ASCII, (Default) UTF-8, UTF-16,
        UTF-32 (with a BOM), Big5, GB2312/GB18030, EUC-TW, EUC-JP, EUC-KR,
        HZ-GB-2312, ISO-2022-CN, ISO-2022-JP, ISO-2022-KR, ISO-8859-1,
        ISO-8859-2, ISO-8859-5, ISO-8859-7, ISO-8859-8, KOI8-R, SHIFT_JIS,
        MacCyrillic, IBM855, IBM866, windows-1250, windows-1251,
        windows-1252, windows-1253, windows-1255, TIS-620''')
parser.add_argument('-o', '--output', help='输出目录')

# 解析参数，得到 Namespace 对象
args = parser.parse_args()
# 输出目录不为空即视为开启转换
if args.output:
    # 检测用户提供的输出目录是否有效
    if not os.path.isdir(args.output):
        print('Invalid Directory: ' + args.output)
        sys.exit()
    else:
        if args.output[-1] != '/':
            args.output += '/'

# 实例化一个通用探测器，用于检测文件的编码格式
detector = UniversalDetector()
print('编码格式 (置信度) : 文件名字')
info = []
for filename in args.filenames:
    # 探测器在使用前先进行重置
    detector.reset()
    # 排除无效文件名
    if not os.path.isfile(filename):
        print('Invalid file:', filename)
        continue
    # 打开文件，使用探测器检测文件的编码格式
    with open(filename, 'rb') as f:
        for each in f:
            # 探测器读取数据并检测
            detector.feed(each)
            # 当文件的编码格式被确定后，探测器的属性 done 的值为 True 
            if detector.done:
                break
    # 关闭探测器
    detector.close()
    # 探测器的 result 属性是字典，从中获取文件的编码格式和置信度
    encoding = detector.result['encoding']
    if not encoding:
        encoding = 'Unknown'
    confidence = detector.result['confidence']
    if not confidence:
        confidence = 0.99
    print('{} {:>8} :'.format(encoding.rjust(8), '({}%)'.format(
            confidence*100)), filename)
    # 如果探测器检测到了文件的编码格式，而且置信度超过六成
    if (args.encoding and encoding != 'Unknown' and confidence >= 0.6 and
            encoding != args.encoding):
        output_path = args.output + os.path.basename(filename) \
                if args.output else filename
        # 打开被转换编码格式的文件
        # errors='replace' 表示如果出现解码异常的字符，使用问号代替
        with open(filename, encoding=encoding, errors='replace') as f:
            data = f.read()
        # 将文件内容以规定的编码格式写入文件
        with open(output_path, 'w', encoding=args.encoding, 
                errors='replace') as f:
            f.write(data)
        info.append('{} 文件的编码格式已经从 {} 转换为 {}'.format(filename, 
            encoding, args.encoding))

if info:
    print()
    for i in info:
        print(i)
