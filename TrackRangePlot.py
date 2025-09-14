import numpy as np
import matplotlib.pyplot as plt

# fig, ax = plt.subplots(2,2)
#
# heights = ["2", "2.25"]
# degrees2 = ["15", "20"]
# degrees1 = ["10", "15"]
#
# for i, height in enumerate(heights):
#     degrees = []
#     if height == "2":
#         degrees = degrees1
#     else:
#         degrees = degrees2
#
#     for j, degree in enumerate(degrees):
#         file_name = "TrackLog_" + height + "m_" + degree + "d"
#         track_data = np.load(file_name + "_n.npy", allow_pickle=True)
#
#         plot_data = []
#
#         for frame in track_data:
#             for target in frame:
#                 print(target)
#                 target_id = target[0]
#                 target_x = target[1]
#                 target_y = target[2]
#                 if target_id >= len(plot_data):
#                     temp_list = []
#                     plot_data.append(temp_list)
#                 plot_data[target_id].append([target_x, target_y])
#
#         plt.figure(1)
#         in_points = [x[0] for x in plot_data]  # 进入范围内的第一个点的xy坐标
#         out_points = [x[-1] for x in plot_data]  # 离开范围的点的xy坐标
#
#         track_data = np.load(file_name + "_y.npy", allow_pickle=True)
#
#         plot_data = []
#
#         for frame in track_data:
#             for target in frame:
#                 target_id = target[0]
#                 target_x = target[1]
#                 target_y = target[2]
#                 if target_id >= len(plot_data):
#                     temp_list = []
#                     plot_data.append(temp_list)
#                 plot_data[target_id].append([target_x, target_y])
#
#         in_points.extend([x[0] for x in plot_data])
#         out_points.extend([x[-1] for x in plot_data])
#
#         ax[i][j].scatter([x[0] for x in in_points], [x[1] for x in in_points], label="in")
#
#         ax[i][j].scatter([x[0] for x in out_points], [x[1] for x in out_points], label="out")
#
#         ax[i][j].legend()
#         ax[i][j].set_xlim(-4, 4)
#         ax[i][j].set_ylim(0, 10)
#         ax[i][j].set_title("Height " + height + "m  Elevation: " + degree + "d")
#
# # plt.savefig("./out/2-2.25.svg")
# plt.show()


height = "2.1"
degree = "15"
file_name = "TrackLog_" + height + "m_" + degree + "d"
track_data = np.load(file_name + "_n.npy", allow_pickle=True)

plot_data = []

for frame in track_data:
    for target in frame:
        print(target)
        target_id = target[0]
        target_x = target[1]
        target_y = target[2]
        if target_id >= len(plot_data):
            temp_list = []
            plot_data.append(temp_list)
        plot_data[target_id].append([target_x, target_y])

plt.figure(1)
in_points = [x[0] for x in plot_data]  # 进入范围内的第一个点的xy坐标
out_points = [x[-1] for x in plot_data]  # 离开范围的点的xy坐标

# track_data = np.load(file_name + "_y.npy", allow_pickle=True)
#
# plot_data = []
#
# for frame in track_data:
#     for target in frame:
#         target_id = target[0]
#         target_x = target[1]
#         target_y = target[2]
#         if target_id >= len(plot_data):
#             temp_list = []
#             plot_data.append(temp_list)
#         plot_data[target_id].append([target_x, target_y])
#
# in_points.extend([x[0] for x in plot_data])
# out_points.extend([x[-1] for x in plot_data])

plt.scatter([x[0] for x in in_points], [x[1] for x in in_points], label="in")
plt.scatter([x[0] for x in out_points], [x[1] for x in out_points], label="out")

plt.legend()
plt.xlim(-4, 4)
plt.ylim(0, 10)
plt.title("Height " + height + "m  Elevation: " + degree + "d")
plt.savefig("./out/" + file_name + ".svg")

plt.show()
