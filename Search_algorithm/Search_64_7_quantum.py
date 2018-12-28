import matplotlib.pyplot as plt
from pylab import mpl

from clsQubit import *
from gatelib import *

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

n = 7
M, N = 7, 64
R = int(math.floor(np.pi * np.sqrt(N / M) / 4))

q_vec = QubitVec(n)
init = np.zeros(128)
init[1] = 1
q_vec.init_state('typein', tuple(init))

init_super = product_all((('H', n, 0), ('H', n, 1), ('H', n, 2), ('H', n, 3), ('H', n, 4), ('H', n, 5), ('H', n, 6)))
grover_unit = product_all((('X', n, 6, (0, 1, 2, 3, 4, 5)), ('X', n, 6, (0, 1, 2, 3), (4,)),
                           ('X', n, 6, (0, 1, 2), (3,)),
                           ('H', n, 0), ('H', n, 1), ('H', n, 2), ('H', n, 3), ('H', n, 4), ('H', n, 5),
                           ('X', n, 0), ('X', n, 1), ('X', n, 2), ('X', n, 3), ('X', n, 4), ('X', n, 5),
                           ('H', n, 5), ('X', n, 5, (0, 1, 2, 3, 4)), ('H', n, 5),
                           ('X', n, 0), ('X', n, 1), ('X', n, 2), ('X', n, 3), ('X', n, 4), ('X', n, 5),
                           ('H', n, 0), ('H', n, 1), ('H', n, 2), ('H', n, 3), ('H', n, 4), ('H', n, 5)))
out_gate = product_all((('H', n, 6),))

iter_max = 30
pos_applytimes = list(np.zeros(iter_max))
for iter_times in range(0, iter_max):
    cir_U = init_super
    for k in range(0, iter_times):
        cir_U = grover_unit.dot(cir_U)
    cir_U = out_gate.dot(cir_U)

    q_vec.init_state('typein', tuple(init))
    q_vec.in_gate(cir_U)
    q_vec.calc_pos()
    pos_applytimes[iter_times] = \
        round(q_vec.calc_pos_state((1, 1, 1, 1, 1, 1, 1)) +
              q_vec.calc_pos_state((1, 1, 1, 1, 0, 1, 1)) +
              q_vec.calc_pos_state((1, 1, 1, 1, 0, 0, 1)) +
              q_vec.calc_pos_state((1, 1, 1, 0, 1, 1, 1)) +
              q_vec.calc_pos_state((1, 1, 1, 0, 1, 0, 1)) +
              q_vec.calc_pos_state((1, 1, 1, 0, 0, 1, 1)) +
              q_vec.calc_pos_state((1, 1, 1, 0, 0, 0, 1)), 4)

print(pos_applytimes)
theta = 2 * np.arccos(np.sqrt((N - M) / N))
x = np.linspace(0, iter_max, 1000)
y = (np.sin((x + 1 / 2) * theta)) ** 2
plt.plot(x, y, linestyle='--', label=u'近似估计')
plt.plot([i for i in range(0, iter_max)], pos_applytimes, 'ro', label=u'模拟数据')
plt.annotate('R = {}, p = {}'.format(R, pos_applytimes[R]),
             (R, pos_applytimes[R]), arrowprops=dict(arrowstyle='->'))
plt.ylabel(u"测得对应状态的概率")
plt.xlabel(u"grover迭代次数")
plt.title(u"M = {}, N = {}, R = {}".format(M, N, R))
plt.legend()
plt.show()
