import os
import sys
import getopt
import markdown
from bs4 import BeautifulSoup


class ArgsParse:
    '''命令行参数解析类
    '''

    # 参数说明文档
    options_explain = '''Options:
        -h, --help  参数说明
        -f          被处理的 Markdown 文件
        -S          美化页面的 CSS 文件
        -d          转换成 HTML 文件后，新文件所在目录路径
        -F          转换成 HTML 文件后，新文件的文件名'''
        

    def __init__(self):
        # 选项有“短选项”和“长选项”两种
        # 短选项格式：一个减号一个字母；长选项格式：俩减号多个字母
        # getopt.getopt 方法有仨参数：要处理的对象列表、短选项组、长选项组
        # 短选项组为字符串，若选项有参数，后面加冒号
        # 长选项组为列表，若选项有参数，后面加等号
        # 该方法返回值为二元元组，元组中每个元素都是列表
        # 一个是选项解析结果，另一个是其余参数
        options, _ = getopt.getopt(sys.argv[1:], 'hf:d:S:F:', ['help'])
        # options 是列表，列表中每个元素都是二元元组，将其转换为字典
        self.options_dict = (dict(options))
        # 如果选项中有 -h 或 --help ，打印参数说明文档并结束程序
        if '-h' in self.options_dict or '--help' in self.options_dict:
            print(self.options_explain)
            sys.exit()
        # 调用参数处理函数，将各个参数赋值给相应的属性
        self.args_parse()

    def args_parse(self):
        '''参数处理函数，从解析后的选项字典中读取各个文件名
        '''
        self.markdown_file = self.options_dict.get('-f')
        self.css_file = self.options_dict.get('-S')
        self.html_file_dir = self.options_dict.get('-d')
        self.html_file = self.options_dict.get('-F')


class Markdown2Html:
    '''将 Markdown 文档转换为 HTML 文档并存储
    '''

    # HTML 文档的默认 head 标签
    head_tag = '<head><meta charset="utf-8" /></head>'

    def __init__(self, css_file=None):
        ''' 初始化方法，处理未来向 HTML 文档中添加的 head 标签
        '''
        if css_file:
            with open(css_file) as f:
                data = f.read()
            self.head_tag = (self.head_tag[:-7] + 
                    '<style type="text/css">{}</style>'.format(data) +
                    self.head_tag[-7:])

    def switch(self):
        '''核心方法，将 Markdown 文本转换为 HTML 文本并保存
        '''
        # 读取 Markdown 文件内容
        with open(args.markdown_file) as f:
            markdown_text = f.read()
        # 将 Markdown 文件内容转换为 HTML 文本
        # 参数 output_format 指定转换格式
        value = markdown.markdown(markdown_text, output_format='html5')
        # 为 HTML 文本添加 head 标签
        html_raw = self.head_tag + value
        # 使用 bs4 模块美化文本
        html_beautiful = BeautifulSoup(html_raw, 'html5lib').prettify()
        # 处理存储 HTML 文件的目录
        if args.html_file_dir[-1] != '/':
            args.html_file_dir += '/'
        # 处理 HTML 文件名
        if not args.html_file:
            args.html_file = os.path.splitext(
                    os.path.basename(args.markdown_file))[0] + '.html'
        # 存储 HTML 文本的路径
        html_file_route = args.html_file_dir + args.html_file
        # 将 HTML 文本存入文件
        with open(html_file_route, 'w') as f:
            f.write(html_beautiful)


if __name__ == '__main__':
    args = ArgsParse()
    markdown2html = Markdown2Html(args.css_file)
    markdown2html.switch()
