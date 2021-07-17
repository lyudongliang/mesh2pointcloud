'''
test.py in trimesh2pointcloud

author  : simbaforrest
created : 11/5/17 4:29 PM
'''

import os
import sys
import glob
import time
import argparse

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

import pyximport; pyximport.install(inplace=True)
from _trimesh2pointcloud import cy_trimesh2pointcloud as tri2pts

def strip_slash(str1):
    slash_pos = str1.find('/')
    if slash_pos > -1:
        return int(str1[0:slash_pos])
    else:
        return int(str1)

def read_obj(fname):
    with open(fname) as f:
        content = f.readlines()

    content = [x.strip('\n') for x in content]

    valid_content = []
    for x in content:
        cur_line = x.split()
        if len(cur_line) > 0:
            valid_content.append(cur_line)
    
    type_col = np.array([row[0] for row in valid_content])
    
    v_ind = np.where(type_col == 'v')[0]
    f_ind = np.where(type_col == 'f')[0]

    content = [x[1:4] for x in valid_content]
    content = np.array(content)
    vertices = content[v_ind].tolist()
    faces = content[f_ind].tolist()

    vertices = np.array([[float(y) for y in x] for x in vertices])
    faces = np.array([[strip_slash(y) - 1 for y in x] for x in faces])
    return vertices, faces


def dump_obj_file(file_name, pts):
    with open(file_name, 'w') as f:
        for i in range(pts.shape[0]):
            pt = list(pts[i])
            str_list = [str(round(s, 6)) for s in pt]
            line_str = 'v ' + ' '.join(str_list) + '\n'
            f.write(line_str)   


def main(args):
    # V=np.array([
    #     [1,0,0],
    #     [0,1,0],
    #     [0,0,1]
    # ], dtype=np.float32)
    # G=np.array([
    #     [0,1,2]
    # ], dtype=int)
    # k=1024
    # P = tri2pts(V,G,k)
    # print(P.shape)
    #
    # plt.figure()
    # ax=plt.subplot(111,projection='3d')
    # ax.plot(V[:,0],V[:,1],V[:,2],'b.')
    # ax.plot(P[:,0],P[:,1],P[:,2],'r.')
    # plt.show()

    V, G = read_obj('./cup.obj')
    print('V shape', V.shape)
    print('G shape', G.shape)
    P = tri2pts(V,G,2048)

    V = V * 0.001
    G = G * 0.001
    P = P * 0.001
    print('P shape', P.shape)

    dump_obj_file('./sampled_cup.obj', P)

    plt.figure()
    ax=plt.subplot(111,projection='3d')
    ax.plot(V[:,0],V[:,1],V[:,2],'b.')
    ax.plot(P[:,0],P[:,1],P[:,2],'r.')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(sys.argv[0])

    args = parser.parse_args(sys.argv[1:])
    args.script_folder = os.path.dirname(os.path.abspath(__file__))

    main(args)