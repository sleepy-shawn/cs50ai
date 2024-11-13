# PROJECT CONCLUSION

*This is my reflection of project codes in reverse order.*

1. **Attention**
   引入transformer, Numpy, tensorflow, 深度学习入门；
   需要配置http；
   tokenizer的输出结果为字典，index后转为numpy处理；
   注意力得分转灰度；
   enumerate函数；
   网络外用numpy；

2. **parser**
   string.lower();
   char.isalpha();
   parse基本原理；

3. **traffic**
   基本视觉处理模型；
   os.listdir 与 os.join操作处理目录，
   cv2.imread读取文件;
   cv2.resize调整大小；
   列表转np.array后分测试集和训练集；
   先compile后fit;
   model用顺序网络；
   keras.layers.Conv2D卷积，relu激活，3色通道
   池化层用最大池化；
   展开后128全连接，relu激活，dropout正则化；
   最后输出层，softmax激活，输出label，
   优化，评估，损失函数都用分类方法；

4. **nim**
   针对state, action建立q_value字典，有reward时更新；
   >>> Q(s, a) <- old value estimate + alpha * (new value estimate - old value estimate)；
   
    公式是核心，旧Q + 更新
    更新需要学习率
    新值用当前奖励和未来最佳奖励确定 需要y作比率
    未来最佳奖励即4种move的最佳；
    引入随机避免过贪；

5. **shopping**
   csv.reader和csv.dictReader
   float(row[])
   map[row[]]
   sum, zip, list comprehension 用于计算sensitivity and specificity

6. **pagerank**
   基础值 + 引用值构成page score
   迭代收敛和sample两种方式
   sample根据概率分布不断random choice 加分 最后归一
   迭代算法为遍历各个网页 根据引用到自身的网页的引用情况加分 最后根据收敛情况return

7. **heredity**
   经典贝叶斯网络；
   考虑所有情况概率相加；
   构建联合概率分布后归一，代码极为繁琐；

8. **crossword**
   最难的project
   一元consistency + arc consistency分别考虑
   arc consistency用revise完成；
   ac3用队列完成全部domain的arc consistency
   基本consistency考虑 word独立，长度正确，不重合， 作为backtrack基础；
   backtrack用最大度，最小剩余，最小影响来对赋值排序；
   联合ac3求解；

9. **knights**
   最简单proj and, not, or, implication加入knowledge， model_check求解，无脑遍历

10. **minesweeper**
    第二难proj
    sentence作为knowledge单元包括标记和已知
    ai作为代理，基本操作是标记safe和mine,做出move，
    难点在于update_all_cells
    以及每次add新的knowledge都要update， 做出的推断还要update， 还要及时清理

11. **tictactoe**
    入门proj;
    注意gamestate的copy；
    游戏获胜和玩家操作都很基础；
    核心是mini-max算法；
    相互递归+剪枝 超级震撼！

12. **degree**
    广度优先搜索；
    路径保存用指针；
    neighbours即同一部电影的角色，较为入门


***总结：没有引导文档和骨架代码，难如登天，但是在这些帮助之下完成了很多惊人的成就**。***



