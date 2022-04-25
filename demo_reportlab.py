from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics, ttfonts


class DemoReportLab(object):
    """docstring for DemoReportLab"""

    def __init__(self):
        super(DemoReportLab, self).__init__()
        # simsun字体路径
        self.simsun_FONT_PATH = "./fonts/simsun.ttc"
        self.register_Font()
        self.filename = "output.pdf"
        # pdfgen是生成PDF文档的最低级别接口 canvas被认为是一张白纸，以左下角为(0, 0)坐标
        # 实例化一个Canvas对象
        # X坐标默认向右，Y坐标默认向上
        # 参数
        # filename 最终的PDF文件名
        # pagesize 两个点数的tuple 定义页面大小,默认是A4大小
        # 在reportlab.lib.pagesize中定义了letter,A4等页面大小
        # bottomup将来可能会被放弃 为了转换坐标
        # pageCompression 是否对PDF操作进行压缩，默认情况下不被压缩，压缩会减慢运行速度\
        # 如果页面有大量的文本和矢量图形的话压缩会节省空间
        # encrypt 如果赋值一个字符串的话 将会作为PDF的用户密码使用
        self.cav = canvas.Canvas(
            filename=self.filename, pagesize=None, bottomup=1,
            pageCompression=1, encrypt=None)
        self.page_width, self.page_height = self.pagesize = self.cav._pagesize

    def register_Font(self):
        # 注册字体解决中文显示问题
        font = ttfonts.TTFont(name="simsun", filename=self.simsun_FONT_PATH)
        pdfmetrics.registerFont(font=font)

    def draw_PDF(self):
        # 设置字体
        self.set_font()
        self.draw_str()
        self.draw_line()
        self.draw_shape()
        self.draw_image()
        self.change_color()
        self.set_line()
        self.control_cav_state()
        self.draw_textobj()
        self.draw_pathobj()
        self.set_geometry()
        # self.set_grad()
        self.set_other()
        self.save_cav()

    def draw_str(self):
        # 在画布上画上字符串 text 坐标位置 x,y
        # drawString
        # drawRightString 绘制与x坐标右对齐的字符串
        # drawCentredString 绘制以x坐标为中心的字符串
        # drawAlignedString
        text = "ReportLab库的学习"
        x = 300
        y = 420
        self.cav.drawString(x=x, y=y, text=text)
        self.cav.drawRightString(x, y-10, "drawRightString "+text)
        self.cav.drawCentredString(x, y-20, "drawCentredString "+text)
        # self.cav.drawAlignedString(x, y-20, "drawAlignedString "+text)

        self.cav.bookmarkPage(key="draw_str")
        self.show_cav()

    def show_cav(self):
        # showPage 完成当前页面的绘制，保存Canvas对象绘制的当前页面内容,如果后续有新的绘制将在下一个页面进行
        # 另外：当前设置的字体 颜色 旋转等都会重置
        self.cav.showPage()

    def save_cav(self):
        # 保存Canvas对象绘制的内容到filename文件
        self.cav.save()

    def set_font(self):
        # psfontname 字体名称 size 字体大小 leading 行间距？
        self.cav.setFont(psfontname="simsun", size=10, leading=1)

    def draw_line(self):
        self.set_font()
        # 绘制直线
        # x1和y1 作为起点坐标 x2和y2 作为终点坐标 画一条直线
        self.cav.line(x1=300, y1=400, x2=300, y2=550)
        self.cav.drawCentredString(x=300, y=390, text="line方法")
        # 存放多条线的坐标
        crosshairs = [(350, 550, 400, 550),
                      (350, 500, 450, 500),
                      (350, 450, 500, 450),
                      (350, 400, 550, 400), ]
        # 画多条线 参数 linelist 存放多条线的坐标
        self.cav.lines(linelist=crosshairs)
        self.cav.drawCentredString(x=450, y=380, text="lines方法")
        self.cav.bookmarkPage(key="draw_line")
        self.show_cav()

    def draw_shape(self):
        # 绘制形状
        self.set_font()
        # grid 绘制网格  xlist X轴坐标list  ylist Y轴坐标list
        # 源码：grid方法主要逻辑：
        # lines = []
        # y0, y1 = ylist[0], ylist[-1]
        # x0, x1 = xlist[0], xlist[-1]
        # for x in xlist:
        # 在画横线？
        #     lines.append((x, y0, x, y1))
        # for y in ylist:
        # 在画竖线？
        #     lines.append((x0, y, x1, y))
        # Canvas.lines(lines)
        # xlist 中X坐标轴数据等差 画等距地横线
        xlist = [50, 150, 200, 300]
        # ylist 中Y坐标轴数据等差 画等距地竖线
        ylist = [800, 750, 700, 650]
        self.cav.grid(xlist=xlist, ylist=ylist)
        self.cav.drawCentredString(x=175, y=810, text="grid方法")
        # self.cav.bezier(x1=10, y1=10, x2=20, y2=20, x3=30, y3=30, x4=40, y4=40)

        # rect 绘制矩形
        # width 矩形宽度 正数 向右绘制，负数 向左绘制
        # height 矩形高度 正数 向上绘制，负数 向下绘制
        self.cav.rect(x=350, y=800, width=200, height=-150, stroke=1, fill=0)
        self.cav.drawCentredString(x=450, y=810, text="rect方法")

        # circle 绘制一个圆形 x_cen 圆心的X坐标 y_cen圆心的Y坐标 r 圆的半径
        self.cav.circle(x_cen=175, y_cen=500, r=120, stroke=1, fill=0)
        self.cav.drawCentredString(x=175, y=630, text="circle方法")

        # roundRect 绘制一个圆角的矩形 radius参数是矩形四个角圆形的半径 类似CSS的border-radius？
        self.cav.roundRect(x=350, y=620, width=200,
                           height=-240, radius=50, stroke=1, fill=0)
        self.cav.drawCentredString(x=450, y=630, text="roundRect方法")

        # arc 在矩形x1，y1，x2，y2内画一个椭圆 从startAng度开始逆时针画extent度
        self.cav.arc(x1=50, y1=10, x2=300, y2=330, startAng=90, extent=270)
        self.cav.drawCentredString(x=175, y=340, text="arc方法")
        self.cav.drawCentredString(x=175, y=320, text="startAng=90")
        self.cav.drawCentredString(x=300, y=175, text="extent=270")

        # wedge 绘制一个楔形 扇形  参数同arc
        self.cav.wedge(x1=350, y1=175, x2=550, y2=330, startAng=0, extent=200)
        self.cav.drawCentredString(x=450, y=340, text="wedge方法")

        # ellipse 在一个封闭的矩形内绘制一个椭圆
        self.cav.ellipse(x1=350, y1=10, x2=550, y2=165, stroke=1, fill=0)
        self.cav.drawCentredString(x=450, y=175, text="ellipse方法")

        self.cav.bookmarkPage(key="draw_shape")
        self.show_cav()

    def draw_textobj(self):
        from reportlab.lib import colors
        # text object beginText方法创建一个text对象 通过调用text对象的方法进行格式化文本，
        # 文本对象界面提供了对画布级别无法直接使用的文本布局参数的详细控制。
        # 此外，它会生成更小的PDF 比许多单独调用drawString方法的速度更快
        # 然后用drawText方法将text对象绘制到页面上
        #  text object 的 方法：
        # textobject.setTextOrigin(x, y) 重置 text对象的坐标
        # textobject.setTextTransform(a, b, c, d, e, f) 与setTextOrigin类似，但有旋转、缩放等功能
        # textobject.moveCursor(dx, dy)  # 从当前光标 移动 X轴移动dx Y轴移动dy 后的光标
        # (x, y) = textobject.getCursor() 获取text对象的坐标
        # x = textobject.getX() 获取text对象的X坐标
        # y = textobject.getY() 获取text对象的Y坐标
        # textobject.setFont(psfontname, size, leading=None) 设置字体
        # textobject.textLine(text='') 绘制text 绘制完成后光标向下一行移动
        # textobject.textOut(text) 绘制text 绘制完成后光标不向下一行移动
        # textobject.textLines(stuff, trim=1) 绘制多行 对应Python多行字符串类型 trim=0 保留字符串中的空白位置 trim=1 不保留
        # textobject.setCharSpace(charSpace) 调整文本的字符间距
        # textobject.setWordSpace(wordSpace) 调整单词直接的间距 中文没有测试到作用
        # textobject.setHorizScale(horizScale) 水平拉伸或收缩文本行。
        # textobject.setLeading(leading) 调节行间距

        # textobject.setTextRenderMode(mode) 设置文本呈现模式
        # 参数 mode
        # 0 = Fill text
        # 1 = Stroke text
        # 2 = Fill then stroke
        # 3 = Invisible
        # 4 = Fill text and add to clipping path
        # 5 = Stroke text and add to clipping path
        # 6 = Fill then stroke and add to clipping path
        # 7 = Add to clipping path

        # textobject.setRise(rise) 上下移动文本基线以允许上标/下标
        # textobject.setFillColor(aColor) 设置填充颜色
        # textobject.setStrokeColor(aColor)

        # beginText方法返回一个 text object
        textobj = self.cav.beginText(x=300, y=200, direction=None)
        # text 对象的一些方法：
        # setTextOrigin 重置 text对象的坐标
        textobj.setTextOrigin(x=inch, y=10*inch)
        # setTextTransform(a, b, c, d, e, f) 与setTextOrigin类似，但有旋转、缩放等功能
        # textobj.setTextTransform(a, b, c, d, e, f)
        # getCursor getX getY 获取text对象的坐标
        print("getCursor()方法 获取坐标tuple", textobj.getCursor())
        print("getX()方法 获取X坐标", textobj.getX())
        print("getY()方法 获取Y坐标", textobj.getY())
        # setFont 设置字体
        textobj.setFont(psfontname="simsun", size=30, leading=None)
        # 调整文本的字符间距
        textobj.setCharSpace(charSpace=0.1*inch)
        # 调整单词直接的间距 中文没有测试到作用
        textobj.setWordSpace(wordSpace=0.1*inch)
        # 水平拉伸或收缩文本行
        textobj.setHorizScale(horizScale=1.5*inch)
        # 调节行间距
        textobj.setLeading(leading=0.5*inch)
        # 绘制text 绘制完成后光标向下一行移动
        textobj.textLine(text="this is text object")
        # 从当前光标位置进行移动光标到 X轴移动dx Y轴移动dy 后的光标位置
        textobj.moveCursor(dx=20, dy=20)
        # 绘制多行 对应Python多行字符串类型 trim=0 保留字符串中的空白位置 trim=1 不保留
        textobj.textLines(stuff='''
                          1.第一行
                          2.第二行
                          3.第三行''', trim=1)
        # 绘制text 绘制完成后光标不向下一行移动
        textobj.textOut(text="setRise方法")
        # 上下移动文本基线以允许上标/下标
        textobj.setRise(rise=12)
        textobj.textLine(text="上标")
        textobj.setRise(rise=-12)
        textobj.textOut(text="setRise方法")
        textobj.setRise(rise=-20)
        textobj.textLine(text="下标")

        # 设置填充颜色
        textobj.setFillColor(aColor=colors.green)
        # 设置线条颜色
        textobj.setStrokeColor(aColor=colors.red)
        textobj.moveCursor(dx=-50, dy=0)
        # textobject.setTextRenderMode(mode) 设置文本呈现模式
        # 参数 mode
        # 0 = Fill text
        # 1 = Stroke text
        # 2 = Fill then stroke
        # 3 = Invisible
        # 4 = Fill text and add to clipping path
        # 5 = Stroke text and add to clipping path
        # 6 = Fill then stroke and add to clipping path
        # 7 = Add to clipping path
        # mode == 3 or 7 在页面上看不到内容
        textobj.textLine(text="setTextRenderMode方法：")
        textobj.setFont(psfontname="simsun", size=50, leading=50)
        for mode in range(8):
            textobj.setTextRenderMode(mode=mode)
            textobj.textLine(text=f"mode={mode}:mode")
        # 调用Canvas对象的drawText方法完成绘制
        # drawText(aTextObject)
        # aTextObject == PDFTextObject对象
        self.cav.drawText(aTextObject=textobj)

        self.cav.bookmarkPage(key="draw_textobj")
        self.show_cav()

    def draw_pathobj(self):
        # path object类似于text object path对象提供了可以执行复杂图像绘制的方法，
        # beginPath方法 返回PDFPathObject
        pathobject = self.cav.beginPath()

        # pathobject.moveTo(x,y)
        # 提起画笔 移动到坐标 x,y
        pathobject.moveTo(x=100, y=100)
        self.cav.drawCentredString(x=100, y=100, text="100 100")
        # pathobject.lineTo(x,y)
        # 从画笔坐标点到x,y坐标点画一条直线
        pathobject.lineTo(x=100, y=200)
        self.cav.drawCentredString(x=100, y=200, text="100 200")

        # pathobject.curveTo(x1, y1, x2, y2, x3, y3)
        # curveTo方法从当前画笔位置开始
        # 使用（x1，y1）、（x2，y2）和（x3，y3）作为其他三个控制点绘制贝塞尔曲线
        # 画笔落在（x3，y3）的点上
        pathobject.moveTo(x=200, y=100)
        self.cav.setStrokeColor(aColor="red")
        self.cav.drawCentredString(x=200, y=90, text="200 100")
        self.cav.drawString(x=400, y=195, text="400 200")
        self.cav.drawCentredString(x=300, y=410, text="300 400")
        self.cav.line(200, 100, 400, 200)
        self.cav.line(400, 200, 300, 400)
        self.cav.setStrokeColor(aColor="black")
        pathobject.curveTo(200, 100, 400, 200, 300, 400)

        # pathobject.arc(x1,y1, x2,y2, startAng=0, extent=90)
        # Canvas对象的arc
        # pathobject.arc(x1=100,y1=500, x2=200,y2=580, startAng=0, extent=90)

        # pathobject.arcTo(x1,y1, x2,y2, startAng=0, extent=90)
        # 从当前画笔位置开始画
        # pathobject.arcTo(x1=100,y1=580, x2=300 ,y2=500, startAng=0, extent=90)
        # pathobject.rect(x, y, width, height)
        # pathobject.ellipse(x, y, width, height)
        # pathobject.circle(x_cen, y_cen, r)
        # pathobject.close()
        # 放下画笔
        pathobject.close()

        # drawPath方法绘制path object
        self.cav.drawPath(aPath=pathobject)

        # clipPath方法剪切path object？
        # self.cav.clipPath(aPath=pathobject)

        self.cav.bookmarkPage(key="draw_pathobj")
        self.show_cav()

    def draw_image(self):
        # drawImage 在页面中绘制一个图像
        # drawImage(self, image, x, y, width=None, height=None, mask=None,
        #           preserveAspectRatio=False, anchor='c', anchorAtXY=False, showBoundary=False)
        # 参数
        # image 一个ImageReader对象或者一个图片的文件名称
        # width|height 定义绘制图片的尺寸
        # mask
        # preserveAspectRatio
        # anchor
        # anchorAtXY
        # showBoundary
        image_path = "./img/logo2.png"
        img = Image.open(image_path)
        width, height = img.size
        self.cav.drawImage(image=image_path, x=10, y=10, width=width*0.8, height=height*0.8,
                           mask=None, preserveAspectRatio=False, anchor='c',
                           anchorAtXY=False, showBoundary=True)
        from reportlab.lib.utils import ImageReader
        from io import BytesIO

        image_path = "./img/logo.png"
        img = Image.open(image_path)
        width, height = img.size
        img_io = BytesIO()
        img.save(img_io, 'png')
        image = ImageReader(img_io)

        self.cav.drawImage(image=image, x=10, y=360, width=width, height=height,
                           mask=None, preserveAspectRatio=False, anchor='c',
                           anchorAtXY=False, showBoundary=True)

        self.cav.bookmarkPage(key="draw_image")
        self.show_cav()

    def change_color(self):
        self.set_font()
        # 设置颜色
        # CMYK模式是减色模式，相对应的RGB模式是加色模式
        # setFillColorCMYK 使用减色模式填充区域 接受4个介于0.0和1.0之间的参数
        # setStrokeColorCMYK 使用减色模式填充边框
        # alpha 设置填充颜色的透明度

        # self.cav.setFillColorCMYK(c=0.5, m=0.1, y=0.1, k=0.1, alpha=0.1)
        # self.cav.setStrokeColorCMYK(c=0.5, m=0.1, y=0.1, k=0.1, alpha=None)
        dx_cen = 0
        x_cen = 50+dx_cen
        y_cen = 750
        r = 25
        for cmyk in [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (0, 0, 0, 0)]:
            c, m, y, k = cmyk
            self.cav.setFillColorCMYK(c, m, y, k, alpha=0.8)
            self.cav.circle(x_cen=x_cen+dx_cen, y_cen=y_cen, r=r, fill=1)
            self.cav.setFillColorCMYK(c=0, m=0, y=0, k=1)
            self.cav.drawCentredString(
                x=x_cen+dx_cen, y=y_cen+r+10, text=f"CMYK:{cmyk}")
            dx_cen += 120

        # setFillColorRGB 使用RGB模式填充区域 接受3个介于0.0和1.0之间的参数
        # setStrokeColorRGB 使用RGB模式填充边框
        # self.cav.setFillColorRGB(r=0.5, g=0.5, b=0.5, alpha=None)
        # self.cav.setStrokeColorRGB(r=1, g=1, b=1, alpha=None)
        dx_cen = 0
        x_cen = 50+dx_cen
        y_cen = 650
        R = 25
        for rgb in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, 0), (1, 1, 1)]:
            r, g, b = rgb
            self.cav.setFillColorRGB(r, g, b, alpha=None)
            self.cav.circle(x_cen=x_cen+dx_cen, y_cen=y_cen, r=R, fill=1)
            self.cav.setFillColorRGB(r=0, g=0, b=0)
            self.cav.drawCentredString(
                x=x_cen+dx_cen, y=y_cen+R+10, text=f"RGB:{rgb}")
            dx_cen += 120

        # setFillGray 灰度；0.0=黑色，1.0=白色
        # gray_fill = 0.5
        # self.cav.setFillGray(gray=gray_fill)
        # gray_stroke = 0
        # self.cav.setStrokeGray(gray=gray_stroke)
        dx_cen = 0
        x_cen = 50+dx_cen
        y_cen = 550
        R = 25
        for gray in [0, 0.2, 0.4, 0.6, 0.8, 1]:
            self.cav.setFillGray(gray=gray)
            self.cav.circle(x_cen=x_cen+dx_cen, y_cen=y_cen, r=R, fill=1)
            self.cav.setFillGray(gray=0)
            self.cav.drawCentredString(
                x=x_cen+dx_cen, y=y_cen+R+10, text=f"Gray:{gray}")
            dx_cen += 100

        # 设置透明度
        self.cav.setFillAlpha(a=0.5)
        self.cav.setStrokeAlpha(a=0.2)

        # setFillColor 根据颜色对象填充区域 setStrokeColor填充边框
        # 参数 aColor  CMYKColor对象、Color对象、tuple、list 或者 Str，colors模块下颜色常量
        from reportlab.lib import colors
        # aColor == CMYKColor对象
        aColor = colors.CMYKColor(cyan=0.1, magenta=0.5,
                                  yellow=0.6, black=0.1,
                                  spotName=None, density=1,
                                  knockout=None, alpha=1)
        # aColor == list or tuple
        # list or tuple 的长度 只能是3(RGB)或者4(CYMK) 否则引发 ValueError
        aColor = (0.2, 0.3, 0.4)
        # aColor == Color对象
        aColor = colors.Color(red=0.5, green=0.6, blue=0.7)
        # aColor == Str
        # aColor 如果是Str类型则通过toColor对象转换
        # 'rgb(50 %, 0%, 0%)' 'rgba(255, 0, 0, 0.5)'
        aColor = 'rgba( 255,0,0,0.5)'
        # colors模块下颜色常量
        # aColor = colors.darkgray
        self.cav.setFillColor(aColor=aColor, alpha=None)
        self.cav.setStrokeColor(aColor=aColor, alpha=None)

        self.cav.bookmarkPage(key="change_color")
        self.show_cav()

    def set_line(self):
        self.set_font()

        # 设置线条样式
        # setLineWidth设置线条宽度
        self.cav.setLineWidth(width=5)
        self.cav.saveState()

        # setLineCap设置线条顶端样式  参数mode取值：0=butt,1=round,2=square 0=对接，1=圆形，2=方形
        dx = 0
        mode_dict = {0: 'butt', 1: 'round', 2: 'square'}
        for i in range(3):
            self.cav.setLineCap(mode=i)
            self.cav.lines(
                linelist=[(50+dx, 800, 100+dx, 800), (50+dx, 800, 70+dx, 700)])
            self.cav.drawCentredString(x=100+dx, y=810, text=f'setLineCap方法 mode={mode_dict[i]}')
            dx += 200

        # setLineJoin设置线条相交方式 参数mode取值：0=mitre, 1=round, 2=bevel 0=斜接，1=圆形，2=斜面
        # self.cav.setLineJoin(mode=1)

        dx = 0
        mode_dict = {0: 'mitre', 1: 'round', 2: 'bevel'}
        for i in mode_dict.keys():
            self.cav.setLineJoin(mode=i)
            self.cav.wedge(x1=50+dx, y1=400, x2=100+dx,
                           y2=600, startAng=0, extent=90)
            # self.cav.lines(
            #     linelist=[(50+dx, 600, 100+dx, 600), (50+dx, 600, 100+dx, 500), (100+dx, 500, 100+dx, 600)])
            self.cav.drawCentredString(x=100+dx, y=610, text=f'setLineJoin方法 mode={mode_dict[i]}')
            dx += 200

        # setMiterLimit

        # self.cav.setMiterLimit(limit=50)
        self.cav.setLineJoin(mode=0)
        self.cav.setMiterLimit(limit=1)
        self.cav.wedge(x1=50, y1=190, x2=100,
                       y2=390, startAng=0, extent=90)
        self.cav.drawCentredString(x=75, y=410, text=f'setLineJoin方法 mode=mitre')
        self.cav.drawCentredString(x=75, y=400, text=f'setMiterLimit方法 limit=1')

        self.cav.restoreState()

        # setDash 设置线条类型 将线拆分为点或破折号
        # setDash(array=[], phase=0)
        # 参数 array 绘制的点数 可以是一个数值 也可以是一个list
        # phase 间隔不绘制的点数
        dx = 0
        for arr, phase in zip([6, 3, (3, 2, 1), [1, 2, 3]], [3, 3, 3, 3]):
            self.cav.setDash(array=arr, phase=phase)
            self.cav.circle(x_cen=60+dx, y_cen=100, r=30)
            self.cav.line(x1=30+dx, y1=50, x2=90+dx, y2=50)
            self.cav.drawCentredString(x=60+dx, y=140, text=f'setDash arr={arr},phase={phase}')
            dx += 150
        self.cav.bookmarkPage(key="set_line")
        self.show_cav()

    def set_geometry(self):
        # 设置几何变换
        self.set_font()
        # setPageSize 设置页面大小
        self.cav.setPageSize(size=letter)

        # self.cav.setLineWidth(width=5)
        # self.cav.setFillColor(aColor="rgb(0,1,0)")
        # self.cav.grid([inch, 2*inch, 3*inch, 4*inch],
        #               [0.5*inch, inch, 1.5*inch, 2*inch, 2.5*inch])
        # self.cav.rect(0, 2*inch, 0.2*inch, 0.3*inch, fill=1)
        # self.cav.circle(4.5*inch, 0.4*inch, 0.2*inch, fill=1)
        # self.cav.setFillColor(aColor="rgb(0,0,0)")
        # self.cav.drawString(0, 0, "(0,0) the Origin")
        # self.cav.drawString(2.5*inch, inch, "(2.5,1) in inches")
        # self.cav.drawString(4*inch, 2.5*inch, "(4, 2.5)")

        # self.cav.rect(x=10, y=650, width=100, height=50, stroke=1, fill=1)

        # transform 矩阵转换
        # transform(a, b, c, d, e, f)
        # self.cav.transform(a=1, b=1, c=0, d=1, e=1, f=1)
        # self.show_cav()

        # translate 将原点从当前（0,0）点移动到（dx，dy）点
        self.cav.drawString(0, 0, "old:(0,0) the Origin")
        self.cav.translate(dx=50, dy=50)
        self.cav.drawString(0, 0, "new:(0,0) the Origin")

        self.cav.bookmarkPage(key="set_geometry")
        self.show_cav()

        # scale 按 x y 比例缩放
        # scale(x, y)
        # scale(x, y)==transform(x, 0, 0, y, 0, 0)
        self.set_font()
        x, y = 300, 400
        dx = dy = 0.5
        self.cav.drawCentredString(x, y, text="x, y = %s" % ([x, y]))
        self.cav.setFillColor(aColor="rgb(0.5,0.5,1)", alpha=0.5)
        self.cav.circle(x, y, 150, fill=1)
        self.cav.scale(x=dx, y=dy)
        self.cav.circle(x, y, 150, fill=1)
        self.cav.setFillColor(aColor="black", alpha=0.5)
        self.cav.drawCentredString(x, y, text="x, y = %s" % ([x*dx, y*dy]))

        self.cav.bookmarkPage(key="set_scale")
        self.show_cav()

        # rotate 将画布旋转 theta=角度
        # rotate(theta)
        # c = cos(theta * pi / 180)
        # s = sin(theta * pi / 180)
        # self.transform(c, s, -s, c, 0, 0)
        # self.cav.line(x1=100, y1=100, x2=100, y2=200)
        from math import cos, sin, pi, tan
        print(cos(45 * pi / 180))
        print(sin(45 * pi / 180))
        print(45 * pi / 180)
        print(tan(45 * pi / 180))

        for theta in range(60):
            self.cav.rotate(theta=1)
            self.cav.line(x1=450, y1=200, x2=550, y2=200)

        self.cav.bookmarkPage(key="set_rotate")
        self.show_cav()

        # skew(alpha, beta) 错切
        # tanAlpha = tan(alpha * pi / 180)
        # tanBeta = tan(beta * pi / 180)
        # self.transform(1, tanAlpha, tanBeta, 1, 0, 0)
        self.cav.setFillColor(aColor="red")
        self.cav.rect(x=300, y=10, width=25, height=50, fill=1)
        self.cav.skew(alpha=0, beta=45)
        self.cav.setFillColor(aColor="green")
        self.cav.rect(x=300, y=10, width=25, height=50, fill=1)

        self.cav.bookmarkPage(key="set_skew")
        self.show_cav()

    def control_cav_state(self):
        from reportlab.lib import colors
        # canvas.saveState()  保持画布当前的设置
        # canvas.restoreState() 清除画布在saveState之后的设置
        self.cav.setFillColor(aColor=colors.red)
        # 保存画布setFillColor(aColor=colors.red)的样式状态
        self.cav.saveState()

        self.cav.setFillColor(aColor=colors.green)
        self.cav.scale(2, 2)
        self.cav.circle(x_cen=2.5*inch, y_cen=3*inch, r=1*inch, fill=1)
        # 清除setFillColor(aColor=colors.green)和scale(2, 2)的样式状态
        self.cav.restoreState()
        self.cav.circle(x_cen=2.5*inch, y_cen=2*inch, r=1*inch, fill=1)

        self.cav.bookmarkPage(key="control_cav_state")
        self.show_cav()

    def set_other(self):
        from reportlab.lib import colors
        # canvas.setAuthor()
        self.cav.setAuthor("Mark")
        # canvas.setTitle(title)
        self.cav.setTitle(title="标题")
        # canvas.setSubject(subj)
        self.cav.setSubject(subject="主题")
        # canvas.getPageNumber() 获取当前PDF页数
        print("PageNumber", self.cav.getPageNumber())
        # canvas.pageHasData() 在showPage后调用它，查看是否需要保存
        print("pageHasData", self.cav.pageHasData())
        # canvas.getAvailableFonts() 返回可用PostScript字体名称的列表
        print("getAvailableFonts", self.cav.getAvailableFonts())

        # 设置PDF演示的页面转换效果
        # canvas.setPageTransition(self, effectname=None, duration=1,
        #                          direction=0, dimension='H', motion='I')
        # 参数 ：
        # direction_arg = [0, 90, 180, 270]
        # dimension_arg = ['H', 'V']
        # motion_arg = ['I', 'O'](start at inside or outside)
        # PageTransitionEffects = {
        #         'Split': [direction_arg, motion_arg],
        #         'Blinds': [dimension_arg],
        #         'Box': [motion_arg],
        #         'Wipe' : [direction_arg],
        #         'Dissolve' : [],
        #         'Glitter':[direction_arg]
        #         }
        self.cav.setPageTransition(
            effectname='Split', duration=1, direction=0, dimension='H', motion='I')

        # canvas.bookmarkPage(name) 当前页面创建一个书签
        # self.cav.bookmarkPage(key="mark_key")
        # canvas.addOutlineEntry(title, key, level=0, closed=None)
        # 设置书签目录 title名称 key对应的书签 level目录级别  closed是否展开子目录 默认展开
        self.cav.addOutlineEntry(
            title="绘制字符串", key="draw_str", level=0, closed=None)
        self.cav.addOutlineEntry(
            title="绘制直线", key="draw_line", level=0, closed=None)
        self.cav.addOutlineEntry(
            title="绘制形状", key="draw_shape", level=0, closed=None)
        self.cav.addOutlineEntry(
            title="绘制图片", key="draw_image", level=0, closed=None)
        self.cav.addOutlineEntry(
            title="改变颜色", key="change_color", level=0, closed=None)
        self.cav.addOutlineEntry(
            title="线条样式", key="set_line", level=0, closed=None)
        self.cav.addOutlineEntry(
            title="几何变换", key="set_geometry", level=0, closed=None)
        self.cav.addOutlineEntry(
            title="画布缩放", key="set_scale", level=1, closed=None)
        self.cav.addOutlineEntry(
            title="画布旋转", key="set_rotate", level=1, closed=1)
        self.cav.addOutlineEntry(
            title="下一级", key="set_skew", level=2, closed=None)

        # canvas.showOutline() 设置默认显示大纲目录
        self.cav.showOutline()
        # 全屏模式打开
        # self.cav.showFullScreen0()
        # canvas.bookmarkHorizontalAbsolute(name, yhorizontal)
        # canvas.doForm()

        # canvas.beginForm(name, lowerx=0, lowery=0, upperx=None, uppery=None)
        # canvas.endForm()
        # canvas.linkAbsolute(contents, destinationname,
        #                     Rect=None, addtopage=1, name=None, **kw)
        # canvas.linkRect(contents, destinationname, Rect=None,
        #                 addtopage=1, relative=1, name=None, **kw)

        # canvas.addLiteral()
        # canvas.stringWidth(self, text, fontName, fontSize, encoding=None)
        print("stringWidth方法", self.cav.stringWidth(
            text="宋体", fontName="simsun", fontSize=10))
        # canvas.setPageCompression(onoff=1)

        self.cav.bookmarkPage(key="set_other")
        self.show_cav()

    def size(self):
        print("inch", inch)
        print("letter", letter)
        print("A4", A4)

    def set_grad(self):
        # 绘制方格
        start, step = 50, 120
        X_end = 580
        Y_end = 830
        x_list = self.get_grad_XY_list(start, X_end, step)
        y_list = self.get_grad_XY_list(start, Y_end, step)
        self.cav.grid(xlist=x_list, ylist=y_list)
        self.set_broken_line(xlist=x_list, ylist=y_list)
        self.set_Text(xlist=x_list, ylist=y_list, step=step, size=120)

    def get_grad_XY_list(self, start, end, step):
        return [x for x in range(start, end, step)]

    def set_broken_line(self, xlist, ylist):
        linelist = list()
        X_len = len(xlist)
        Y_len = len(ylist)
        max_len = max(X_len, Y_len)
        for x_indx in range(0, X_len-1):
            for y_indx in range(0, Y_len-1):
                x1, y1 = xlist[x_indx], ylist[y_indx]
                x2, y2 = xlist[x_indx+1], ylist[y_indx+1]
                linelist.append((x1, y1, x2, y2))

                x1, y1 = xlist[x_indx+1], ylist[y_indx]
                x2, y2 = xlist[x_indx], ylist[y_indx+1]
                linelist.append((x1, y1, x2, y2))
        self.set_broken_style()
        self.cav.lines(linelist=linelist)

    def set_broken_style(self):
        # 设置对折线样式
        self.cav.setStrokeGray(gray=0.8, alpha=0.5)
        self.cav.setDash(array=[1], phase=2)

    def set_Text(self, xlist, ylist, step, size):
        text = "宋"
        self.cav.setFont(psfontname="simsun", size=size)
        self.cav.drawCentredString(
            x=xlist[0]+step/2, y=ylist[0]+size/5, text=text)


