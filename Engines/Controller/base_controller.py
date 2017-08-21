# -*- coding: utf-8 -*-

from Configs import user_agents
import random

"""所有controller的基础方法，如果需要使用该controller中的方法，则继承即可"""


def chooseagent():
    agent_list = user_agents.user_agent_list
    length = len(agent_list)
    rand = random.randint(0, length-1)
    return agent_list[rand]