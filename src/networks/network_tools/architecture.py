class Architecture:
    full_config_file_name = "full_config.txt"
    opt_config_file_name = "opt_config.txt"
    layers_config_file_name = "layers_config.txt"
    base_model_names = ['densenet', 'densenet121', 'densenet169', 'densenet201', 'inception_resnet_v2', 'inception_v3',
                        'NASNet', 'resnet50', 'vgg16', 'vgg19', 'xception', ]
    def __init__(self, model):
        self.full_config = model.get_config()
        self.layers_list = self.list_layers(model)
        self.opt_config = model.optimizer.get_config()

    def log(self, path):
        with open(path + self.layers_config_file_name, 'w') as f:
            for layer in self.layers_list:
                f.write("%s\n" % layer)

        f = open(path + self.full_config_file_name, "w")
        f.write(str(self.full_config))
        f.close()

        f = open(path + self.opt_config_file_name, "w")
        f.write(str(self.opt_config))
        f.close()

    def list_layers(self, model):
        layers_list = []
        for layer in model.layers:
            if any(layer.name in s for s in self.base_model_names):
                for l in layer.layers:
                    layers_list.append(l.name + ' - ' + 'trainable: ' + str(l.trainable))
            else:
                layers_list.append(layer.name + ' - ' + 'trainable: ' + str(layer.trainable))
        return layers_list