def star(canvas, title="Title Here", aka="Comment here.",
         xcenter=None, ycenter=None, nvertices=5):
    # 五角星实例 手册源码
    from math import pi
    from reportlab.lib.units import inch
    radius = inch/3.0
    if xcenter is None:
        xcenter = 2.75*inch
    if ycenter is None:
        ycenter = 1.5*inch
    canvas.drawCentredString(xcenter, ycenter+1.3*radius, title)
    canvas.drawCentredString(xcenter, ycenter-1.4*radius, aka)
    p = canvas.beginPath()
    p.moveTo(xcenter, ycenter+radius)
    from math import pi, cos, sin
    angle = (2*pi)*2/5.0
    startangle = pi/2.0
    for vertex in range(nvertices-1):
        nextangle = angle*(vertex+1)+startangle
        x = xcenter + radius*cos(nextangle)
        y = ycenter + radius*sin(nextangle)
        p.lineTo(x, y)
    if nvertices == 5:
        p.close()
    canvas.drawPath(p)


def caps(canvas):
    from reportlab.lib.units import inch
    # make lines big
    canvas.setLineWidth(5)
    star(canvas, "Default", "no projection", xcenter=1*inch,
         nvertices=4)
    canvas.setLineCap(1)
    star(canvas, "Round cap", "1: ends in half circle", nvertices=4)
    canvas.setLineCap(2)
    star(canvas, "Square cap", "2: projects out half a width", xcenter=4.5*inch,
         nvertices=4)


def joins(canvas):
    from reportlab.lib.units import inch
    # make lines big
    canvas.setLineWidth(5)
    star(canvas, "Default: mitered join", "0: pointed", xcenter=1*inch)
    canvas.setLineJoin(1)
    star(canvas, "Round join", "1: rounded")
    canvas.setLineJoin(2)
    star(canvas, "Bevelled join", "2: square", xcenter=4.5*inch)


if __name__ == "__main__":
    r = DemoReportLab()
    r.size()
    r.draw_PDF()
    # cav = canvas.Canvas(filename="star.pdf")
    # joins(cav)
    # cav.showPage()
    # cav.save()
