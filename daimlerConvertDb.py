'''This is the python script to convert Daimler Path Prediction Benchmark db file in python class'''

import copy

class Seq():
    def __init__(self):
        self.seq_id = []
        self.path_to_seq_data = []
        self.numimages = []
        self.imglists = []
    def update_seq(self, data):
        self.seq_id, self.path_to_seq_data, self.numimages = data[0],data[1],int(data[2])

class Img():
    def __init__(self):
        self.image_name = []
        self.width = []
        self.height = []
        self.default_obj_class = []
        self.numobjects = []
        self.objlists = []
    def update_img(self, data):
        # print(data)
        self.image_name.append(data[0])
        self.width.append(int(data[1].split(' ')[0]))
        self.height.append(int(data[1].split(' ')[1]))
        self.default_obj_class.append(int(data[2].split(' ')[0]))
        self.numobjects.append(int(data[2].split(' ')[1]))
        self.objlists.append(int(data[3]))

class Obj2d():
    def __init__(self):
        self.data = []
        self.attrs = []
    def update_obj(self, data):
        if data == []:
            self.data.append([])
        else:
            tmp = 17*[[],]
            tmp[0] = data[0].split(' ')[1]
            tmp[1:3] = data[1].split(' ')
            tmp[3] = float(data[2])
            tmp[10:14] = [int(data[3].split(' ')[i]) for i in range(4)]
            self.data.append(tmp)
    def update_attrs(self, attrs):
        if attrs == []:
            self.attrs.append([])
        else:
            attrs_dict = {}
            for i in range(len(attrs)):
                attrs[i] = attrs[i].strip().split(' ')[1:]
                attrs_dict[attrs[i][0]] = float(attrs[i][1])
            self.attrs.append(attrs_dict)

class Obj3d():
    def __init__(self):
        self.data = []
        self.attrs = {}
    def update_obj(self, data, attrs):
        self.data.append(data)
        self.attrs.append(attrs)

class DaimlerPath(Seq):
    def __init__(self, Seq, Img, Obj2d):
        self.sequences = Seq()
        self.images = Img()
        self.objects = Obj2d()
        self.detection_area_x = []
        self.detection_area_y = []
        self.detection_area_z = []
def read_one_seq(fname):
    f = open(fname, 'r')
    da = f.readlines()
    f.close()
    oneseq = DaimlerPath(Seq, Img, Obj2d)
    # separator characters
    seq_separator = ':'
    img_separator = ';'
    obj_2d_separator = '#'
    obj_3d_separator = '?'
    comment_attribute = '%'
    seq_tmp = []
    img_tmp = []
    img_info = []
    obj2d_info = []
    state = []
    img_ind = 0

    for i, d in enumerate(da):
        d=d.strip()
        if d == seq_separator:
            state = 'sequence'
        elif d == img_separator or i == len(da)-1:
            if i == len(da)-1:
                img_tmp.append(d.strip())
            state = 'image'
            if img_tmp != []:
                img_tmp = img_tmp[1:]
                data = copy.deepcopy(img_tmp[0:3])
                data.append(img_ind)
                oneseq.images.update_img(data)
                if len(img_tmp)>3:
                    if obj_2d_separator in img_tmp[3]:
                        oneseq.objects.update_obj(img_tmp[3:8])
                        if len(img_tmp)>8:
                            if comment_attribute in img_tmp[8]:
                                oneseq.objects.update_attrs(img_tmp[8:])
                        else:
                            oneseq.objects.update_attrs([])
                    else:
                        oneseq.objects.update_obj([])
                    if comment_attribute in img_tmp[3]:
                        oneseq.objects.update_attrs(img_tmp[3:])
                else:
                    oneseq.objects.update_obj([])
                    oneseq.objects.update_attrs([])
                img_tmp = []
                img_ind = img_ind + 1
        if state == 'sequence':
            seq_tmp.append(d.strip())
        if state == 'image':
            img_tmp.append(d.strip())
    oneseq.sequences.update_seq(seq_tmp[1:])
    return oneseq

if __name__ == '__main__':
    oneseq=read_one_seq('gt.db')
