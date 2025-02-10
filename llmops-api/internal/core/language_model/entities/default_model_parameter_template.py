

from .model_entity import  DefaultModelParameterName, ModelParameterType

# 默认模型参数模版，用于减少YAML的配置，参数以OpenAI的模型接口作为标准
DEFAULT_MODEL_PARAMETER_TEMPLATE = {
    # 温度模版默认参数
    DefaultModelParameterName.TEMPERATURE: {
        "label": "温度",
        "type": ModelParameterType.FLOAT,
        "help": "温度控制的随机性，较低的温度会导致较少的随机生成，随着温度接近零，较高的温度会导致更多随机内容被生成",
        "required": False,
        "default": 1.0,
        "min": 0.0,
        "max": 2.0,
        "precision": 2,
        "options": []
    },
    # top_p模版默认参数
    DefaultModelParameterName.TOP_P: {
        "label": "Top P",
        "type": ModelParameterType.FLOAT,
        "help": "通过核心采样控制多样性，0.5表示考虑了一半的所有可能性加权选项",
        "required": False,
        "default": 0.0,
        "min": -2.0,
        "max": 2.0,
        "precision": 2,
        "options": []
    },
    # 存在惩罚模版默认参数
    DefaultModelParameterName.PRESENCE_PENALTY: {
        "label": "存在惩罚",
        "type": ModelParameterType.FLOAT,
        "help": "对文本中已有的标记的对数概率施加惩罚，以减少重复",
        "required": False,
        "default": 0.0,
        "min": -2.0,
        "max": 2.0,
        "precision": 2,
        "options": []
    },
    # 频率惩罚模版默认参数
    DefaultModelParameterName.FREQUENCY_PENALTY: {
        "label": "频率惩罚",
        "type": ModelParameterType.FLOAT,
        "help": "对生成的标记的频率进行惩罚，以减少重复",
        "required": False,
        "default": 0.0,
        "min": -2.0,
        "max": 2.0,
        "precision": 2,
        "options": []
    },
    # 最大生成token模版默认参数
    DefaultModelParameterName.MAX_TOKENS: {
        "label": "最大标记",
        "type": ModelParameterType.INT,
        "help": "要生成的标记的最大数量",
        "required": False,
        "default": None,
        "min": 1,
        "max": 16384,
        "precision": 0,
        "options": []
    }
}