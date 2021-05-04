### Bloom Filter

application:

当我们进行大成本查询数据，比如说硬盘I/O的时候， 加一层bloom filter，能快速地过滤掉大部分不存在的查询，而如果出现误判，再继续在下层的数据结构里进行深度查询。能够节省大量时间。

approximation：
$$
\lim_{n\rightarrow-\infty}(1+\frac{1}{n})^n = e\\
(1-\frac{1}{m})^{kn} = ((1+\frac{1}{-m})^{-m})^{-\frac{kn}{m}} \approx e^{-\frac{kn}{m}}\text{ when }m\rightarrow \infty
$$

minimization:

The accurate optimized k is 
$$
k = -\frac{\ln2}{n\ln(1-\frac{1}{m})}
$$
The accurate minimized p is
$$
p = 2^{\frac{\ln2}{n\ln(1-\frac{1}{m})}}
$$
or 
$$
\ln p = \frac{(\ln2)^2}{n\ln(1-\frac{1}{m})}
$$
The accurate m is 
$$
m = \frac{1}{1-2^{\frac{\ln2}{n\ln p}}}
$$

### 最小哈希

计算两个集合A和B的相似程度时，我们没必要先把$A\cap B$算出来 再把$A\cup B$算出来 然后求$\frac{|A\cap B|}{|A\cup B|}$

我们可以在$A\cup B$里随机采样 取到$A\cap B$内点的概率就是Jaccard measure$\frac{|A\cap B|}{|A\cup B|}$

设采样的随机变量为$X$ $X = 1$代表取到了$A\cap B$内点， 0为没取到，根据大数定理采样的平均值会趋于jaccard measure

但是随机采样这件事是比较难的 我们用minhash函数来代替随机采样 hash完了取最小值

一种minhash函数代表一次采样 这里应该要求是单射

所以一种求measure的方法就是用k个minhash计算k次 如果$h(A) = h(B)$就代表$h(A\cup B)$这个在$A\cup B$里随机采样的数就在$A\cap B$里，因为$h(A\cup B) = min\{h(A),h(B)\}$, 且当$h(A) = h(B)$时 $h(A) = h(B) = h(A\cap B)$ 但是这个太耗时间

另一种方法就是取一种hash结果的前k个 这个期望和取k次是一样的 （displacement和without displacement期望相同）所以是unbiased的
$$
\hat J = \frac{|h_k(A\cup B)\cap h_k(A)\cap h_k(B)|}{k}
$$
其中$h_k(A\cup B)$就是A，B minhash结果的前k个（显然）

后面的并就是计算随机取出来的元素是不是在$A\cap B$里

这个方法可以省下大量的空间 因为我储存A交并B的哈希表会异常大 但是这里我只需要k个元素就能够对比

但是对于时间的节省我并不是很懂。



对于两个元素来说 求交并至少需要|A|+|B|的时间 

优化就是先建一个B的哈希表，用A在B里查找元素 如果元素存在则对$|A\cap B|$计数 如果不存在则对$|A\backslash B|$计数，$|A\backslash B|+|B| = |A\cup B|$. 这种方法的空间复杂度是$O(|B|)$， 时间复杂度是$O(|A|+|B|)$，具体的操作数大致是hash一遍B，再hash一遍A，A在每次遍历都要常数时间判断和计数，所以大致是$h|B|+h|A|+c|A|$

而minhash的空间复杂度是$O(1)$，即常数复杂度，占有空间是$2k$，几乎可忽略。时间复杂度也是$O(|A|+|B|)$，算法是记录k个数及其最大值 hash集合，当当前值小于k个数的最大值时替换。这样下来对于A而言 需要hash一遍 每次都需要常数时间判断和替换，那么总的时间大致是$(h+c)(|B|+|A|)$ 好像比原本的时间还慢



**但是到多个文档对比就不同了**

对于**普通办法** 涉及多个文档时，比如说三个文档，最优的办法就是先建B的hash表 用A和C遍历一遍 求出$|A\cup B|,|C\cup B|,|A\cap B|,|C\cap B|$，再用A或者C建hash表，重复同样的操作

那么这样空间复杂度就是$O(|B|+|C|)$或者是$O(|B|+|A|)$，而时间复杂度虽然是$O(|A|+|B|+|C|)$但是事实上大致需要
$$
h|B|+h|A|+h|C|+c|A|+c|C|+h|A|+h|C|+c|C| = h|B|+2h(|A|+|C|)+c|A|+2c|C|
$$
 的时间



而对于**minhash**，总时间仍然是$(h+c)(|A|+|B|+|C|)$，肯定是小于前者的（前者遍历了5遍 后者遍历了3遍），空间上仍然使$O(1)$，占有空间大致是$3k$，远小于前者

这时候minhash做数字哈希签名的优点就体现了出来 对于多个文档的对比，该方法既大大降低了空间复杂度，也有效降低了空间复杂度。

