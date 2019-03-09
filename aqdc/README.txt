注意：
    1. xadmin到对应当前所用的django的版本，去https://github.com/sshwsfc/xadmin下载
        对应版本的xadmin-xx.zip，解压后提取xadmin文件夹与requirements.txt放到
        项目目录下
    2. xadmin文件夹相当于一个库，就不用安装xadmin了
    3. requirements.txt文件处理依赖
    4. 若你的django是2.x版本，为解决在xadmin中添加组件时遇到的问题，请务必pip install django==2.0.8
    5. 若你要修改xadmin中页脚的显示请修改xadmin/templates/xadmin/base_site.html中的内容
相关xadmin的操作参见https://blog.csdn.net/u014793102/article/details/80316335