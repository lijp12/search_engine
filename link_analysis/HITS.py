# -*- coding: utf-8 -*-


"""
HITS算法基于query召回的主题相关的文档进行排序。
涉及两个概念：
    1、authority页面（权威页面）：与某个领域或主题相关的高质量网页。
    2、hub页面（枢纽页面）：包含了很多指向高质量"authority"页面链接的网页。
假设：
    1、一个好的authority页面会被很多好的hub页面指向；
    2、一个好的hub页面会指向很多好的authority页面。
算法过程：
    根集合 ->  扩展集合base（与根集合有链接的页面集合）  ->  计算base集合中元素的hub值和authority值
ref：
    https://blog.csdn.net/hguisu/article/details/8013489
"""

from pygraph.classes.digraph import digraph


class HITSIterator:
    __doc__ = '''计算一张图中的hub，authority值'''

    def __init__(self, dg):
        self.max_iterations = 100   # 最大迭代次数
        self.min_delta = 0.0001     # 确定迭代是否结束的参数
        self.graph = dg

        self.hub = {}
        self.authority = {}
        for node in self.graph.nodes():
            self.hub[node] = 1
            self.authority[node] = 1

    def hits(self):
        """
        计算每个node的hub，authority值
        :return:
        """
        if not self.graph:
            return
        mode = 'max_iter'
        for it in range(self.max_iterations):
            change = 0.0   # 统计每轮该变量
            norm = 0     # 标准化系数
            tmp = {}
            # 计算authority值
            tmp = self.authority.copy()
            for node in self.graph.nodes():
                self.authority[node] = 0
                for incident_page in self.graph.incidents(node):    # 所有入链的节点
                    self.authority[node] += self.hub[incident_page]
                norm += pow(self.authority[node], 2)

            # authority标准化
            for node in self.graph.nodes():
                self.authority[node] /= norm
                change += abs(self.authority[node] - tmp[node])

            # 计算hub值
            norm = 0
            tmp = self.hub.copy()
            for node in self.graph.nodes():
                self.hub[node] = 0
                for neighbor_page in self.graph.neighbors(node):
                    self.hub[node] += self.authority[neighbor_page]
                norm += pow(self.hub[node], 2)

            # hub标准化
            for node in self.graph.nodes():
                self.hub[node] /= norm
                change += abs(self.hub[node] - tmp[node])

            print('{}th iteration:'.format(it+1))
            print('authority:\t', self.authority)
            print('hub:\t', self.hub)

            if change < self.min_delta:
                mode = 'min_delta'
                break
        print('finished with', mode)
        print('The best authority page:\t', max(self.authority.items(), key=lambda x: x[1]))
        print('The best hub page:\t', max(self.hub.items(), key=lambda x: x[1]))


def main():
    dg = digraph()
    dg.add_nodes(["A", "B", "C", "D", "E"])
    dg.add_edge(("A", "C"))
    dg.add_edge(("A", "D"))
    dg.add_edge(("B", "D"))
    dg.add_edge(("C", "E"))
    dg.add_edge(("D", "E"))
    dg.add_edge(("B", "E"))
    dg.add_edge(("E", "A"))
    hits = HITSIterator(dg)
    hits.hits()


if __name__ == "__main__":
    main()
