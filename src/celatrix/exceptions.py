"""Custom exceptions."""
class CelatrixError(Exception): pass
class DAGCycleError(CelatrixError): pass
class SchedulingError(CelatrixError): pass
class ResourceExhaustedError(CelatrixError): pass
class CheckpointError(CelatrixError): pass
