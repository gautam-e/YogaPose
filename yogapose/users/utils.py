from pathlib import Path
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from yogapose import mail
from fastai.vision.all import *
import piexif

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


def predict_picture(form_picture, foldername='profile_pics', output_size=(224,224)):
    """ Make a random name for the given image, resize it, save it 
    and predict pose name and score
    """
    
    # Make a random name and construct a valid Path with it
    random_hex = secrets.token_hex(8)
    f_ext = str(Path(form_picture.filename).suffix)
    picture_fn = random_hex + f_ext
    picture_path = Path(current_app.root_path).joinpath('static').joinpath(foldername).joinpath(picture_fn)

    # Read as image
    img = Image.open(form_picture.stream)
    exif_data = img.info.get("exif")
    # Rotate
    try:
        exif_dict = piexif.load(exif_data)
    except TypeError:
        img = img.rotate(0, expand=True)
    else:
        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
            #exif_bytes = piexif.dump(exif_dict)

            if orientation == 2: img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3: img = img.rotate(180)
            elif orientation == 4: img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5: img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6: img = img.rotate(-90, expand=True)
            elif orientation == 7: img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8: img = img.rotate(90, expand=True)

    # Resizing and saving 
    img = PILImage(img)
    rsz = Resize(output_size, method=ResizeMethod.Crop)
    img = rsz(img, split_idx=1)
    img.save(picture_path)

    # Load model and predict
    path = Path(current_app.root_path).joinpath('pkls')
    learn_inf = load_learner( path.joinpath('y82-resnet18-multi.pkl') )

    pred,pred_idx,probs = learn_inf.predict(img)
    poses = learn_inf.dls.vocab

    if not pred:
        name = "No pose"
        score = 0
    else:
        name = poses[probs.argmax().item()]
        name = string.capwords(get_pose_name(name))
        score = probs[pred_idx].item()
        score = int(round(float(score),2)*100)

    return picture_fn, score, name



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='admin@yogapose.app', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
