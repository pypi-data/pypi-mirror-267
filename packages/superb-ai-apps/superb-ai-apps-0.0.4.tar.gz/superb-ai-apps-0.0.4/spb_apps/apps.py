from typing import Dict, List, Tuple

from spb_label import sdk as spb_label

from spb_apps.curate.superb_curate import SuperbCurate
from spb_apps.label.superb_label import SuperbLabel
from spb_apps.utils.converter import convert_yolo_bbox
from spb_apps.utils.utils import read_info_from_zip_yolo


class SuperbApps:
    """
    This class manages interactions with Superb applications, specifically Label and Curate platforms.
    It provides functionalities to download images, upload images and annotations, change project contexts,
    and more, based on the specified platform.
    """

    def __init__(
        self,
        team_name: str,
        access_key: str,
        platform: str,
        dev: bool = False,
        project_id: str = "",
        project_name: str = "",
        dataset_name: str = "",
    ):
        """
        Initializes the SuperbApps instance with necessary details and sets up clients for the specified platform.

        Args:
            team_name (str): The name of the team.
            access_key (str): The access key for authentication.
            platform (str): The platform to initialize (either 'label' or 'curate').
            dev (bool, optional): Flag to indicate if this is a development instance. Defaults to False.
            project_id (str, optional): The ID of the project for labeling. Only required for 'label' platform. Defaults to "".
            project_name (str, optional): The name of the project for labeling. Only required for 'label' platform. Defaults to "".
            dataset_name (str, optional): The name of the dataset for Curate. Only required for 'curate' platform. Defaults to "".
        """
        self.team_name = team_name
        self.access_key = access_key
        platform = platform.lower()
        if platform == "label":
            self.client = SuperbLabel(
                team_name=team_name,
                access_key=access_key,
                project_id=project_id,
                project_name=project_name,
            )

            self.label_project_name = self.client.client._project.name
        if platform == "curate":
            self.client = SuperbCurate(
                team_name=team_name,
                access_key=access_key,
                dataset_name=dataset_name,
                is_dev=dev,
            )
            self.dataset_name = dataset_name
        self.platform = platform

    def download_image_by_key(self, data_key: str, path: str = None):
        """
        Downloads an image using its unique data key.

        Args:
            data_key (str): The unique identifier for the image.
            path (str, optional): The local file path to save the downloaded image. Defaults to None.
        """
        if self.platform == "label":
            _, label = self.client.get_labels(data_key=data_key)
            self.client.download_image(label=label[0], path=path)
        if self.platform == "curate":
            self.client.download_image(data_key=data_key, download_path=path)

    def download_image_by_filter(
        self,
        tags: list = [],
        data_key: str = "",
        status: list = [],
        path: str = None,
    ):
        """
        Downloads images by applying filters such as tags, data key, and status.

        Args:
            tags (list, optional): A list of tags to filter images. Defaults to [].
            data_key (str, optional): A specific data key to filter images. Defaults to "".
            status (list, optional): A list of statuses to filter images. Defaults to [].
            path (str, optional): The local file path to save the downloaded images. Defaults to None.
        """
        from concurrent.futures import ThreadPoolExecutor

        if self.platform == "label":

            def download(label):
                self.client.download_image(label=label, path=path)

            count, labels = self.client.get_labels(
                tags=tags, data_key=data_key, status=status
            )
            print(f"Downloading {count} data to {path}")
            if count > 50:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    executor.map(download, labels)
            else:
                for label in labels:
                    download(label)
        else:
            print("Curate does not support filters for downloading images.")

    def get_width_height(
        self, data_hanler: spb_label.DataHandle = None, data_key: str = ""
    ) -> Tuple[int, int]:
        """
        Retrieves the width and height of an image based on its data key.

        Args:
            data_hanler (spb_label.DataHandle, optional): The data handler object for 'label' platform. Defaults to None.
            data_key (str, optional): The unique identifier for the image for 'curate' platform. Defaults to "".

        Returns:
            Tuple[int, int]: A tuple containing the width and height of the image.
        """
        if self.platform == "label":
            if data_hanler is None:
                print(
                    "Label platform requires a data handler object from spb_label."
                )
                return
            return self.client.get_width_height(label=data_hanler)
        if self.platform == "curate":
            if data_key == "":
                print("Curate platform requires a data key.")
                return
            return self.client.get_width_height(data_key=data_key)

    def get_labels(
        self,
        data_key: str = "",
        tags: list = [],
        assignees: list = [],
        status: list = [],
        all: bool = False,
    ) -> Tuple[int, List]:
        """
        Retrieves labels based on filters or all labels if specified.

        Args:
            data_key (str, optional): A data key to filter labels. Defaults to "".
            tags (list, optional): A list of tags to filter labels. Defaults to [].
            assignees (list, optional): A list of assignees to filter labels. Defaults to [].
            status (list, optional): A list of statuses to filter labels. Defaults to [].
            all (bool, optional): If True, retrieves all labels ignoring other filters. Defaults to False.

        Returns:
            Tuple[int, List]: A tuple containing the count of labels and a list of labels.
        """
        count, labels = self.client.get_labels(
            data_key=data_key,
            tags=tags,
            assignees=assignees,
            status=status,
            all=all,
        )

        return count, labels

    def change_project(self, project_name: str):
        """
        Changes the project context for the label client.

        Args:
            project_name (str): The name of the project to switch to.
        """
        if self.platform == "label":
            self.client.client.set_project(name=project_name)
            self.label_project_name = self.client.client._project.name
        else:
            print("Curate platform does not support changing projects.")

    def get_label_interface(self) -> Dict:
        """
        Retrieves the label interface configuration for the 'label' platform.

        Returns:
            Dict: The label interface configuration, or prints a message if the platform is 'curate'.
        """
        if self.platform == "label":
            lb_interface = self.client.client.project.label_interface
            return lb_interface
        else:
            print(
                "Curate platform does not support label interface retrieval."
            )

    def make_bbox(self, class_name: str, annotation: list, data_key: str = ""):
        """
        Creates a bounding box based on the specified platform ('label' or 'curate').

        Args:
            class_name (str): The class name associated with the bounding box.
            annotation (list): A list containing the x, y coordinates, width, and height of the bounding box.
            data_key (str, optional): The unique identifier for the image. Required for 'curate' platform.

        Returns:
            The result of the bounding box setting operation, which varies by platform.
        """
        if self.platform == "label":
            return self.client.bbox_setting(
                class_name=class_name, annotation=annotation
            )
        if self.platform == "curate":
            if data_key == "":
                print("To make a Curate bbox, you must provide a data_key.")
                return
            return self.client.bbox_setting(
                data_key=data_key, class_name=class_name, annotation=annotation
            )

    def upload_images(self, images_path: str, dataset_name: str = ""):
        """
        Uploads images to the specified platform ('label' or 'curate').

        Args:
            images_path (str): The path to the images to be uploaded.
            dataset_name (str, optional): The name of the dataset to upload the images to. Required for 'label' platform.

        Returns:
            The result of the image upload operation, which varies by platform.
        """
        if self.platform == "label":
            if dataset_name == "":
                print(
                    "Must specify a dataset name when uploading to Label platform."
                )
                return
            return self.client.upload_image(images_path, dataset_name)
        if self.platform == "curate":
            return self.client.curate_upload_images(images_path)

    def upload_annotations(
        self, data_key: str, annotations: list, format: str, classes: list = ""
    ) -> str:
        """
        Uploads annotations to the specified platform ('label' or 'curate') based on the provided format.

        Args:
            data_key (str): The unique identifier for the image or dataset.
            annotations (list): A list of annotations to be uploaded.
            format (str): The format of the annotations ('yolo' supported).
            classes (list, optional): The classes associated with the annotations. Required if format is 'yolo'.

        Returns:
            str: The status of the upload operation ('Completed', 'Skipped', or 'Failed').
        """
        status = "Completed"
        if self.platform == "label":
            _, label = self.client.get_labels(data_key=data_key)
            if len(label) == 0:
                print(
                    f"[SKIPPED] Data key: {data_key}, does not exist in project {self.label_project_name}"
                )
                status = "Skipped"
                return status
            data_handler = label[0]
            if format == "yolo":
                if classes == "":
                    print(
                        "To upload yolo annotations, you must provide classes."
                    )
                    status = "Failed"
                    return status
                width, height = self.get_width_height(
                    data_handler=data_handler
                )
                converted_annotations = convert_yolo_bbox(
                    data_key, annotations, classes, width, height
                )
                if converted_annotations is not None:
                    self.client.upload_annotation(
                        data_handler, converted_annotations
                    )

        if self.platform == "curate":
            if format == "yolo":
                if classes == "":
                    print(
                        "To upload yolo annotations, you must provide classes."
                    )
                    status = "Failed"
                    return status
                bbox_annotation = []
                try:
                    width, height = self.get_width_height(data_key=data_key)
                except:
                    return "Skipped"
                converted_annotations = convert_yolo_bbox(
                    data_key, annotations, classes, width, height
                )
                if converted_annotations is not None:
                    for anno in converted_annotations:
                        bbox = self.client.bbox_setting(
                            data_key,
                            anno[0],
                            anno[1],
                        )
                        bbox_annotation.append(bbox)

                self.client.curate_upload_annotations(bbox_annotation)

        return status

    def build_label_interface(self, class_list: list, bbox: bool = True):
        """
        Builds the label interface for the 'label' platform based on the provided class list and bbox flag.

        Args:
            class_list (list): The list of classes to include in the label interface.
            bbox (bool, optional): Flag to indicate if bounding boxes should be included. Defaults to True.

        Returns:
            The result of the label interface building operation for 'label' platform, or prints a message for 'curate'.
        """
        if self.platform == "label":
            return self.client.build_label_interface_from_yolo(
                class_list, bbox
            )
        else:
            print(
                "Curate platform does not support building a Label Interface."
            )

    def download_image_by_slice(self, slice_name: str, download_path: str):
        """
        Downloads an image by its slice name to a specified path. This method is exclusive to the Curate platform.

        Args:
            slice_name (str): The name of the slice from which to download the image.
            download_path (str): The local file path where the downloaded image will be saved.
        """
        if self.platform == "curate":
            self.client.download_image_by_slice(
                slice_name=slice_name, download_path=download_path
            )
        else:
            print("Download by slice is only for Curate platform.")
