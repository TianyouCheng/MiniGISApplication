import os,sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#region 引入窗体
from MainGUI import Ui_MainWindow

#endregion

# 主窗体操作
class Main_exe(QMainWindow,Ui_MainWindow):
    def __init__(self):
        # 创建窗体
        super(Main_exe,self).__init__()
        self.setupUi(self)




# 作为主窗体运行
if __name__=='__main__':
    myapp=QApplication(sys.argv)
    myDlg=Main_exe()
    myDlg.show()
    sys.exit(myapp.exec_())
