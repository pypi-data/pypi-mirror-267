# -*- coding: utf-8 -*-
# @Author: Vivian Li 
# @Date:   2024-03-29 17:10:22
# @Last Modified by:   Vivian Li 
# @Last Modified time: 2024-04-02 18:26:20
from typing import Dict, Optional

from gailbot.engineManager.engine.engine import Engine
from gailbot.engineManager.engine.engineProvider import EngineProvider
from gailbot.engineManager.engine.watson import Watson
from gailbot.engineManager.engine.watson.watsonSetting import WatsonSetting


class WatsonProvider(EngineProvider):

    @staticmethod
    def load(name, data: Dict[str, str]) -> Optional[EngineProvider]:
        try:
            engine = WatsonProvider(name, data)
            assert engine.data.engine.lower() == "watson"
            return engine
        except Exception as e:
            return None

    def is_cpu_intensive(self) -> bool:
        return False

    def __init__(self, name, data: Dict[str, str]):
        self.data: WatsonSetting = WatsonSetting(**data)
        self.name = name
        Watson.validate_api(apikey=self.data.apikey, region=self.data.region)

    def make_engine(self) -> Engine:
        return Watson(self.data)
