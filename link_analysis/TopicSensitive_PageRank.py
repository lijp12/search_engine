# -*- coding: utf-8 -*-


"""
Topic-Sensitive PageRank算法是针对PageRank算法的主题无关性问题提出的折中方案。（理想方案是为每个用户维护一套专用向量，即个性化）
    大致做法：预定义几个类别，然后为每个类单独维护一个向量，然后利用这些类别去关联用户的话题倾向，然后根据话题倾向去排序结果。
算法流程：
    1）确定话题类别：16个大类别
    2）网页topic归属：将每个页面归入最合适的topic
    3）分topic计算PageRank向量
        G = αS + (1-α)ee^T/N    =>    G = αS + (1-α)ss^T/|s|
        其中，对于某个topic，如果某网页k属于该topic，则s中第k个元素为1，否则为0；其中｜s｜为s中1的个数。
    4）在线相似度计算
        确定用户查询的主题倾向，一般为在各个主题上的兴趣概率，然后拿到每个网页在各个topic下的PR值，对应求和即得该网页与用户查询的相似度。
ref:
    https://guisu.blog.csdn.net/article/details/8005192
"""


def main():
    pass


if __name__ == "__main__":
    main()
