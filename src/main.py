import sys
from spatial_coord_to_pd_code import spatial_coord_to_pd_code

def main():
    inp = eval(sys.stdin.read().strip()) # 输入一个 list of list 作为空间坐标数据
    print(spatial_coord_to_pd_code(inp))

if __name__ == "__main__":
    main()