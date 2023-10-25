from typing import Optional, TypedDict

ICatalystOCROptions = TypedDict('ICatalystOCROptions', {
    'language': Optional[str],
    'model_type': Optional[str]
}, total=False)

ICatalystBarCodeOptions = TypedDict('ICatalystBarCodeOptions', {
    'format': Optional[str]
})

ICatalystImageModerationOpts = TypedDict('ICatalystImageModerationOpt', {
    'mode': Optional[str]
})

ICatalystFaceAnalysisOptions = TypedDict('ICatalystFaceAnalysisOptions', {
    'mode': Optional[str],
    'emotion': Optional[bool],
    'age': Optional[bool],
    'gender': Optional[bool]
}, total=False)
