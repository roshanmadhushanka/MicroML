import h2o
import os

def save_model(path, model):
    '''
    Save h2o model pojo

    :param path: location
    :param model: h2o model
    :return: None
    '''
    h2o.init()
    id = model.model_id
    path += "/" + id + "/"

    if not os.path.exists(path):
        os.mkdir(path)

    model.download_pojo(path, get_genmodel_jar=True)

    gen_model_path = path + "h2o-genmodel.jar"
    model_path = path + id + ".java"
    os.system("javac -cp " + gen_model_path +" -J-Xmx2g -J-XX:MaxPermSize=128m " + model_path)
    os.remove(gen_model_path)