# CaptchaCatcher

## Using Machine Learning to Crack Captcha Images

### Dependencies

    Python 3
    OpenCV
    Tensorflow
    Keras
    
### Try it out!

Download virtualenv

    python3 -m pip install --user virtualenv

Run the following to activate and create your virtual environment

    python3 -m venv env
    source env/bin/activate
    cd env
    
Pull the repository

    git pull 

Run:

    pip3 install -r requirements.txt
    
### Extract single letters from the training_data which contains Captcha Images
Run: 

    python3 extract_letters.py

The results are stored in the "extracted_letters" folder.


### Train the neural network to recognize the single letters

Run:

    python3 train_model.py

This will write out "captcha_model.hdf5" and "model_labels.dat"


### Using the model

Run: 



### Made by following

https://www.pyimagesearch.com/deep-learning-computer-vision-python-book/

https://medium.com/@ageitgey/how-to-break-a-captcha-system-in-15-minutes-with-machine-learning-dbebb035a710

