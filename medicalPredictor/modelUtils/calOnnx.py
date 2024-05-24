# coding: UTF-8
import onnxruntime as ort
import psutil
from .calUtils import pysoftmax
from monai.data import ImageDataset, DataLoader
from monai.transforms import EnsureChannelFirst, Compose, RandRotate90, Resize, ScaleIntensity
from monai.data import CSVSaver, DataLoader
import torch
from monai.data import ITKReader, PILReader

def cal_nii_ad(imgfile):
    val_transforms = Compose([ScaleIntensity(), EnsureChannelFirst(), Resize((96, 96, 96))])

    val_ds = ImageDataset(image_files=[imgfile], labels=[0], transform=val_transforms, reader=ITKReader)
    val_loader = DataLoader(val_ds, batch_size=1, num_workers=0, pin_memory=torch.cuda.is_available())
    for val_data in val_loader:
        val_images, val_labels = val_data[0], val_data[1]

    imgdata = str(val_images.as_tensor().cpu().tolist())
    pred, score = cal_img_onnx(imgdata, "model/alzheimer_clean/alzheimer_clean.onnx")
    return pred, score

def cal_img_onnx(imgdata, modelfile):

    sess_options = ort.SessionOptions()
    sess_options.execution_mode = ort.ExecutionMode.ORT_PARALLEL
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    sess_options.intra_op_num_threads = psutil.cpu_count(logical=True)
    modelonnx = ort.InferenceSession(modelfile, sess_options,
                                     ["CPUExecutionProvider", "CUDAExecutionProvider"])
    imgdata = eval(imgdata)
    val_outputs = modelonnx.run(None, {"input": imgdata})
    scorearr = pysoftmax(val_outputs[0][0])[0]
    pred = scorearr.argmax()
    score = scorearr[pred]
    return pred, score
