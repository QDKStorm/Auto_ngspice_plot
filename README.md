# Auto ngspice plot

有两个示例spice代码`7-10.cp`和`7-11.cp`，分别对应7.10和7.11题。

环境：Python 3.8.19 + ngspice 42，要求ngspice在环境变量中

应该只需要一个matplotlib库

通过以下命令运行：

```bash
python auto_spice.py --spice "* 7-10\nV1 1 2 DC 9V\nI1 1 3 3mA\nR1 2 3 1k\nC1 3 0 25uF\nR2 3 0 2k\nS1 0 1 4 0 switchmodel\nV2 4 0 PULSE(0 5 -1 0 0 1 0 1)\n.model switchmodel sw vt=1 vh=0.2 ron=1m roff=1G\n\n.tran 1ms 1s\n.control\nrun\nplot v(3)\n.endc\n.end\n" --circuit 7-11.sp --save
```

其中参数的意义分别是：

- `--spice`：spice代码，可以是多行，用`\n`分隔
- `--circuit`：电路文件名，如果同时有`--spice`参数，`--spice`参数优先
- `--save`：如果有这个参数，会保存图片，否则显示图片

使用了https://github.com/Diordany/spicemill 中的 modules/rawfile.py