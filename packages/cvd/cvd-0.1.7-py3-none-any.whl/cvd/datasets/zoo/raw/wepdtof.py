import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import List

import imagesize

from cvd.datasets.annotations.image_annotation import ImageAnnotation
from cvd.datasets.annotations.objects import TrackGTObjectBBox
from cvd.datasets.annotations.rbbox import RBBoxXYCenterWHA
from cvd.datasets.image_dataset import ImagesDataset
from cvd.datasets.meta import DatasetMeta, FileInfo, DatasetPart, DatasetType, ImageFileInfo


def import_dataset(main_data_folder: Path, image_set: DatasetPart) -> ImagesDataset:
    """
    The function allow import WAPDTOF dataset.
    @param main_data_folder: main path to wilder dataset
    @type main_data_folder: Path
    #param image_set: Determines which part of the dataset is imported.
    @type image_set: DatasetPart
    @return: Imported dataset in specific structure
    @rtype: ImagesDataset
    """
    if image_set.value == 'all':
        ann_folder = main_data_folder / 'annotations'
    else:
        raise Exception(f"Raw dataset doesn't contain {image_set.value} part")
    images_anns: List[ImageAnnotation] = []
    files_info: List[FileInfo] = []
    for ann_file in ann_folder.glob('*.json'):
        with open(ann_file, 'r') as fin:
            frame_anns = json.load(fin)
        frame_anns_dict = defaultdict(list)
        for ann in frame_anns['annotations']:
            frame_anns_dict[ann['image_id']].append(ann)
        frame_images_folder = main_data_folder / 'frames' / f'{ann_file.stem}'
        for frame_image_path in frame_images_folder.glob('*.jpg'):
            width, height = imagesize.get(str(frame_image_path))
            files_info.append(
                ImageFileInfo(
                    abs_path=frame_image_path,
                    unique_id=frame_image_path.stem,
                    width=width,
                    height=height
                )
            )
            objects = []
            for ann in frame_anns_dict[frame_image_path.stem]:
                objects.append(
                    TrackGTObjectBBox(
                        bbox=RBBoxXYCenterWHA(
                            x_center=ann['bbox'][0],
                            y_center=ann['bbox'][1],
                            width=ann['bbox'][2],
                            height=ann['bbox'][3],
                            angle=ann['bbox'][4] if ann['bbox'][4] > 0 else ann['bbox'][4]+180
                        ),
                        label='person',
                        track_id=ann['person_id']
                    )
                )
            images_anns.append(
                ImageAnnotation(objects=objects)
            )
    cepdof_dataset = ImagesDataset(
        DatasetMeta(
            name='WEPDTOF',
            version='1.0.0',
            description="WEPDTOF has been produced at the Visual Information Processing (VIP) "
                        "Laboratory at Boston University. WEPDTOF consists of 16 clips from "
                        "14 YouTube videos, each recorded in a different scene, "
                        "with 1 to 35 people per frame and 188 person identities consistently "
                        "labeled across time. WEPDTOF has more than 10 times the number of "
                        "distinct people, approximately 3 times the maximum number "
                        "of people per frame, and double the number of scenes. "
                        "https://vip.bu.edu/projects/vsns/cossy/datasets/wepdtof/",
            part=image_set,
            dstype=DatasetType.IMAGE
        )
    )
    for file_info, ann in zip(files_info, images_anns):
        cepdof_dataset.add_item(file_info, ann)
    return cepdof_dataset
