from zigzag.classes.stages import *
from zigzag.classes.cost_model.cost_model import CostModelEvaluation
from typing import Type
import re
from onnx import ModelProto

def get_hardware_performance_zigzag(
    workload,
    accelerator,
    mapping,
    opt="latency",
    dump_filename_pattern="outputs/{datetime}.json",
    pickle_filename="outputs/list_of_cmes.pickle",
    lpf_limit: int = 6,
    cost_model_class: Type = CostModelEvaluation,
):
    # Initialize the logger
    import logging as _logging

    _logging_level = _logging.INFO
    _logging_format = (
        "%(asctime)s - %(funcName)s +%(lineno)s - %(levelname)s - %(message)s"
    )
    _logging.basicConfig(level=_logging_level, format=_logging_format)

    # Sanity check on the optimization criterion
    if opt == "energy":
        opt_stage = MinimalEnergyStage
    elif opt == "latency":
        opt_stage = MinimalLatencyStage
    elif opt == "EDP":
        opt_stage = MinimalEDPStage
    else:
        raise NotImplementedError(
            "Optimization criterion 'opt' should be either 'energy' or 'latency' or 'EDP'."
        )

    # Check workload format and based on it select the correct workload parser stage
    try:
        if isinstance(workload, ModelProto) or workload.split(".")[-1] == "onnx":
            workload_parser_stage = ONNXModelParserStage
        else:
            workload_parser_stage = WorkloadParserStage
    except:
        workload_parser_stage = WorkloadParserStage

    mainstage = MainStage(
        [  # Initialize the MainStage as entry point
            workload_parser_stage,  # Parse the ONNX Model into the workload
            AcceleratorParserStage,  # Parse the accelerator module/passthrough given accelerator
            SimpleSaveStage,  # Save the summed CME energy and latency to a json
            PickleSaveStage,  # Save all received CMEs in a list to a pickle file
            SumStage,  # Sum up the received best CME across all layers of the workload
            WorkloadStage,  # Iterate through the different layers in the workload
            CompleteSaveStage,  # Save each processed layer to a json
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            SpatialMappingGeneratorStage,  # Generate multiple spatial mappings (SM)
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            LomaStage,  # Generate multiple temporal mappings (TM)
            # TemporalOrderingConversionStage,  # Based on the fixed temporal mapping order, generate one temporal mapping (TM)
            CostModelStage,  # Evaluate generated SM and TM through cost model
        ],
        accelerator=accelerator,  # required by AcceleratorParserStage
        workload=workload,  # required by workload_parser_stage
        mapping=mapping,  # required by workload_parser_stage
        dump_filename_pattern=dump_filename_pattern,  # output file save pattern
        pickle_filename=pickle_filename,  # filename for pickled list of cmes
        loma_lpf_limit=lpf_limit,  # required by LomaStage
        loma_show_progress_bar=True,
        # If we need access the same input data multiple times from the innermost memory level and the data size is smaller than the memory read bw,
        # take into account only one-time access cost (assume the data can stay at the output pins of the memory as long as it is needed).
        # By default, if the parameter is not defined, it will be set as False internally.
        access_same_data_considered_as_no_access=True,
        cost_model_class=cost_model_class,
    )

    # Launch the MainStage
    answers = mainstage.run()
    # Get CME from answer
    cmes = answers

    return cmes[0][0].energy_total, cmes[0][0].latency_total2, cmes

