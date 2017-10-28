#!d:/python32/python
import random
import re


class shuangseqiu():
    def __init__(self):
        self.quanzhong = [2.618, 1.618, 4.236]  # 权重，分别为一周统计数据，一月统计数据，一年统计数据与完全随机权重的比值，表示对最后选出的号码的影响力大小，此数据依据最伟大的黄金分割点制定。
        # self.quanzhong = [1,1,1]
        self.qishu = [4, 13, 153]  # 一周、一月、一年的彩票期数
        self.data_long = ['W', 'M', 'Y']  # 期数时间范围的长度表示
        self.fle = '123.txt'  # 打开彩票文件
        self.red_dict = {}  # 红球存储字典
        self.blue_dict = {}  # 篮球字典
        self.red_rate = {}  # 红球出现率字典
        self.blue_rate = {}  # 篮球出现率字典
        self.red_qz = []  # 红球权重
        self.blue_qz = []  # 篮球权重
        # 初始化存储字典
        for i in range(1, 34):
            self.__initdict__(i, self.red_dict)
            self.__initdict__(i, self.red_rate)
        for i in range(1, 17):
            self.__initdict__(i, self.blue_dict)
            self.__initdict__(i, self.blue_rate)
            # print(self.red_dict,self.blue_dict)

    def __initdict__(self, num, color_dict):
        color_dict[str(num)] = {}
        for x in range(len(self.data_long)):
            color_dict[str(num)][self.data_long[x]] = 0

    def __count__(self, num, color_dict, data_long):  # 统计一个号码出现的次数

        # print(num)
        color_dict[str(num)][data_long] += 1
        # print (num,data_long)

    def __countlst__(self, ball_lst, data_long):
        # print(ball_lst)
        # 年数据存储
        for i in range(6):
            self.__count__(ball_lst[i], self.red_dict, data_long)
        self.__count__(ball_lst[6], self.blue_dict, data_long)
        # print(self.red_dict)
        # print(self.blue_dict)

    def __readdata__(self):
        # 从文件读取彩票中奖纪录
        ball_file = open(self.fle, 'r')
        ball_lst = ball_file.readline()
        for i in range(1, self.qishu[2]):
            ball_lst = ball_file.readline().split()
            # print(ball_lst)
            # red = ball_list[5:11]
            # blue = ball_list[11:]
            # print(ball_lst)
            ball_lst = ball_lst[4:]
            if i <= self.qishu[0]:
                self.__countlst__(ball_lst, self.data_long[0])
            if i <= self.qishu[1]:
                self.__countlst__(ball_lst, self.data_long[1])
            self.__countlst__(ball_lst, self.data_long[2])
        ball_file.close()
        # print(self.red_dict)
        # print('------------------------')
        # print(self.blue_dict)

    def __rateone__(self, qishu, data_long):  # 根据统计的一段时间内(以data_long为依据)的出现次数计算1-33,1-16的出现几率
        # 计算总出现的次数
        redall = qishu * 6
        blueall = qishu * 1
        # 计算红球出现率
        for i in range(1, 34):
            self.red_rate[str(i)][data_long] = self.red_dict[str(i)][data_long] / redall
        # 计算篮球出现率
        for i in range(1, 17):
            self.blue_rate[str(i)][data_long] = self.blue_dict[str(i)][data_long] / blueall

    def __rate__(self):
        for i in range(len(self.data_long)):
            self.__rateone__(self.qishu[i], self.data_long[i])
            # print(self.red_rate)

    def __quanzhong__(self, num, color_rate):  # 计算num号码对应的权重
        value = (1 / len(color_rate) - color_rate[str(num)][self.data_long[0]]) * self.quanzhong[0] / sum(
            self.quanzhong)  # 一周出现概率高，那么后面，出现概率就会降
        value += (color_rate[str(num)][self.data_long[1]] - 1 / len(color_rate)) * self.quanzhong[1] / sum(
            self.quanzhong)
        value += (color_rate[str(num)][self.data_long[2]] - 1 / len(color_rate)) * self.quanzhong[2] / sum(
            self.quanzhong)
        return value

    def make_quanzhong(self):  # 生成整个权重的列表
        for i in range(1, 34):
            self.red_qz.append([self.__quanzhong__(i, self.red_rate), i])
        for i in range(1, 17):
            self.blue_qz.append([self.__quanzhong__(i, self.blue_rate), i])
            # print(self.red_qz)
            # print('--------------------------------------')
            # print(self.blue_qz)

    def init_data(self):  # 初始化读入数据、生成概率和权重数据结构
        self.__readdata__()
        self.__rate__()
        self.make_quanzhong()

    def _str_format(self, s):  # 格式化输入的字符串。形成数字列表
        a = re.compile('\d+')
        b = re.findall(a, s)
        return b

    def _find_qz(self, color_qz, num):  # 查找数字num的出现概率
        for i in range(0, 34):
            if color_qz[i][1] == num:
                return color_qz[i][0]

    def _suiji_gl(self):  # 计算随机概率
        sjgl = 1
        for x in range(28, 34):
            sjgl *= x
        sjgl = 1 / sjgl
        return sjgl * 1 / 16

    def gailv(self, s):  # 计算概率
        lst = self._str_format(s)
        # print(lst)
        lst = [int(x) for x in lst]
        # print(lst)
        gl = 1
        if not lst or len(lst) > 7 or len(lst) < 7 or max(lst) > 33 or min(lst) < 1:
            return None
        else:
            for x in lst[:7]:
                gl *= (1 + self._find_qz(self.red_qz, x))
        return gl * self._suiji_gl()

    def caipiao_random(self):  # 随机红篮球列表
        redball = sorted(random.sample(range(1, 34), 6))
        blueball = random.sample(range(1, 17), 1)
        return redball + blueball

    def print_random(self):  # 打印随机结果
        random_ball = self.caipiao_random()
        print('--------------------------------------------------')
        print('红球：', random_ball[:6], '篮球：', random_ball[6:7])
        print('--------------------------------------------------')

    def print_best_number(self):  # 输出中奖概率最高的号码
        print('根据规则选出的最可能中奖的号码如下:')
        print('--------------------------------------------------')
        print('红球：', sorted(list(x[1] for x in sorted(self.red_qz)[-6:])), '篮球：', sorted(self.blue_qz)[-1][1])
        print('--------------------------------------------------')

    def print_gl(self):
        print('输入格式为-> \"(1,9,13,21,28,32)(14)\"')
        c = input('请输入:')
        if not self.gailv(c):
            print('输入有误!')
            return
        print('--------------------------------------------------')
        print('         随机概率为：%0.10f%%' % (self._suiji_gl() * 100))
        print('         -------------------------')
        print('         自选概率为：%0.10f%%' % (self.gailv(c) * 100))
        print('--------------------------------------------------')


def print_all(shuangseqiu_obj):
    print('''
    |----------功能列表-------------|
    |--1:打印中奖率最高代码---------|
    |--2:打印随机号码---------------|
    |--3:自助选取号码，打印中奖概率-|
    |--q:退出-----------------------|
''')

    while True:
        a = input('功能选择:')
        if a == '1':
            shuangseqiu_obj.print_best_number()
        elif a == '2':
            shuangseqiu_obj.print_random()
        elif a == '3':
            shuangseqiu_obj.print_gl();
        elif a == 'q':
            break;
        else:
            print('输入有误')
    print('谢谢使用')


if __name__ == '__main__':
    b = shuangseqiu()
    b.init_data()
    print_all(b)