# MiniGISApplication
For GIS presentation

说明
----
* StyleOn属性设为True时，还需将显示屏显示设置-缩放与布局-更改文本、应用等项目的大小-设为100%（需重启），才能正常显示UI
* 如果不知道图标所代表的功能，鼠标悬停可以查看
* 窗体大小设为固定

文件说明
----
### UI文件夹
* 界面文件,包括.UI和一些图像文件
* 把界面`.ui`和`.py`文件放入UI文件夹，然后在`__init__.py`中添加引用，即可在`Main.py`中直接使用。
### Function文件夹
* 函数功能文件
* 使用方法同上
### Main文件
* 主函数文件，包括界面启动及基本功能
### .gitignore文件
* 忽视了使用Pycharm开发时自动生成的.idea，venv文件夹
### README文件

绘图参考
----
    https://www.pythonguis.com/tutorials/bitmap-graphics/