def get_hardware_performance_zigzag_imc(
    workload,
    accelerator,
    mapping,
    opt="latency",
    dump_filename_pattern="outputs/layer_?.json",
    pickle_filename="outputs/list_of_cmes.pickle",
):
    # Initialize the logger
    import logging as _logging

    _logging_level = _logging.INFO
    _logging_format = ( 
        "%(asctime)s - %(funcName)s +%(lineno)s - %(levelname)s - %(message)s"
    )   
    _logging.basicConfig(level=_logging_level, format=_logging_format)

    # Sanity check on the optimization criterion
    if opt == "energy":
        opt_stage = MinimalEnergyStage
    elif opt == "latency":
        opt_stage = MinimalLatencyStage
    elif opt == "EDP":
        opt_stage = MinimalEDPStage
    else:
        raise NotImplementedError(
            "Optimization criterion 'opt' should be either 'energy' or 'latency' or 'EDP'."
        )   

    # Check workload format and based on it select the correct workload parser stage
    try:
        if workload.split(".")[-1] == "onnx":
            workload_parser_stage = ONNXModelParserStage
        else:
            workload_parser_stage = WorkloadParserStage
    except:
        workload_parser_stage = WorkloadParserStage

    mainstage = MainStage(
        [  # Initialize the MainStage as entry point
            workload_parser_stage,  # Parse the ONNX Model into the workload
            AcceleratorParserStage,  # Parse the accelerator module/passthrough given accelerator
            SimpleSaveStage,  # Save the summed CME energy and latency to a json
            PickleSaveStage,  # Save all received CMEs in a list to a pickle file
            SumStage,  # Sum up the received best CME across all layers of the workload
            SearchUnusedMemoryStage,  # Detect unnecessary memory instances
            WorkloadStage,  # Iterate through the different layers in the workload
            RemoveUnusedMemoryStage,  # Remove unnecessary memory instances
            CompleteSaveStage,  # Save each processed layer to a json
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            SpatialMappingGeneratorStage,  # Generate multiple spatial mappings (SM)
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            LomaStage,  # Generate multiple temporal mappings (TM)
            # TemporalOrderingConversionStage,  # Based on the fixed temporal mapping order, generate one temporal mapping (TM)
            CostModelStage,  # Evaluate generated SM and TM through cost model
        ],
        accelerator=accelerator,  # required by AcceleratorParserStage
        workload=workload,  # required by workload_parser_stage
        mapping=mapping,  # required by workload_parser_stage
        dump_filename_pattern=dump_filename_pattern,  # output file save pattern
        pickle_filename=pickle_filename,  # filename for pickled list of cmes
        loma_lpf_limit=6,  # required by LomaStage
        enable_mix_spatial_mapping_generation=True,  # enable auto-generation of mix spatial mapping
        maximize_hardware_utilization=True, # only evaluate spatial mapping with top2 utilization (fast simulation)
        enable_weight_diagonal_mapping=True,  # required by SpatialMappingGeneratorStage
        loma_show_progress_bar=True,
        # If we need access the same input data multiple times from the innermost memory level and the data size is smaller than the memory read bw,
        # take into account only one-time access cost (assume the data can stay at the output pins of the memory as long as it is needed).
        # By default, if the parameter is not defined, it will be set as False internally.
        access_same_data_considered_as_no_access=True,
    )

    # Launch the MainStage
    answers = mainstage.run()
    # Get CME from answer
    cmes = answers

    return cmes[0][0].energy_total, cmes[0][0].latency_total2, cmes[0][0].tclk, cmes[0][0].area_total, cmes

def get_hardware_performance_zigzag_pe_array_scaling(
    workload,
    accelerator,
    mapping,
    pe_array_scaling,
    opt="latency",
    dump_filename_pattern="outputs/{datetime}.json",
    pickle_filename="outputs/list_of_cmes.pickle",
):
    # Initialize the logger
    import logging as _logging

    _logging_level = _logging.INFO
    _logging_format = (
        "%(asctime)s - %(funcName)s +%(lineno)s - %(levelname)s - %(message)s"
    )
    _logging.basicConfig(level=_logging_level, format=_logging_format)

    # Sanity check on the optimization criterion
    if opt == "energy":
        opt_stage = MinimalEnergyStage
    elif opt == "latency":
        opt_stage = MinimalLatencyStage
    elif opt == "EDP":
        opt_stage = MinimalEDPStage
    else:
        raise NotImplementedError(
            "Optimization criterion 'opt' should be either 'energy' or 'latency' or 'EDP'."
        )

    # Check workload format and based on it select the correct workload parser stage
    try:
        if workload.split(".")[-1] == "onnx":
            workload_parser_stage = ONNXModelParserStage
        else:
            workload_parser_stage = WorkloadParserStage
    except:
        workload_parser_stage = WorkloadParserStage

    mainstage = MainStage(
        [  # Initialize the MainStage as entry point
            workload_parser_stage,  # Parse the ONNX Model into the workload
            AcceleratorParserStage,  # Parse the accelerator module/passthrough given accelerator
            PEArrayScalingStage,  # Scale the PE array of the given accelerator
            SimpleSaveStage,  # Save the summed CME energy and latency to a json
            PickleSaveStage,  # Save all received CMEs in a list to a pickle file
            SumStage,  # Sum up the received best CME across all layers of the workload
            WorkloadStage,  # Iterate through the different layers in the workload
            CompleteSaveStage,  # Save each processed layer to a json
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            SpatialMappingGeneratorStage,  # Generate multiple spatial mappings (SM)
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            LomaStage,  # Generate multiple temporal mappings (TM)
            # TemporalOrderingConversionStage,  # Based on the fixed temporal mapping order, generate one temporal mapping (TM)
            CostModelStage,  # Evaluate generated SM and TM through cost model
        ],
        accelerator=accelerator,  # required by AcceleratorParserStage
        workload=workload,  # required by workload_parser_stage
        mapping=mapping,  # required by workload_parser_stage
        dump_filename_pattern=dump_filename_pattern,  # output file save pattern
        pickle_filename=pickle_filename,  # filename for pickled list of cmes
        loma_lpf_limit=6,  # required by LomaStage
        loma_show_progress_bar=True,
        # If we need access the same input data multiple times from the innermost memory level and the data size is smaller than the memory read bw,
        # take into account only one-time access cost (assume the data can stay at the output pins of the memory as long as it is needed).
        # By default, if the parameter is not defined, it will be set as False internally.
        access_same_data_considered_as_no_access=True,
        pe_array_scaling=pe_array_scaling,
    )

    # Launch the MainStage
    answers = mainstage.run()
    # Get CME from answer
    cmes = answers

    return cmes[0][0].energy_total, cmes[0][0].latency_total2, cmes


