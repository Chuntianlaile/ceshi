import random

## 创建卡池
card_turple = ('武则天','嬴政','诸葛亮','宫本武藏','李白')
## 创建背包
package = [ ]

## 主程序
while 1:
    ## 接收用户的选择指令
    choose = int(input('''
    充值能让你变得更强！
    请选择指令：
    1. 抽卡
    2. 查看背包
    3. 整理背包
    4. 离开
    '''))

    ## 当用户输入 1 时，先询问抽卡次数
    if choose == 1:
        num = int(input('输入抽卡次数：'))
        ## 然后执行对应次数的抽卡程序
        for i in range(0,num):
            ## 生成 0 - 4 的随机整数，然后读取对应索引的卡
            n = random.randint(0,4)
            print('你抽到了: {}'.format(card_turple[n]))
            ## 放入背包
            package.append(card_turple[n])

        ## 完成抽完后，提示卡已存入背包    
        print('卡已存入背包')
        print('________________')

    ## 当用户输入 2，打印背包内容
    if choose == 2:
        ## 分背包有卡片和背包没卡片两种情况
        if len(package) == 0:
            print('背包暂无英雄，快去抽卡吧')
            print('________________')
        else:
            for i in package:
                print(i)
            print('________________')

    ## 当用户输入 3，整理背包内容，然后打印
    if choose == 3:
        ## 同样分有卡和没卡两种情况
        if len(package) == 0:
            print('背包暂无英雄，快去抽卡吧')
            print('________________')
        else:
            package.sort()
            for i in package:
                    print(i)
            print('________________')

    ## 当用户输入 4，退出程序
    if choose == 4:
        break
