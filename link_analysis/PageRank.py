# -*- coding: utf-8 -*-


"""
page rank算法是通过海量的网页间链接关系分析出每个网页的重要性。
假设：
    1、数量假设：如果一个页面节点接收到的其他页面指向的入链数量越多，那么这个页面就越重要。
    2、质量假设：指向页面的入链质量不同。质量越高的页面会通过链接向其他页面传递更多的权重。
算法过程：
    随机初始化页面的权重  ->  迭代更新页面的pr值  ->  直到达到稳定态
优化：
    1、随机性修正：有些网页没有出链，最终导致所有的权重聚集在这些无出链的网页上（悬挂网页）
        针对悬挂网页，用户有一定概率随机选取一个网页进行访问。
        S = H + ea^T/N (其中，H是原本的转移矩阵，e是全1的向量，a是指示函数，表明是否是悬挂网页，N是所有网页的数目)
    2、素性修正：用户不会完全受当前网页所限，他们会在每一步都有一个小于1的几率α访问当前网页所提供的链接，同时却也有一个几率1-α不受那些链接所限，
    随机访问互联网上的任何一个网站。
        G = αS + (1-α)ee^T/N
ref：
    https://guisu.blog.csdn.net/article/details/7996185
    https://www.changhai.org/articles/technology/misc/google_math.php
    https://zhuanlan.zhihu.com/p/35005949
"""

from pygraph.classes.digraph import digraph


class PRIteration:
    __doc__ = '''计算一张图中的PR值'''

    def __init__(self, dg):
        self.damping_factor = 0.85  # 阻尼系数，即a
        self.max_iterations = 100   # 最大迭代次数
        self.min_delta = 0.00000001    # 确定迭代是否结束的参数

        self.graph = dg

    def page_rank(self):
        # 针对没有出链的页面添加到所有的页面的出链
        for node in self.graph.nodes():
            if len(self.graph.neighbors(node)) == 0:
                for node2 in self.graph.nodes():
                    digraph.add_edge(self.graph, (node, node2))

        nodes = self.graph.nodes()
        graph_size = len(nodes)

        if graph_size == 0:
            return {}

        page_rank = dict.fromkeys(nodes, 1.0 / graph_size)  # 给每个节点赋予初始PR值
        damping_value = (1 - self.damping_factor) / graph_size
        mode = 'max_iter'
        for it in range(self.max_iterations):
            change = 0
            for node in nodes:
                PR = 0
                for incident_page in self.graph.incidents(node):
                    PR += self.damping_factor * (page_rank[incident_page] / len(self.graph.neighbors(incident_page)))
                PR += damping_value
                change += abs(PR - page_rank[node])
                page_rank[node] = PR
            print('{}th iteration'.format(it + 1))
            print('page_rank:\t', page_rank)

            if change < self.min_delta:
                mode = 'min_delta'
                break
        print('finished with', mode)
        print('The best page:\t', max(page_rank.items(), key=lambda x: x[1]))


def main():
    dg = digraph()
    dg.add_nodes(["A", "B", "C", "D", "E"])
    dg.add_edge(("A", "B"))
    dg.add_edge(("A", "C"))
    dg.add_edge(("A", "D"))
    dg.add_edge(("B", "D"))
    dg.add_edge(("C", "E"))
    dg.add_edge(("D", "E"))
    dg.add_edge(("B", "E"))
    dg.add_edge(("E", "A"))
    pr = PRIteration(dg)
    pr.page_rank()


if __name__ == "__main__":
    main()
