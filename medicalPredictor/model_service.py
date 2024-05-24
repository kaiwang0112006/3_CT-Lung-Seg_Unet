# coding: UTF-8

import os,sys
import json
from flask import Flask, render_template, url_for, request, jsonify
from flask import *
from modelUtils.model_conf import *
from modelUtils.calOnnx import *
import argparse
import logging, logging.config, yaml
import time

##########################################
## Options and defaults
##########################################
def getOptions():
    parser = argparse.ArgumentParser(description='python *.py [option]')
    parser.add_argument('--ip', dest='ip', help="ip", default='0.0.0.0')
    parser.add_argument('--port', dest='port', help="port", default=8080)
    parser.add_argument('--debug', dest='debug', help="if debug", default='True')
    args = parser.parse_args()

    return args


"""
Flask
"""
app = Flask(__name__,static_folder='static',template_folder='static/html')
"""
log
"""
logging.config.dictConfig(yaml.load(open(os.path.join(sys.path[0], 'logging.conf')),Loader=yaml.FullLoader))
logger = logging.getLogger()

@app.route('/alzheimer_clean_main' , methods=['GET'])
def alzheimer_clean_main():
    return render_template(r"alzheimer_clean.html")

@app.route('/upload_file' , methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save(r"/tmp/%s" % f.filename)
    return redirect(url_for('clean_predict', file_msg=f.filename))

@app.route('/clean_predict' , methods=['GET'])
def alzheimer_clean_predict():
    file_msg = request.args['file_msg']
    return render_template(r"clean_predict.html",file_msg=file_msg)

@app.route('/clean' , methods=['POST'])
def alzheimer_clean():
    """

    """
    st = time.time()
    # 解析请求
    requestjson = request.get_json(force=True, silent=True)
    logger.info(requestjson)

    # 需要data字段
    if "imgdata" not in requestjson:
        result = {'msg':"arg not in request",
                  'status':1,
                  'data':{},
                  "time_used":time.time()-st}
    else:
        imgdata = requestjson.get('imgdata', "")
        pred, probs_detail = cal_img_onnx(imgdata, modelfile=model_load["alzheimer_clean"])
        labelmap = {0:"AD",1:"NC"}
        result = {'msg': "success",
                  'status': 0,
                  'prediction': str(pred),
                  "predlabel": labelmap[pred],
                  'pvalue':str(probs_detail),
                  'version':"alzheimer_clean",
                  "time_used":time.time()-st}
        logger.info(result)
    resultstr = json.dumps(result, ensure_ascii=False)
    logger.debug("response:" + resultstr)
    return resultstr

@app.route('/predict_nii' , methods=["POST"])
def predict_nii():
    #filename = dict(request.form["filename"])
    filename = request.get_json(force=True, silent=True)["filename"]
    #filename = r"/tmp/%s" % filename
    print("filename: "+str(filename))
    pred, score = cal_nii_ad(r"/tmp/%s" % filename)
    return jsonify({"pred":str(pred), "score":str(score)})



if __name__ == "__main__":
    options = getOptions()
    print(options)
    check = {"False":False,"True":True}
    app.run(host=options.ip, port=options.port,debug=check[options.debug])
