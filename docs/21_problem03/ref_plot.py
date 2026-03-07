
import matplotlib.pyplot as plt
cwd.create_cwd('./wsm/2/g7-2-plt')
import platform
system = platform.system()
if system == "Windows":
    plt.rcParams['font.sans-serif'] = ['SimHei']
elif system == "Darwin":  # Mac
    plt.rcParams['font.sans-serif'] = ['PingFang SC']
else:  # Linux
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

import json
import math
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


# ======================= 透明度设置（核心） =======================

POINT_ALPHA = 0.35            # 所有点
SUBWAY_LINE_ALPHA = 0.65      # 地铁线
PEDESTRIAN_LINE_ALPHA = 0.65  # 步行线
ARROW_ALPHA = 0.25            # 箭头
STATION_ALPHA = 0.35          # 地铁站点
START_END_ALPHA = 0.75        # 任务路由起点终点
INIT_TERM_ALPHA = 0.25        # 初始位置和技术位置
TASK_TEXTBOX_ALPHA = 0.45     # s{i} / e{i} 标签框（更透明）
LABEL_ALPHA = 0.75            # 其他标注
FINAL_POINT_ALPHA = 0.6       # 最终终点稍微明显一点


# 定义球面距离计算函数（哈弗辛公式）
def haversine(p1, p2):
    R = 6371.0 * 1000  # 地球半径，单位米
    lat1, lon1 = math.radians(p1[1]), math.radians(p1[0])
    lat2, lon2 = math.radians(p2[1]), math.radians(p2[0])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 查找最近地铁站函数
def find_nearest_station(point, station_dict, haversine):
    min_dist = float('inf')
    nearest = None
    for name, (lon, lat, lines) in station_dict.items():
        dist = haversine((lon, lat), point)
        if dist < min_dist:
            min_dist = dist
            nearest = name
    return nearest, min_dist

# 路径段类定义
class RouteSegment:
    def __init__(self, from_point, to_point, from_station, to_station, metro_path, walk_start, walk_end):
        self.from_point = from_point
        self.to_point = to_point
        self.from_station = from_station
        self.to_station = to_station
        self.metro_path = metro_path
        self.walk_start = walk_start
        self.walk_end = walk_end

# BFS查找最短地铁路径
def bfs_shortest_path(graph, start, end):
    if start == end:
        return [start]
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        node, path = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

# 加载数据
with open('metro-draw-data-80%.json', 'r', encoding='utf-8') as f:
    metro_data = json.load(f)

station_dict = {}
for station in metro_data['all_stations']:
    name = station['name']
    lon = station['longitude']
    lat = station['latitude']
    lines = station['belong_lines']
    station_dict[name] = (lon, lat, lines)

# 构建地铁图（邻接表）
graph = {}
for line in metro_data['lines']:
    stations = line['stations']
    for i in range(len(stations) - 1):
        st1_name = stations[i]['name']
        st2_name = stations[i+1]['name']
        if st1_name not in graph:
            graph[st1_name] = []
        if st2_name not in graph:
            graph[st2_name] = []
        graph[st1_name].append(st2_name)
        graph[st2_name].append(st1_name)

# 构建任务点序列
start_point = (116.39088849999999, 39.92767)
with open('route_data.json', 'r', encoding='utf-8') as f:
    route_data = json.load(f)
tasks = []
# 存储任务点的标注信息（用于绘图）
task_point_labels = {}
for idx, route in enumerate(route_data['routes']):
    pickup = (route['start_point']['longitude'], route['start_point']['latitude'])
    delivery = (route['end_point']['longitude'], route['end_point']['latitude'])
    tasks.append({'pickup': pickup, 'delivery': delivery})
    # 记录任务点标注 s1/e1, s2/e2...
    task_point_labels[pickup] = f's{idx+1}'
    task_point_labels[delivery] = f'e{idx+1}'

all_points = [start_point]
for task in tasks:
    all_points.append(task['pickup'])
    all_points.append(task['delivery'])

# 构建旅程段
journey_segments = []
for i in range(len(all_points) - 1):
    from_point = all_points[i]
    to_point = all_points[i+1]

    from_station, walk_start = find_nearest_station(from_point, station_dict, haversine)
    to_station, walk_end = find_nearest_station(to_point, station_dict, haversine)

    metro_path = bfs_shortest_path(graph, from_station, to_station)

    segment = RouteSegment(
        from_point=from_point,
        to_point=to_point,
        from_station=from_station,
        to_station=to_station,
        metro_path=metro_path,
        walk_start=walk_start,
        walk_end=walk_end
    )
    journey_segments.append(segment)

# 输出报告
total_walk_distance = sum(seg.walk_start + seg.walk_end for seg in journey_segments)
total_segments = len(journey_segments)
metro_stations_passed = sum(len(seg.metro_path) - 1 for seg in journey_segments if seg.metro_path)

