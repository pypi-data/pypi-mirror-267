"""
对比笔迹和答案进行批改
"""

from correct.tools.str_tools import similarity
from correct.tools.constants import constants


def correct(params: dict):
    """
    对笔迹和答案做对比，得到批阅结果
    :param params:  成功对齐的结果
        [
            {
                // 标注数据点
                "point": (343.77, 443.43),
                // 标准答案
                "answer": "A",
                // 小题id
                "id": 13,
                // 匹配上的ocr识别内容
                "ocr_text": "A"
            },
            ...
        ]
    :return: 批阅结果
        {
            'success': [
                {
                    // 标注数据中点的坐标
                    "mark_location":{
                        "x":109,
                        "y":218
                    },
                    // 对应ocr识别内容
                    "ocr_text":"C6",
                    // 标准答案
                    "answer":"C",
                    // 匹配率。0-1，值越大认为越正确
                    "match_rate":"0.5806",
                    // 小题id
                    "sub_id":3570,
                    // 小题所属大题id
                    "parent_id": 15
                }
            ]
        }

    """

    if not params:
        return []
    return {
        'success': [
            {
                'mark_location': {
                    "x": ele['point'][0],
                    "y": ele['point'][1]
                },
                'ocr_text': ele['ocr_text'],
                'answer': ele['answer'],
                # 考虑到实际场景，编辑距离操作中的替换操作给的惩罚比插入和编辑大一些
                'match_rate': similarity(ele['answer'], ele['ocr_text'], constants.NUM_ONE, constants.NUM_ONE,
                                         constants.NUM_ONE),
                'sub_id': ele['id'],
                'parent_id': ele['parent_id'],
            } for ele in params
        ]
    }