def get_hardware_performance_zigzag_without_unused_memory(
    workload,
    accelerator,
    mapping,
    opt="latency",
    dump_filename_pattern="outputs/{datetime}.json",
    pickle_filename="outputs/list_of_cmes.pickle",
):
    # Initialize the logger
    import logging as _logging

    _logging_level = _logging.INFO
    _logging_format = (
        "%(asctime)s - %(funcName)s +%(lineno)s - %(levelname)s - %(message)s"
    )
    _logging.basicConfig(level=_logging_level, format=_logging_format)

    # Sanity check on the optimization criterion
    if opt == "energy":
        opt_stage = MinimalEnergyStage
    elif opt == "latency":
        opt_stage = MinimalLatencyStage
    elif opt == "EDP":
        opt_stage = MinimalEDPStage
    else:
        raise NotImplementedError(
            "Optimization criterion 'opt' should be either 'energy' or 'latency' or 'EDP'."
        )

    # Check workload format and based on it select the correct workload parser stage
    try:
        if workload.split(".")[-1] == "onnx":
            workload_parser_stage = ONNXModelParserStage
        else:
            workload_parser_stage = WorkloadParserStage
    except:
        workload_parser_stage = WorkloadParserStage

    mainstage = MainStage(
        [  # Initialize the MainStage as entry point
            workload_parser_stage,  # Parse the ONNX Model into the workload
            AcceleratorParserStage,  # Parse the accelerator module/passthrough given accelerator
            SimpleSaveStage,  # Save the summed CME energy and latency to a json
            PickleSaveStage,  # Save all received CMEs in a list to a pickle file
            SumStage,  # Sum up the received best CME across all layers of the workload
            SearchUnusedMemoryStage,  # Search for unused memory instance
            WorkloadStage,  # Iterate through the different layers in the workload
            RemoveUnusedMemoryStage,  # Remove unused memory instance
            CompleteSaveStage,  # Save each processed layer to a json
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            SpatialMappingGeneratorStage,  # Generate multiple spatial mappings (SM)
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            LomaStage,  # Generate multiple temporal mappings (TM)
            # TemporalOrderingConversionStage,  # Based on the fixed temporal mapping order, generate one temporal mapping (TM)
            CostModelStage,  # Evaluate generated SM and TM through cost model
        ],
        accelerator=accelerator,  # required by AcceleratorParserStage
        workload=workload,  # required by workload_parser_stage
        mapping=mapping,  # required by workload_parser_stage
        dump_filename_pattern=dump_filename_pattern,  # output file save pattern
        pickle_filename=pickle_filename,  # filename for pickled list of cmes
        loma_lpf_limit=6,  # required by LomaStage
        loma_show_progress_bar=True,
        # If we need access the same input data multiple times from the innermost memory level and the data size is smaller than the memory read bw,
        # take into account only one-time access cost (assume the data can stay at the output pins of the memory as long as it is needed).
        # By default, if the parameter is not defined, it will be set as False internally.
        access_same_data_considered_as_no_access=True,
    )

    # Launch the MainStage
    answers = mainstage.run()
    # Get CME from answer
    cmes = answers

    return cmes[0][0].energy_total, cmes[0][0].latency_total2, cmes

