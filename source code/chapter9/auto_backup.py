# -*- coding: utf-8 -*-

# 导入库
import os
import zipfile
from datetime import datetime

def zip_dir(scr_path, tar_path):
    filelist = []
    for root, dirs, files in os.walk(scr_path):
        for name in files:
            filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(tar_path, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(scr_path):]
        zf.write(tar, arcname)
    zf.close()
	
# 源文件
scr_paths = [r'D:\[书籍]python数据分析\3_附件\chapter9\sales_data',
              r'D:\[书籍]python数据分析\3_附件\chapter9\traffic_data']
# 目标文件
tar_paths = [r'E:\BK\sales_data.zip',
               r'E:\BK\traffic_data.zip']
# 日期字符串
dt = datetime.now().strftime("%Y%m%d%H%M%S")

# 删除历史备份
for each_file in tar_paths:
    if os.path.exists(each_file):
        os.remove(each_file)
		
# 执行单次备份
with open(f'backup_{dt}.log','w+') as fn:
    for scr_path, tar_path in zip(scr_paths, tar_paths):
        target_path = os.path.split(tar_path)[0]
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        fn.write(f'source {scr_path} → target {tar_path} start...')
        zip_dir(scr_path, tar_path)
        fn.write(f'\n')
        fn.write(f'source {scr_path} → target {tar_path} success!!!')
        fn.write(f'\n')