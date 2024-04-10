# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-03-29 17:10:22
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-02 18:27:12
from pydantic import BaseModel


class WhisperXSetting(BaseModel):
    engine: str
    language: str