print("\n=== 完整配送任务路径规划报告 ===")
print(f"起点坐标: {start_point}")
print(f"总行程段数: {total_segments}")
print(f"总步行距离: {total_walk_distance:.0f} 米")
print(f"地铁经过站点数: {metro_stations_passed} 站")
print("\n详细路径:")

for i, seg in enumerate(journey_segments):
    print(f"--- 第{i+1}段 ---")
    print(f"从 {seg.from_point} → {seg.to_point}")
    print(f"最近地铁站: {seg.from_station} → {seg.to_station}")
    print(f"步行距离: 入站 {seg.walk_start:.0f}m, 出站 {seg.walk_end:.0f}m")
    if seg.metro_path:
        print(f"地铁路径: {' → '.join(seg.metro_path)} ({len(seg.metro_path)-1} 段)")
    else:
        print("无地铁连接，需全程步行")

# ===================== 路径可视化部分 =====================
# 创建自定义渐变色彩映射（从蓝色到红色的渐变）
colors = [(0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # 蓝→青→绿→黄→红
n_bins = 100  # 渐变精度
cmap_name = 'route_gradient'
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

# 初始化绘图
fig, ax = plt.subplots(figsize=(15, 10))

# 设置固定的经纬度范围
lon_min, lon_max = 116.215722, 116.562321
lat_min, lat_max = 39.802971, 40.052657
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)

# 收集所有经过的地铁站
passed_stations = set()
for seg in journey_segments:
    if seg.metro_path:
        for st in seg.metro_path:
            passed_stations.add(st)
    # 加入起终点对应的地铁站
    passed_stations.add(seg.from_station)
    passed_stations.add(seg.to_station)

# 绘制经过的地铁站点（黑色标记）并标注名称
for name in passed_stations:
    lon, lat, _ = station_dict[name]
    # 绘制站点标记（黑色小圆点）
    ax.scatter(lon, lat, color='black', s=15, alpha=STATION_ALPHA, zorder=2)
    # 标注站点名称（黑色字体，避免重叠微调位置）
    ax.annotate(name, (lon, lat), xytext=(2, 2), textcoords='offset points', 
                fontsize=9, color='black', alpha=LABEL_ALPHA, zorder=3)

# 绘制各段路径
for seg_idx, seg in enumerate(journey_segments):
    # 获取当前段的起点和终点坐标
    from_lon, from_lat = seg.from_point
    to_lon, to_lat = seg.to_point
    
    # 计算当前段在整体路径中的颜色比例
    color_ratio = seg_idx / total_segments
    segment_color = custom_cmap(color_ratio)
    
    # 1. 绘制步行路段（从起点到最近地铁站，黑色虚线）
    from_station_lon, from_station_lat, _ = station_dict[seg.from_station]
    ax.plot([from_lon, from_station_lon], [from_lat, from_station_lat], 
            color='black', linewidth=2, linestyle='--', alpha=SUBWAY_LINE_ALPHA, zorder=4)
    # 步行段箭头
    mid_walk1_lon = (from_lon + from_station_lon) / 2
    mid_walk1_lat = (from_lat + from_station_lat) / 2
    angle_walk1 = math.atan2(from_station_lat - from_lat, from_station_lon - from_lon)
    arrow_walk1 = patches.FancyArrowPatch(
        (mid_walk1_lon, mid_walk1_lat),
        (mid_walk1_lon + 0.0003 * math.cos(angle_walk1), mid_walk1_lat + 0.0003 * math.sin(angle_walk1)),
        connectionstyle="arc3,rad=0.05",
        arrowstyle='->', color='black', linewidth=1, mutation_scale=10, alpha=0.8, zorder=5
    )
    ax.add_patch(arrow_walk1)
    
    # 2. 绘制地铁路段（渐变色彩实线）
    if seg.metro_path:
        # 获取地铁站点坐标
        metro_coords = [station_dict[st][:2] for st in seg.metro_path]
        metro_lons = [p[0] for p in metro_coords]
        metro_lats = [p[1] for p in metro_coords]
        
        # 绘制地铁路径（渐变色彩实线）
        ax.plot(metro_lons, metro_lats, color=segment_color, 
               linewidth=3, linestyle='--', alpha=SUBWAY_LINE_ALPHA, zorder=6)
        
        # 地铁段箭头（每段地铁线段都加箭头）
        for i in range(len(metro_coords)-1):
            m_from_lon, m_from_lat = metro_coords[i]
            m_to_lon, m_to_lat = metro_coords[i+1]
            mid_metro_lon = (m_from_lon + m_to_lon) / 2
            mid_metro_lat = (m_from_lat + m_to_lat) / 2
            angle_metro = math.atan2(m_to_lat - m_from_lat, m_to_lon - m_from_lon)
            arrow_metro = patches.FancyArrowPatch(
                (mid_metro_lon, mid_metro_lat),
                (mid_metro_lon + 0.0004 * math.cos(angle_metro), mid_metro_lat + 0.0004 * math.sin(angle_metro)),
                connectionstyle="arc3,rad=0.05",
                arrowstyle='->', color=segment_color, linewidth=1.5, mutation_scale=15, alpha=ARROW_ALPHA, zorder=7
            )
            ax.add_patch(arrow_metro)
    
    # 3. 绘制出站步行路段（从目的地铁站到终点，黑色虚线）
    to_station_lon, to_station_lat, _ = station_dict[seg.to_station]
    ax.plot([to_station_lon, to_lon], [to_station_lat, to_lat], 
            color='black', linewidth=2, linestyle='--', alpha=SUBWAY_LINE_ALPHA, zorder=4)
    # 步行段箭头
    mid_walk2_lon = (to_station_lon + to_lon) / 2
    mid_walk2_lat = (to_station_lat + to_lat) / 2
    angle_walk2 = math.atan2(to_lat - to_station_lat, to_lon - to_station_lon)
    arrow_walk2 = patches.FancyArrowPatch(
        (mid_walk2_lon, mid_walk2_lat),
        (mid_walk2_lon + 0.0003 * math.cos(angle_walk2), mid_walk2_lat + 0.0003 * math.sin(angle_walk2)),
        connectionstyle="arc3,rad=0.05",
        arrowstyle='->', color='black', linewidth=1, mutation_scale=10, alpha=0.8, zorder=5
    )
    ax.add_patch(arrow_walk2)
    
    # 4. 标注路段起点和终点编号
    # 起点标注：当前段号-1
    ax.annotate(f'{seg_idx}', (from_lon, from_lat), xytext=(5, 5), 
                textcoords='offset points', fontsize=9, color='darkred', 
                fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=POINT_ALPHA), zorder=9)
    # 终点标注：当前段号
    end_label = f'{seg_idx+1}'
    if seg_idx == total_segments - 1:
        ax.annotate(end_label, (to_lon, to_lat), xytext=(5, 5), 
                    textcoords='offset points', fontsize=9, color='darkred', 
                    fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=FINAL_POINT_ALPHA), zorder=9)
    else:
        ax.annotate(end_label, (to_lon, to_lat), xytext=(5, 5), 
                    textcoords='offset points', fontsize=9, color='darkred', 
                    fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=POINT_ALPHA), zorder=9)

    # 5. 标注route_data中的任务点（s1/e1, s2/e2...）
    # 标注段起点（如果是任务点）
    if seg.from_point in task_point_labels:
        ax.annotate(task_point_labels[seg.from_point], (from_lon, from_lat), xytext=(-10, 10),
                    textcoords='offset points', fontsize=10, color='blue',
                    fontweight='bold', bbox=dict(boxstyle="round,pad=0.4", fc="yellow", ec="blue", alpha=TASK_TEXTBOX_ALPHA), zorder=11)
    # 标注段终点（如果是任务点）
    if seg.to_point in task_point_labels:
        ax.annotate(task_point_labels[seg.to_point], (to_lon, to_lat), xytext=(-10, 10),
                    textcoords='offset points', fontsize=10, color='blue',
                    fontweight='bold', bbox=dict(boxstyle="round,pad=0.4", fc="yellow", ec="blue", alpha=TASK_TEXTBOX_ALPHA), zorder=11)
    
    # 6. 标注任务点（当前段的起点和终点）
    # 标注段起点
    ax.scatter(from_lon, from_lat, color=segment_color, s=80, marker='o', 
               alpha=START_END_ALPHA, edgecolors='black', linewidth=1, zorder=8)
    # 标注段终点（最后一段单独处理）
    if seg_idx == total_segments - 1:
        ax.scatter(to_lon, to_lat, color='red', s=150*2, marker='*', 
                   alpha=INIT_TERM_ALPHA, edgecolors='black', linewidth=2, zorder=10, label='最终终点')

    ax.scatter(to_lon, to_lat, color=segment_color, s=80, marker='o', 
                alpha=START_END_ALPHA, edgecolors='black', linewidth=1, zorder=8)

# 绘制起点标记（蓝色星标）
start_lon, start_lat = start_point
ax.scatter(start_lon, start_lat, color='blue', s=150*2, marker='*', 
           alpha=INIT_TERM_ALPHA, label='起点', edgecolors='black', linewidth=2, zorder=10)

# 设置图表样式
ax.set_xlabel('经度', fontsize=12)
ax.set_ylabel('纬度', fontsize=12)
ax.set_title('配送任务完整路径规划图（含所有站点标注+步行路段）', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, zorder=1)
ax.legend(loc='upper right', fontsize=10)

# 添加颜色条（显示渐变对应路段）
sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=plt.Normalize(0, total_segments))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('路段序号', fontsize=10)

# 调整布局避免文字重叠
plt.tight_layout()
# 显示图表
plt.show()