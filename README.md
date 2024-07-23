# spatial_coord_to_pd_code
将扭结的空间坐标数据转换为 PD_CODE。

由于我实在是懒得重构我的 C++ 程序，这里暂时复用了 `x86_64` 下编译得到的二进制，未来争取把它换掉。



## 前置条件 

- `linux`, `x86_64`, `bash`
- `python3`



## 使用方法

- `python3 ./src/main.py`
  - 向标准输入中输入一个 list of list 作为坐标序列，内层 list 里有三个数值，分别表示采样点的 x, y, z 坐标
  - 程序会向标准输出中输出一行内容，即为 PD\_CODE

