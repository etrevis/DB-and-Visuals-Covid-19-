import imageio
import os
from pygifsicle import optimize
import time

today_gif = "0{}-0{}.gif".format(time.gmtime(time.time()).tm_mday,time.gmtime(time.time()).tm_mon)
today_gif_opt = "0{}-0{}_opt.gif".format(time.gmtime(time.time()).tm_mday,time.gmtime(time.time()).tm_mon)


gif_path = os.path.join(os.getcwd(),'GIFs',today_gif)
gif_path_opt = os.path.join(os.getcwd(),'GIFs',today_gif_opt)
figs_path  = os.path.join(os.getcwd(),'Figs')

gif_settings ={'fps' : 5}

figures = []
for (dirpath, dirnames, filenames) in os.walk(figs_path):
    for file in filenames:
        if 'png' in file:
            figures.append(file)
figures = sorted(figures,key=lambda x: int(os.path.splitext(x)[0]))
for i in range(10):
	figures.append(figures[len(figures)-1])
print(figures)

images = []
for fig in figures:
    images.append(imageio.imread(os.path.join(os.getcwd(),'Figs',fig)))

    
with imageio.get_writer(gif_path, mode='I', **gif_settings) as writer:
    for fig in figures:
        writer.append_data(imageio.imread(os.path.join(figs_path,fig)))

optimize(gif_path, gif_path_opt)
exit()