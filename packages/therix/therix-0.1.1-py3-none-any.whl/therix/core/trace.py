from therix_core.core.pipeline_component import PipelineComponent
from therix_core.entities.models import ConfigType

class Trace(PipelineComponent):
    def __init__(self, config):
        config['host'] = 'https://trace.dev.therix.ai'
        super().__init__(ConfigType.TRACE_DETAILS, 'LANGFUSE', config)