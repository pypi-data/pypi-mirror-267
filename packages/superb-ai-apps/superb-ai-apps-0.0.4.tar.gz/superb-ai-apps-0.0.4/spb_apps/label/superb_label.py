import os
from io import BytesIO
from pathlib import Path
from typing import List, Optional, Tuple
from uuid import uuid4

import phy_credit
import requests
from PIL import Image
from spb_label import sdk as spb_label
from spb_label.exceptions import ParameterException
from spb_label.utils import SearchFilter


class SuperbLabel(object):
    def __init__(
        self,
        team_name: str,
        access_key: str,
        project_id: str = "",
        project_name: str = "",
    ):
        """
        Initialize the SuperbLabel class with necessary details for operation.

        Parameters:
        - team_name (str): The name of the team.
        - access_key (str): The access key for authentication.
        - project_id (str, optional): The ID of the project to be set for the client. Defaults to an empty string.
        - project_name (str, optional): The name of the project. Defaults to an empty string.
        """
        self.team_name = team_name
        self.client = spb_label.Client(
            team_name=team_name,
            access_key=access_key,
            project_id=project_id if project_id else None,
            project_name=project_name if project_name else None,
        )

    def download_export(
        self,
        input_path: str,
        export_id: str,
    ):
        """
        Download an export from the server to a local path.

        Parameters:
        - input_path (str): The local file path where the export will be saved.
        - export_id (str): The ID of the export to download.
        """
        print("[INFO] Checking for the export to be downloaded...")
        download_url = self.client.get_export(id=export_id).download_url
        r = requests.get(download_url)
        if r.status_code == 200:
            print("Saving export to local path")
            Path(input_path).parents[0].mkdir(parents=True, exist_ok=True)
            with open(input_path, "wb") as f:
                f.write(r.content)
        else:
            print(f"Failed to download the file. Status code: {r.status_code}")

    def get_labels(
        self,
        data_key: str = "",
        tags: list = [],
        assignees: list = [],
        status: list = [],
        all: bool = False,
    ) -> Tuple[int, List]:
        """
        Retrieve labels based on provided filters or all labels if specified.

        Parameters:
        - data_key (str, optional): Filter for a specific data key. Defaults to an empty string.
        - tags (list, optional): Filter for specific tags. Defaults to an empty list.
        - assignees (list, optional): Filter for specific assignees. Defaults to an empty list.
        - status (list, optional): Filter for specific status. Defaults to an empty list.
        - all (bool, optional): If True, ignores other filters and retrieves all labels. Defaults to False.

        Returns:
        Tuple[int, List]: A tuple containing the count of labels and a list of labels.
        """
        if all:
            next_cursor = None
            count, labels, next_cursor = self.client.get_labels(
                cursor=next_cursor
            )
        else:
            filter = SearchFilter(project=self.client.project)
            if data_key:
                filter.data_key_matches = data_key
            if tags:
                filter.tag_name_all = tags
            if assignees:
                filter.assignee_is_any_one_of = assignees
            if status:
                filter.status_is_any_one_of = status
            next_cursor = None
            count, labels, next_cursor = self.client.get_labels(
                filter=filter, cursor=next_cursor
            )

        return count, labels

    def download_image(self, label: spb_label.DataHandle, path: str = None):
        """
        Download an image associated with a label to a specified path.

        Parameters:
        - label (spb_label.DataHandle): The label data handle containing the image to download.
        - path (str, optional): The local file path where the image will be saved. If None, defaults to the label's default path.
        """
        label.download_image(download_to=path)

    def get_width_height(self, label: spb_label.DataHandle) -> Tuple[int, int]:
        """
        Download an image associated with a label, return its width and height, and delete the image.

        Parameters:
        - label (spb_label.DataHandle): The label data handle containing the image to download.

        Returns:
        Tuple[int, int]: A tuple containing the width and height of the downloaded image.
        """
        image_url = label.get_image_url()
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size

        return width, height

    def bbox_setting(self, class_name: str, annotation: list):
        """
        Create a bounding box setting for a given class name and annotation coordinates.

        Parameters:
        - class_name (str): The class name associated with the bounding box.
        - annotation (list): A list containing the coordinates of the bounding box in the order [x, y, width, height].

        Returns:
        A tuple containing the class name and a dictionary with the bounding box coordinates.
        """
        bbox = {
            "class_name": class_name,
            "annotation": {
                "coord": {
                    "x": annotation[0],
                    "y": annotation[1],
                    "width": annotation[2],
                    "height": annotation[3],
                }
            },
        }

        return bbox

    def upload_image(self, image_paths: list, dataset_name: str):
        """
        Upload images to a specified dataset.

        Parameters:
        - image_paths (list): A list of paths to the images to be uploaded.
        - dataset_name (str): The name of the dataset to upload the images to.
        """
        for path in image_paths:
            try:
                self.client.upload_image(path, dataset_name)
            except ParameterException as e:
                print(f"[ERROR]: Uploading went wrong: {e}")

    def upload_annotation(
        self, label: spb_label.DataHandle, annotations: list
    ):
        """
        Upload annotations for a given label.

        Parameters:
        - label (spb_label.DataHandle): The label to which the annotations will be added.
        - annotations (list): A list of annotations to be added to the label.
        """
        for anno in annotations:
            bbox = self.bbox_setting(anno[0], anno[1])
            label.add_object_label(
                class_name=bbox["class_name"], annotation=bbox["annotation"]
            )
        label.update_info()

    def build_label_interface(
        self,
        class_list: list,
        bbox: bool,
    ):
        """
        Build and update the label interface for the project based on the provided class list and bounding box flag.

        Parameters:
        - class_list (list): A list of class names to be included in the label interface.
        - bbox (bool): A flag indicating whether bounding boxes should be used.

        Returns:
        A tuple containing the updated label interface and a category map.
        """
        existing_label_interface = self.client.project.label_interface
        if existing_label_interface:
            label_interface = phy_credit.imageV2.LabelInterface.from_dict(
                existing_label_interface
            )
            object_detection = phy_credit.imageV2.ObjectDetectionDef.from_dict(
                existing_label_interface.get("object_detection")
            )
        else:
            label_interface = phy_credit.imageV2.LabelInterface.get_default()
            object_detection = (
                phy_credit.imageV2.ObjectDetectionDef.get_default()
            )

        category_map = dict()
        for class_name in class_list:
            bbox_suite_class_id = str(uuid4())
            bbox_suite_class_name = class_name

            object_detection.add_box(
                name=bbox_suite_class_name, id=bbox_suite_class_id
            )

        label_interface.set_object_detection(object_detection=object_detection)

        self.client.update_project(
            id=self.client.project.id,
            label_interface=label_interface.to_dict(),
        )
        return label_interface, category_map
