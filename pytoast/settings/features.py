import os
import re
from pytoast.settings.scenario import Scenario

RESERVED_KEYWORDS = re.compile('^(?P<keyword>(given|when|then|and))(\s+)(?P<sentence>(.*))$',
                               re.IGNORECASE)


class Features(object):

    def __init__(self):
        self.scenarios = []

    def parse_file(self, feature_file_path):
        # io.FileIO.readlines()
        with open(feature_file_path) as f:
            feature_content_lines = f.readlines()
            current_scenario = None
            tags = None

            for line in feature_content_lines:
                content = line.strip()
                # print('content: {}'.format(content))
                if not content:
                    continue
                    current_scenario = None
                    tags = None
                elif content.lower().strip().find('@') == 0:
                    tags = [tag.strip()
                            for tag in content.split(' ') if tag.strip()]
                elif content.lower().find('scenario:') == 0:
                    scenario_name = content.split(':')[1].strip()
                    current_scenario = Scenario(scenario_name, tags)
                    self.scenarios.append(current_scenario)
                else:
                    found_search = RESERVED_KEYWORDS.search(content)
                    step_line = found_search.groupdict()
                    keyword = step_line.get('keyword').lower()
                    sentence = step_line.get('sentence')

                    current_scenario.steps.append((keyword, sentence))
