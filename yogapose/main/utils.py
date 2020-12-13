from pathlib import Path
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from yogapose import mail

from fastai.vision.all import *

def get_pose_name(folder_name):
    """Returns a name for the pose in lower case given the folder name of the pose
    
    Parameters:
    folder_name (str): Name of folder in original dataset 
    
    Preconditions:
    Parameter folder_name contains 'asana' or 'pose'
    
    Postconditions:
    A unique name in EN or SK (in that order) is returned in lower case
    
    """
    # Split on "_or_"
    substring_list = folder_name.split(sep='_or_')
    # Get substring containing "pose" else "asana"
    en_name = [s.replace("_"," ") for s in substring_list if 'pose' in s.lower()]
    sk_name = [s.replace("_"," ") for s in substring_list if 'asana' in s.lower()]
    
    return (en_name + sk_name)[0].lower()

def predict_picture(form_picture, foldername='profile_pics', output_size=(125,125)):
    """ Save picture, resize, overwrite and the predict name and score"""
    random_hex = secrets.token_hex(8)
    f_ext = str(Path(form_picture.filename).suffix)
    picture_fn = random_hex + f_ext
    picture_path = Path(current_app.root_path).joinpath('static').joinpath(foldername).joinpath(picture_fn)

    # Needs to be re-worked: saving and overwriting!
    i = Image.open(form_picture)
    i.save(picture_path)
    img = PILImage(PILImage.create(picture_path))
    rsz = Resize(output_size, method=ResizeMethod.Crop)
    img = rsz(img, split_idx=1)
    img.save(picture_path)

    # Needs to be re-worked: looks ugly!
    path = Path(current_app.root_path).joinpath('pkls')
    def get_x(r): return path/'data'/r['fn_col']
    def get_y(r): return [r['label']]
    import __main__
    __main__.get_x = get_x
    __main__.get_y = get_y
    learn_inf = load_learner( path.joinpath('y82-resnet18-multi.pkl') )

    pred,pred_idx,probs = learn_inf.predict(img)

    score = list(probs[pred_idx]) or [0]
    score = int(round(float(score[0]),2)*100)

    try:
        name = string.capwords(get_pose_name(pred[0]))
    except:
        name = 'No pose'
    return picture_fn, score, name

