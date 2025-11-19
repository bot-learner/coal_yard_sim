import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import time
import math

import mujoco
import mujoco.viewer

# MjModel 存储模型文件信息，mjData 存储仿真数据
# 根据 mujoco xml 文件来创建一个 静态模型
# m = mujoco.MjModel.from_xml_path('/home/wanghan/prj/mujoco_flexiv_sim/flexiv_description/urdf/rizon.xml')
m = mujoco.MjModel.from_xml_path('./description/mjcf/scene.xml')
# m = mujoco.MjModel.from_xml_path('/home/wanghan/prj/mujoco_flexiv_sim/universal_robots_ur5e/scene.xml')
d = mujoco.MjData(m)  # 根据这个静态模型来创建一个动态模型


def main():
    # 使用 launch_passive 意味着 viewer 不自动推进仿真，需要你手动调用 mj_step
    with mujoco.viewer.launch_passive(m, d) as viewer:  # 使用 GUI 启动仿真器

        # Close the viewer automatically after 30 wall-seconds.
        start = time.time()
        cnt = 0
        # 限制仿真运行 30 秒 或直到用户关闭窗口
        while viewer.is_running() and time.time() - start < 3000:
            step_start = time.time()

            # joint_id = m.get_joint_qpos_addr("joint1")  # 返回索引
            # angle1 = d.qpos[joint_id]
            # print("joint1 angle:", angle1)

            # 获取关节角度
            # joint = [
            #     d.sensor(name).data.item() for name in [
            #         "jp1", "jp2", "jp3", "jp4", "jp5", "jp6", "jp7",
            #     ]
            # ]
            # print(joint)

            # 每调用一次 mj_step()，MuJoCo 就推进一个 timestep
            # （通常是 0.002s 或你在 XML 文件中设置的值）。

            '''测试step '''
            # 前向动力学（计算加速度 qacc） 数值积分（更新状态 qpos, qvel） 处理碰撞和约束 更新传感器数据
            # d.ctrl[1] = math.sin(cnt)  # 设置控制量
            mujoco.mj_step(m, d)  # 最普通的推进一整步

            '''测试step1 step2 '''
            # 这种方式有两种使用场景：1. 控制量的计算依赖于传感器状态，2. 观测给与控制量前后对比
            # mujoco.mj_step1(m, d)  # 推进到 控制输入之前
            # d.ctrl[1] = math.sin(cnt)  # 计算控制输入
            # mujoco.mj_step2(m, d)  # 施加输入之后再推进一次

            '''测试forward 正向动力学，进行推演（如果我给这样的控制量的话，状态会怎么变） '''
            # 给定关节位置(qpos)、速度(qvel)和关节力矩(τ)，计算关节加速度(qacc)
            # d.ctrl[0] = math.sin(cnt)
            # d.qpos[0] = math.sin(cnt)
            # mujoco.mj_forward(m, d)  # 没有推进时间，也不会改变系统状态，只是更新状态衍生量
            # print("qvel:", d.qvel)
            # print("qacc:", d.qacc)
            # print("qpos:", d.qpos)

            '''测试inverse 逆向动力学，也是推演（要实现这样的状态需要多大的控制量）'''
            # 给定关节位置(qpos)、速度(qvel)、加速度(qacc)，计算所需的关节力矩(τ)
            # d.qacc[0] = math.sin(cnt)
            # d.qpos[0] = 0
            # d.qvel[0] = 0
            # mujoco.mj_inverse(m, d)
            # print("qfrc_inverse", d.qfrc_inverse)

            cnt += 0.01

            # 每两秒开/关一次接触点显示
            # 加一个线程锁，确保在多线程/GUI环境下修改 viewer 的配置是安全的，不会和渲染线程冲突
            # 所有对 viewer.opt 的修改都建议放在这个 with 块中
            # with viewer.lock():
            #     # viewer.opt.flags 是 MuJoCo 控制哪些东西在 GUI 中显示的“开关集合”
            #     # mujoco.mjtVisFlag.mjVIS_CONTACTPOINT 是其中一个开关
            #     # “是否在 GUI 中显示接触点（两个物体接触的位置）”
            #     viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = int(d.time % 2)

            # Pick up changes to the physics state, apply perturbations, update options from GUI.
            # viewer.sync() 会同步 GUI、应用鼠标拖动、GUI 控件等
            # 1. 第一个作用是把在 MjData 和 viewer.opt 等数据结构里的最新变化，
            #    同步到图形界面上，让用户看到更新后的仿真状态
            # 2. 同步仿真数据（MjData）到渲染器（例如刚刚 mj_step/mj_step1 后的结果）
            # 3. 触发渲染图形界面，显示当前仿真状态
            viewer.sync()

            # 保证每次 m.opt.timestep 时间 进行一步 仿真，保证仿真间隔是一致的
            # m.opt.timestep：是在 MJCF/XML 中设置的物理仿真时间步长，单位是秒，例如 0.002
            time_until_next_step = m.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)


if __name__ == "__main__":
    main()