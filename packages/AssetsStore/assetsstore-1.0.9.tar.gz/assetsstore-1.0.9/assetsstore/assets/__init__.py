from .assets import FileAssets
from .s3 import S3Files
from .server import ServerFiles
from .local import LocalFiles
from .azr import AzureFiles
from .minio import MinioFiles

__all__ = [
    "FileAssets",
    "S3Files",
    "ServerFiles",
    "LocalFiles",
    "AzureFiles",
    "MinioFiles",
]
