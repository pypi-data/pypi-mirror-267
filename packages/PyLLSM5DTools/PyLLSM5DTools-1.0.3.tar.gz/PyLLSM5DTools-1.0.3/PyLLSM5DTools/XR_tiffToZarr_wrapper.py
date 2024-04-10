import os
import subprocess


def XR_tiffToZarr_wrapper(tiffFullpaths, **kwargs):
    function_name = "XR_tiffToZarr_wrapper"
    XR_tiffToZarr_wrapper_dict = {
        "zarrPathstr": [kwargs.get("zarrPathstr", "zarr"), "char"],
        "locIds": [kwargs.get("locIds", []), "numericScalar"],
        "blockSize": [kwargs.get("blockSize", [500,500,250]), "numericArr"],
        "shardSize": [kwargs.get("shardSize", []), "numericArr"],
        "flippedTile": [kwargs.get("flippedTile", []), "logical"],
        "resample": [kwargs.get("resample", []), "numericArr"],
        "partialFile": [kwargs.get("partialFile", False), "logical"],
        "ChannelPatterns": [kwargs.get("ChannelPatterns", ['tif']), "cell"],
        "InputBbox": [kwargs.get("InputBbox", []), "numericArr"],
        "tileOutBbox": [kwargs.get("tileOutBbox", []), "numericArr"],
        "processFunPath": [kwargs.get("processFunPath", ), "cell"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "bigData": [kwargs.get("bigData", True), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 1), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "maxTrialNum": [kwargs.get("maxTrialNum", 3), "numericScalar"],
        "unitWaitTime": [kwargs.get("unitWaitTime", 30), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
    tiffFullpathsString = "{" + ",".join(f"'{item}'" for item in tiffFullpaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{tiffFullpathsString}\" "
    
    for key, value in XR_tiffToZarr_wrapper_dict.items():
        if value[1] == "char":
            if not value[0]:
                continue
            cmdString += f"\"{key}\" \"{value[0]}\" "
        elif value[1] == "cell":
            if not value[0]:
                continue
            cellString = "{" + ",".join(f"'{item}'" for item in value[0]) + "}"
            cmdString += f"\"{key}\" \"{cellString}\" "
        elif value[1] == "logicalArr":
            logicalArrString = "[" + ",".join(str(item) for item in value[0]) + "]"
            cmdString += f"\"{key}\" \"{str(logicalArrString).lower()}\" "
        elif value[1] == "logical":
            cmdString += f"\"{key}\" {str(value[0]).lower()} "
        elif value[1] == "numericArr":
            if not value[0]:
                continue
            numericArrString = "[" + ",".join(str(item) for item in value[0]) + "]"
            cmdString += f"\"{key}\" \"{numericArrString}\" "
        elif value[1] == "numericScalar":
            if type(value[0]) is list:
                if not value[0]:
                    continue
                else:
                    value[0] = value[0][0]
            cmdString += f"\"{key}\" {value[0]} "
        else:
            continue
    process = subprocess.Popen(cmdString, shell=True)
    process.wait()
    