def get_hardware_performance_zigzag_with_mix_spatial_mapping(
    workload,
    accelerator,
    mapping,
    opt="latency",
    dump_filename_pattern="outputs/{datetime}.json",
    pickle_filename="outputs/list_of_cmes.pickle",
):
    # Initialize the logger
    import logging as _logging

    _logging_level = _logging.INFO
    _logging_format = (
        "%(asctime)s - %(funcName)s +%(lineno)s - %(levelname)s - %(message)s"
    )
    _logging.basicConfig(level=_logging_level, format=_logging_format)

    # Sanity check on the optimization criterion
    if opt == "energy":
        opt_stage = MinimalEnergyStage
    elif opt == "latency":
        opt_stage = MinimalLatencyStage
    elif opt == "EDP":
        opt_stage = MinimalEDPStage
    else:
        raise NotImplementedError(
            "Optimization criterion 'opt' should be either 'energy' or 'latency' or 'EDP'."
        )

    # Check workload format and based on it select the correct workload parser stage
    try:
        if workload.split(".")[-1] == "onnx":
            workload_parser_stage = ONNXModelParserStage
        else:
            workload_parser_stage = WorkloadParserStage
    except:
        workload_parser_stage = WorkloadParserStage

    mainstage = MainStage(
        [  # Initialize the MainStage as entry point
            workload_parser_stage,  # Parse the ONNX Model into the workload
            AcceleratorParserStage,  # Parse the accelerator module/passthrough given accelerator
            SimpleSaveStage,  # Save the summed CME energy and latency to a json
            PickleSaveStage,  # Save all received CMEs in a list to a pickle file
            SumStage,  # Sum up the received best CME across all layers of the workload
            SearchUnusedMemoryStage,  # Search for unused memory instance
            WorkloadStage,  # Iterate through the different layers in the workload
            RemoveUnusedMemoryStage,  # Remove unused memory instance
            CompleteSaveStage,  # Save each processed layer to a json
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            SpatialMappingGeneratorStage,  # Generate multiple spatial mappings (SM)
            opt_stage,  # Reduce all CMEs, returning minimal energy/latency one
            LomaStage,  # Generate multiple temporal mappings (TM)
            # TemporalOrderingConversionStage,  # Based on the fixed temporal mapping order, generate one temporal mapping (TM)
            CostModelStage,  # Evaluate generated SM and TM through cost model
        ],
        accelerator=accelerator,  # required by AcceleratorParserStage
        workload=workload,  # required by workload_parser_stage
        mapping=mapping,  # required by workload_parser_stage
        dump_filename_pattern=dump_filename_pattern,  # output file save pattern
        pickle_filename=pickle_filename,  # filename for pickled list of cmes
        loma_lpf_limit=6,  # required by LomaStage
        loma_show_progress_bar=True,
        # If we need access the same input data multiple times from the innermost memory level and the data size is smaller than the memory read bw,
        # take into account only one-time access cost (assume the data can stay at the output pins of the memory as long as it is needed).
        # By default, if the parameter is not defined, it will be set as False internally.
        access_same_data_considered_as_no_access=True,
        enable_mix_spatial_mapping_generation=True,  # enable auto-generation of mix spatial mapping
        maximize_hardware_utilization=True, # only evaluate spatial mapping with highest hardware utilization (fast simulation speed)
    )

    # Launch the MainStage
    answers = mainstage.run()
    # Get CME from answer
    cmes = answers

    return cmes[0][0].energy_total, cmes[0][0].latency_total2, cmes

if __name__ == "__main__":
    workload = "zigzag/inputs/examples/workload/mobilenetv2.onnx"
    # workload = 'inputs.examples.workload.resnet18'
    accelerator = "zigzag.inputs.examples.hardware.TPU_like"
    mapping = "zigzag.inputs.examples.mapping.tpu_like"

    hw_name = accelerator.split(".")[-1]
    wl_name = re.split(r"/|\.", workload)[-1]
    if wl_name == "onnx":
        wl_name = re.split(r"/|\.", workload)[-2]
    experiment_id = f"{hw_name}-{wl_name}"
    pkl_name = f"{experiment_id}-saved_list_of_cmes"

    answer = get_hardware_performance_zigzag_pe_array_scaling(
        workload,
        accelerator,
        mapping,
        pe_array_scaling=2,
        opt="EDP",
        dump_filename_pattern=f"outputs/{experiment_id}-layer_?.json",
        pickle_filename=f"outputs/{pkl_name}.pickle",
    )
    # print(f'Answer = {answer}')

    # import pickle
    # path = f"outputs/{pkl_name}.pickle"
    # with open(path, 'rb') as f:
    #     data = pickle.load(f)
    # f.close()
