from typing import List, Union

from .code_generator import ConvertCodeGenerator
from .end_metadata_mapper import end_metadata_mapper, ImageDesc
from .knowledge_graph_construction import (
    get_knowledge_graph_constructor,
    MetadataValues,
    FactoriesCluster,
    ConversionForMetadataPair,
    Metadata,
)

_constructor = get_knowledge_graph_constructor()
_code_generator = ConvertCodeGenerator(_constructor.knowledge_graph)


def im2im(source_image, src_im_desc: ImageDesc, tgt_im_desc: ImageDesc):
    """
    To convert an image from one type to another.

    Args:
        source_image: the image you intend to convert.
        src_im_desc: provides a detailed description of the input image's current format and characteristics. This description is broken down into four key attributes:
            - **lib**: A string indicating the library associated with the image (e.g., 'numpy', 'PIL', 'torch').
            - **color_channel**: An optional attribute that specifies the color channel format of the image, such as 'gray', 'rgb', 'bgr', 'rgba', or 'graya'.
            - **image_dtype**: An optional attribute that defines the data type of the image pixels. including 'uint8', 'uint16', 'uint32', 'uint64',
                    'int8', 'int16', 'int32', 'int64',
                    'float32(0to1)', 'float32(-1to1)',
                    'float64(0to1)', 'float64(-1to1)',
                    'double(0to1)', 'double(-1to1)'.
            - **device**: An optional attribute that indicates the computing device ('cpu' or 'gpu') on which the image is stored or processed.
        tgt_im_desc: The same structure as the second parameter to specify the target image type.

    Returns: target image in the target format.
    """
    target_image_name = "target_image"
    code_str = im2im_code("source_image", src_im_desc, target_image_name, tgt_im_desc)
    exec(code_str)
    return locals()[target_image_name]


def im2im_code(
        source_var_name: str,
        source_image_desc: ImageDesc,
        target_var_name: str,
        target_image_desc: ImageDesc,
) -> Union[str, None]:
    """
    Generates Python code as a string that performs data conversion from a source variable to a target variable.

    Args:
        source_var_name (str): The name of the variable holding the source data.
        source_image_desc (ImageDesc): A dictionary containing description about the source image data.
            - `lib` (str): the library the image data comes from. Supported libraries are "numpy", "scikit-image", "opencv", "scipy", "matplotlib", "PIL", "torch", "kornia", "tensorflow".
            - `color_channel` (Optional[Literal['gray', 'rgb', 'bgr', 'rgba', 'graya']]): Description of color channels.
            - `image_dtype` (Optional[Literal['uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16', 'int32', 'int64', 'float32(0to1)', 'float32(-1to1)', 'float64(0to1)', 'float64(-1to1)', 'double(0to1)', 'double(-1to1)']])
            - `device` (Optional[Literal['cpu', 'gpu']]): Device where the data is processed or stored.
        target_var_name (str): The name of the variable that will store the result of the conversion.
        target_image_desc (ImageDesc): Metadata about the target data, structured similarly to source_metadata.

    Returns:
        str | None: A string containing the Python code necessary to perform the conversion, or None if conversion is not possible.

    Examples:
        >>> source_image_desc = {"lib": "numpy"}
        >>> target_image_desc = {"lib": "torch", "image_dtype": 'uint8'}
        >>> conversion_code = im2im_code("source_image", source_image_desc, "target_image", target_image_desc)
        >>> print(conversion_code)
        #  import torch
        #  image = torch.from_numpy(source_image)
        #  image = image.permute(2, 0, 1)
        #  target_image = torch.unsqueeze(image, 0)
    """

    source_metadata, target_metadata = end_metadata_mapper(
        source_image_desc, target_image_desc
    )
    return im2im_code_by_metadata(
        source_var_name, source_metadata, target_var_name, target_metadata
    )


def im2im_code_by_metadata(
        source_var_name: str,
        source_metadata: Metadata,
        target_var_name: str,
        target_metadata: Metadata,
) -> Union[str, None]:
    return _code_generator.get_conversion(
        source_var_name, source_metadata, target_var_name, target_metadata
    )


def im2im_path(source_image_desc: ImageDesc, target_image_desc: ImageDesc):
    source_metadata, target_metadata = end_metadata_mapper(
        source_image_desc, target_image_desc
    )
    return im2im_path_by_metadata(source_metadata, target_metadata)


def im2im_path_by_metadata(source_metadata: Metadata, target_metadata: Metadata):
    return _code_generator.get_convert_path(source_metadata, target_metadata)


def config_astar_goal_function(cpu_penalty: float, gpu_penalty: float,
                               include_time_cost: bool = False, test_img_size=(256, 256)):
    """
    We use A* to find the shortest path in the knowledge graph. The goal function is only step cost by default.
    You can use this function to set `cpu penalty`, `gpu penalty`  or enable `execution time cost` to the goal function.
    """
    _code_generator.config_astar_goal_function(cpu_penalty, gpu_penalty, include_time_cost, test_img_size)


def add_meta_values_for_image(new_metadata: MetadataValues):
    _constructor.add_metadata_values(new_metadata)
    _code_generator.knowledge_graph = _constructor.knowledge_graph


def add_edge_factory_cluster(factory_cluster: FactoriesCluster):
    _constructor.add_edge_factory_cluster(factory_cluster)
    _code_generator.knowledge_graph = _constructor.knowledge_graph


def add_conversion_for_metadata_pairs(
        pairs: Union[List[ConversionForMetadataPair], ConversionForMetadataPair]
):
    _constructor.add_conversion_for_metadata_pairs(pairs)
    _code_generator.knowledge_graph = _constructor.knowledge_graph
