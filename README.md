
install(Python ≥ 3.9):
```python
pip install mujoco
```

description/mjcf 为 mujoco 的仿真配置文件

rizon4.xml 是机械臂的配置文件，不用动

config.xml 是配置文件，同时负责加载外部的文件资源，需要加载外部资源的时候在这里修改

scene.xml 是主仿真配置文件，其通过 include 方法把 rizon4.xml 和 config.xml 进行导入

故 scene.xml 也是 mujoco 仿真启动时加载的文件

运行仿真:
```python
cd {prj_path}
python sim.py
```


第一次加入仓库：
```
# some works should be done before clone repo
# 把自己的 ssh 公钥添加到 github user config
# 1. 生成公钥
略
# 2. 把公钥添加到 github 
略

git clone https://github.com/bot-learner/coal_yard_sim.git
git remote add origin git@github.com:bot-learner/coal_yard_sim.git
# 测试 ssh 能否连接到 github
ssh -T git@github.com
```


向仓库 push 代码：
```
git add .
git commit -m "some info you should write"
git push -u origin main
```
