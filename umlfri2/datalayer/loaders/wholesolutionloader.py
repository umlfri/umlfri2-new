from uuid import UUID

import lxml.etree

from umlfri2.types.version import Version
from .projectloader import ProjectLoader
from ..constants import FRIP2_SOLUTION_FILE, FRIP2_PROJECT_FILE, FRIP2_VERSION_FILE, MODEL_SAVE_VERSION
from .solutioninfoloader import SolutionInfoLoader
from umlfri2.model import Solution


class WholeSolutionLoader:
    def __init__(self, storage, ruler, addon_manager):
        self.__storage = storage
        self.__ruler = ruler
        self.__addon_manager = addon_manager
    
    def load(self):
        solution_info = SolutionInfoLoader(lxml.etree.parse(self.__storage.open(FRIP2_SOLUTION_FILE)).getroot()).load()
        
        if self.__storage.exists(FRIP2_VERSION_FILE):
            save_version = Version(self.__storage.read_string(FRIP2_VERSION_FILE))
        else:
            save_version = Version("2.0")
        
        if not save_version.is_compatible_with(MODEL_SAVE_VERSION):
            raise Exception("File is created with uncompatible version of UML .FRI")
        
        solution = Solution(save_id=UUID(solution_info.id))
        
        for project in solution_info.projects:
            project_xml = lxml.etree.parse(self.__storage.open(FRIP2_PROJECT_FILE.format(project.id))).getroot()
            solution.add_project(ProjectLoader(project_xml, self.__ruler, self.__addon_manager, save_version).load())
        
        return solution
