from keras.applications import VGG16, VGG19
from keras.applications import InceptionV3
from keras.applications import ResNet50
from keras.applications import InceptionResNetV2
from keras.applications import Xception
from keras.applications import DenseNet121, DenseNet169, DenseNet201
from keras.applications import NASNetMobile, NASNetLarge

import network_tools.settings as settings

def get_VGG16(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return VGG16(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_VGG19(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return VGG19(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_InceptionV3(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return InceptionV3(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_ResNet50(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return ResNet50(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_InceptionResNetV2(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return InceptionResNetV2(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_Xception(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return Xception(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_DenseNet121(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return DenseNet121(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))

def get_DenseNet169(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return DenseNet169(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_DenseNet201(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return DenseNet201(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_NASNetMobile(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
        
    return NASNetMobile(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
    
def get_NASNetLarge(include_weights=True, do_include_top=True):
    weights_s='imagenet'
    if include_weights==False:
        weights_s=None
    
    return NASNetLarge(weights=weights_s,
                      include_top=do_include_top,
                      input_shape=(settings.input_x, settings.input_y, 3))
