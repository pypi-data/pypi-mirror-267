from bauplan._proto.runtime.apply_import_plan.v2 import aip_model_pb2 as _aip_model_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplyImportPlanRequest(_message.Message):
    __slots__ = ('code_intelligence_instructions', 'runner_instructions')
    CODE_INTELLIGENCE_INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    RUNNER_INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    code_intelligence_instructions: _aip_model_pb2.ApplyImportPlanCodeIntelligenceInstructions
    runner_instructions: _aip_model_pb2.ApplyImportPlanRunnerInstructions
    def __init__(
        self,
        code_intelligence_instructions: _Optional[
            _Union[_aip_model_pb2.ApplyImportPlanCodeIntelligenceInstructions, _Mapping]
        ] = ...,
        runner_instructions: _Optional[
            _Union[_aip_model_pb2.ApplyImportPlanRunnerInstructions, _Mapping]
        ] = ...,
    ) -> None: ...

class ApplyImportPlanResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
