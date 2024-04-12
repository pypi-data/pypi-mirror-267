"""
字符串处理工具
"""
import re
from correct.logger.logger import Logger
from correct.tools.min_edit_distance import edit_distance

logger = Logger('correct.tools.str_tools.py')


def split_to_paragraphs(text):
    """
    将字符串分割为连续的中文段落、英文段落和字符段落
    :param text: 要分开的字符串，例如："我是谁？？niubility she is! 好好好！"
    :return: 例如：['我是谁', '？？', 'niubility', ' ', 'she', ' ', 'is', '! ', '好好好', '！']
    """
    paragraphs = []
    current_paragraph = ''
    current_type = None

    for char in text:
        # 判断字符类型：中文、英文、特殊字符（包括空格）
        if '\u4e00' <= char <= '\u9fff':
            char_type = 'ch'
        elif char.isalpha():
            char_type = 'en'
        else:
            char_type = 'spc_char'

        # 如果当前段落为空，或者当前字符类型与上一个字符类型相同，则将字符添加到当前段落中
        if not current_paragraph or char_type == current_type:
            current_paragraph += char
        else:
            # 如果当前字符类型与上一个字符类型不同，则将当前段落添加到列表中，并重新开始一个新段落
            paragraphs.append(current_paragraph)
            current_paragraph = char

        current_type = char_type

    # 将最后一个段落添加到列表中
    if current_paragraph:
        paragraphs.append(current_paragraph)

    return paragraphs


def split_list(lst):
    """
    一个列表，任意元素的类型可能是以下三种情况：纯中文、纯特殊字符、纯英文，把这个列表的每个元素做处理并合成一个新列表，处理过程规则如下：
    如果元素是纯中文或纯字符，拆分为单个文字或字符；如果元素是纯英文，保持原样
    :param lst: 例如：['我是谁', '？？', 'niubility', ' ', 'she', ' ', 'is', '! ', '好好好', '！']
    :return: 例如：['我', '是', '谁', '？', '？', 'niubility', ' ', 'she', ' ', 'is', '! ', '好', '好', '好', '！']
    """
    # 定义正则表达式来匹配纯中文、纯特殊字符和纯英文
    pattern_chinese = re.compile(r'^[\u4e00-\u9fff]+$')
    pattern_special = re.compile(r'^[^\w]+$')  # 匹配非字母数字的字符
    pattern_english = re.compile(r'^[a-zA-Z]+$')

    # 初始化新列表
    new_list = []

    # 遍历列表中的每个元素
    for item in lst:
        # 检查元素是否匹配纯中文模式
        if pattern_chinese.match(item):
            # 如果是纯中文，拆分为单个文字
            new_list.extend(list(item))
            # 检查元素是否匹配纯特殊字符模式
        elif pattern_special.match(item):
            # 如果是纯特殊字符，拆分为单个字符
            new_list.extend(list(item))
            # 检查元素是否匹配纯英文模式
        elif pattern_english.match(item):
            # 如果是纯英文，保持原样
            new_list.append(item)
        else:
            # 如果元素不符合上述任何模式，记录日志并保持原样
            logger.warning(
                f"[split_list]文本段未符合纯中文、纯英文、纯特殊字符中的任意一种情况，将保持原样计入结果列表。文本段内容：{item}")
            new_list.append(item)

    return new_list


def clean_space_for_list(lst):
    """
    如果列表存在某段连续的多个元素为纯空格，则对该段只保留一个单空格元素
    :param lst: 如['a', ' ', '   ', 'b', ' ', ' ', 'c']
    :return: 如['a', ' ', 'b', ' ', 'c']
    """
    cleaned_lst = []  # 用于存储处理后的列表
    whitespace_encountered = False  # 用于标记是否遇到了连续的纯空格元素

    for item in lst:  # 遍历输入列表中的每个元素
        if item.strip() == "":  # 如果当前元素是纯空格
            if not whitespace_encountered:  # 如果之前未遇到过连续的纯空格元素
                cleaned_lst.append(" ")  # 将一个空格元素添加到处理后的列表中
                whitespace_encountered = True  # 更新标记为已遇到连续的纯空格元素
        else:
            cleaned_lst.append(item.strip())  # 如果当前元素不是纯空格，则将其去除首尾空格后添加到处理后的列表中
            whitespace_encountered = False  # 更新标记为未遇到连续的纯空格元素

    return cleaned_lst  # 返回处理后的列表


def similarity(word1: str, word2: str, insertion_cost=1, deletion_cost=1, substitution_cost=1):
    f"""
    基于动态规划计算{word1}和{word2}的最小编辑距离
    :param word1: 字符串1
    :param word2: 字符串2
    :param insertion_cost: 最小编辑距离操作中插入操作权重
    :param deletion_cost: 最小编辑距离操作中删除操作权重
    :param substitution_cost: 最小编辑距离操作中替换操作权重
    :return: 相似度分值。0-1，越高越相似
    """
    # 去除首尾空字符
    word1 = word1.strip()
    word2 = word2.strip()

    # 先把两个字符串各自分割为两个列表。处理规则：中文和特殊字符一律分割为单个字符，英文按空格分割为单词
    list1 = split_list(split_to_paragraphs(word1))
    list2 = split_list(split_to_paragraphs(word2))

    # 去除多余的空格元素
    list1 = clean_space_for_list(list1)
    list2 = clean_space_for_list(list2)

    # 最大长度
    len_list1 = len(list1)
    len_list2 = len(list2)
    # list1和list2的长度如果为1，尝试将这个长度置为其唯一元素的长度（应对英语多选题）
    if len_list1 == 1 and len_list2 == 1:
        len_list1 = len(str(list1[0]))
        len_list2 = len(str(list2[0]))
        max_len = min(len_list1, len_list2)
    else:
        max_len = max(len_list1, len_list2)

    if max_len == 0:
        return 1.0

    # 最小编辑距离
    min_edit_distance = edit_distance(list1, list2, insertion_cost, deletion_cost, substitution_cost)

    # 如果权重不同，可能导致少数情况下max_len < min_edit_distance，这种情况人为做等值处理以便后续计算
    if max_len < min_edit_distance:
        max_len = min_edit_distance

    # 结果归1化
    similarity_score = 1 - min_edit_distance / max_len
    return similarity_score
