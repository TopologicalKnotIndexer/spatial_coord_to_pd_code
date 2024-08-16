# 给定空间中的坐标序列
# 计算对应扭结的 PD_CODE
# 我们直接从 knot-indexer 项目中复用一个二进制文件 knot-pdcode 过来（反正是我自己写的）
# 不出问题就先凑合用着，出了问题再说

import os
import subprocess
import sys
DIRNOW       = os.path.dirname(os.path.abspath(__file__))
KNOT_PDCODE  = os.path.join(DIRNOW, "knot-pdcode")
BUILD_SCRIPT = os.path.join(DIRNOW, "build_knot-pdcode.sh") # 其中会使用 g++ 构建 knot-pdcode
SAMPLE_DATA  = os.path.join(DIRNOW, "sample_data.txt")      # 用于测试的样例数据

def __build_knot_pdcode(): # 重新构建可执行文件
    ret = subprocess.run(["bash", BUILD_SCRIPT])
    return ret.returncode

if not os.path.isfile(KNOT_PDCODE): # 可执行文件不存在，则重新构建
    __build_knot_pdcode()
    assert os.path.isfile(KNOT_PDCODE) # 构建后，knot-pdcode 必须存在

def __grant_exec(): # 给指定的可执行文件赋予可执行权限
    ret = subprocess.run(["chmod", "+x", KNOT_PDCODE])
    return ret.returncode

def __coord_check(spatial_coord: list[list]): # 检查输入的坐标序列是否合法
    assert isinstance(spatial_coord, list)
    for node in spatial_coord:
        assert isinstance(node, list)
        assert len(node) == 3 # 必须是三维坐标序列
        for x in node:
            assert type(x) in [int, float] # 必须是整数或者浮点数坐标

def __gen_text_spatial_data(spatial_coord): # 生成文本形式的 knot-pdcode 的输入数据
    fontline  = "%d\n" % len(spatial_coord)  # 第一行包含采样点的总个数
    nextlines = []
    for coord in spatial_coord:
        nextlines.append("%.20f %.20f %.20f" % tuple(coord)) # 把坐标写成字符串写入文件
    return fontline + ("\n".join(nextlines)) + "\n"   # 连接

def spatial_coord_to_pd_code(spatial_coord: list[list]) -> list: # 将空间数据转化为 PD_CODE
    __coord_check(spatial_coord)
    __grant_exec()
    txt_spatial_data = __gen_text_spatial_data(spatial_coord)
    pfile = subprocess.Popen([KNOT_PDCODE],
                            stdin=subprocess.PIPE, # 直接使用程序控制 stdin 即可
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout_ans, stderr_ans = pfile.communicate(txt_spatial_data.encode())
    returncode = pfile.returncode
    if returncode != 0:  # 不能允许出错的情况发生
        sys.stderr.write(stderr_ans.decode())
        assert False
    return eval(stdout_ans.decode()) # 此处应该赶回一个 list of list 作为 PD_CODE

def __get_sample_data(): # 从样例数据中获取采样点空间坐标序列
    assert os.path.isfile(SAMPLE_DATA)
    arr = []
    for line in open(SAMPLE_DATA):
        line = line.strip()
        if line == "" or line[0] == "#": # 忽略空行以及井号开头的行
            continue
        arr.append(list(map(float, line.split())))
    return arr

if __name__ == "__main__": # 测试
    coord_data = __get_sample_data()
    print(spatial_coord_to_pd_code(coord_data))
