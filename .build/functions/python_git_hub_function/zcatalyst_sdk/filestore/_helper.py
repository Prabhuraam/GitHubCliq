from typing import Optional
from ..types import (
    ICatalystFile,
    ICatalystFolder,
    ICatalystGResponse,
    ICatalystProject,
    ICatalystSysUser
)


class ICatalystFolderDetails(ICatalystFolder):
    created_time: Optional[str]
    created_by: Optional[ICatalystSysUser]
    project_details: Optional[ICatalystProject]


class ICatalystFileDetails(ICatalystFile, ICatalystGResponse):
    pass
