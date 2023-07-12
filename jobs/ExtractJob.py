from toolkit.kohya_model_util import load_models_from_stable_diffusion_checkpoint
from collections import OrderedDict
from typing import List

from jobs.process import BaseExtractProcess
from jobs import BaseJob

process_dict = {
    'locon': 'ExtractLoconProcess',
}


class ExtractJob(BaseJob):

    def __init__(self, config: OrderedDict):
        super().__init__(config)
        self.base_model_path = self.get_conf('base_model', required=True)
        self.base_model = None
        self.extract_model_path = self.get_conf('extract_model', required=True)
        self.extract_model = None
        self.output_folder = self.get_conf('output_folder', required=True)
        self.is_v2 = self.get_conf('is_v2', False)
        self.device = self.get_conf('device', 'cpu')

        # loads the processes from the config
        self.load_processes(process_dict)

    def run(self):
        super().run()
        # load models
        print(f"Loading models for extraction")
        print(f" - Loading base model: {self.base_model_path}")
        self.base_model = load_models_from_stable_diffusion_checkpoint(self.is_v2, self.base_model_path)

        print(f" - Loading extract model: {self.extract_model_path}")
        self.extract_model = load_models_from_stable_diffusion_checkpoint(self.is_v2, self.extract_model_path)

        print("")
        print(f"Running  {len(self.process)} process{'' if len(self.process) == 1 else 'es'}")

        for process in self.process:
            process.run()