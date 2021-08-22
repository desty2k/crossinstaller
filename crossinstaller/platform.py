
class Platform:

    def __init__(self, name, image, extra_files=None):
        super(Platform, self).__init__()

        self.name = name
        self.image = image

        if extra_files is None:
            self.extra_files = []
        else:
            self.extra_files = extra_files
