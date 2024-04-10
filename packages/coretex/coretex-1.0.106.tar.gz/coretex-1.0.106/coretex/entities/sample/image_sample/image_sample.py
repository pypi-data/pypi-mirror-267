#     Copyright (C) 2023  Coretex LLC

#     This file is part of Coretex.ai

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Optional, Union, Any, Dict
from typing_extensions import Self
from pathlib import Path

import json

from .image_sample_data import AnnotatedImageSampleData
from .local_image_sample import LocalImageSample
from .image_format import ImageFormat
from ..network_sample import NetworkSample
from ...annotation import CoretexImageAnnotation
from ....networking import networkManager, NetworkRequestError


class ImageSample(NetworkSample[AnnotatedImageSampleData], LocalImageSample):

    """
        Represents the generic image sample\n
        Contains basic properties and functionality for all image sample classes\n
        The class has several methods that allow users to access and
        manipulate image data and annotations, as well as to create new image samples
    """

    def __init__(self) -> None:
        NetworkSample.__init__(self)

    @property
    def imagePath(self) -> Path:
        path = Path(self.path)

        for format in ImageFormat:
            imagePaths = list(path.glob(f"*.{format.extension}"))
            imagePaths = [path for path in imagePaths if not "thumbnail" in str(path)]

            if len(imagePaths) > 0:
                return Path(imagePaths[0])

        raise FileNotFoundError

    @property
    def annotationPath(self) -> Path:
        return Path(self.path) / "annotations.json"

    @property
    def metadataPath(self) -> Path:
        return Path(self.path) / "metadata.json"

    def saveAnnotation(self, coretexAnnotation: CoretexImageAnnotation) -> bool:
        # Only save annotation locally if it is downloaded
        if self.zipPath.exists() and self.path.exists():
            super().saveAnnotation(coretexAnnotation)

        parameters = {
            "id": self.id,
            "data": coretexAnnotation.encode()
        }

        response = networkManager.post("session/save-annotations", parameters)
        return not response.hasFailed()

    def saveMetadata(self, metadata: Dict[str, Any]) -> None:
        """
            Saves a json object as metadata for the sample

            Parameters
            ----------
            metadata : dict[str, Any]
                Json object containing sample metadata

            Raises
            ------
            NetworkRequestError -> if metadata upload failed
        """

        parameters = {
            "id": self.id,
            "data": metadata
        }

        response = networkManager.post("session/save-metadata", parameters)
        if response.hasFailed():
            raise NetworkRequestError(response, f"Failed to upload metadata for sample {self.name}")

    def loadMetadata(self) -> Dict[str, Any]:
        """
            Loads sample metadata into a dictionary

            Returns
            -------
            dict[str, Any] -> the metadata as a dict object

            Raises
            ------
            FileNotFoundError -> if metadata file is missing\n
            ValueError -> if json in the metadata file is list
        """

        if not self.metadataPath.exists():
            raise FileNotFoundError(f"Metadata file \"{self.metadataPath}\" was not found")

        with self.metadataPath.open("r") as metadataFile:
            metadata = json.load(metadataFile)
            if not isinstance(metadata, dict):
                raise ValueError(f"Metatada for sample \"{self.name}\" is a list. Expected dictionary")

            return metadata

    @classmethod
    def createImageSample(cls, datasetId: int, imagePath: Union[Path, str]) -> Optional[Self]:
        """
            Creates a new image sample with specified properties\n
            For creating custom sample, sample must be an image of supported format

            Parameters
            ----------
            datasetId : int
                id of dataset in which image sample will be created
            imagePath : Union[Path, str]
                path to the image sample

            Returns
            -------
            The created image sample object

            Example
            -------
            >>> from coretex import ImageSample
            \b
            >>> sample = ImageSample.createImageSample(1023, "path/to/file.jpeg")
            >>> if sample is None:
                    print("Failed to create image sample")
        """

        parameters = {
            "dataset_id": datasetId
        }

        return cls._createSample(parameters, imagePath)
