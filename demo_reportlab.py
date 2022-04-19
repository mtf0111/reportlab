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
        # bottomup已弃用 为了转换坐标
        # pageCompression 是否对PDF操作进行压缩，默认情况下不被压缩，压缩会减慢运行速度\
        # 如果页面有大量的文本和矢量图形的话压缩会节省空间
        # encrypt 如果赋值一个字符串的话 将会作为PDF的用户密码使用
        self.cav = canvas.Canvas(
            filename=self.filename, pagesize=None, bottomup=1,
            pageCompression=1, encrypt=None)
        self.page_width, self.page_height = self.pagesize = self.cav._pagesize

    def register_Font(self):
        # 注册字体解决中文显示问题
        pdfmetrics.registerFont(font=ttfonts.TTFont(
            name="simsun", filename=self.simsun_FONT_PATH))

    def draw_PDF(self):
        # 设置字体
        self.set_font()
        self.draw_str()
        self.draw_line()
        self.draw_shape()
        self.draw_textobj()
        self.draw_pathobj()
        self.draw_image()
        self.show_cav()
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
        self.cav.drawRightString(x, y+10, "drawRightString "+text)
        self.cav.drawCentredString(x, y-10, "drawCentredString "+text)
        # self.cav.drawAlignedString(x, y-20, "drawAlignedString "+text)
        # self.show_cav()

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
        # 绘制直线
        # x1和y1 作为起点坐标 x2和y2 作为终点坐标 画一条直线
        self.cav.line(x1=300, y1=410, x2=420, y2=410)
        # 存放多条线的坐标
        crosshairs = [(300, 400, 420, 400),
                      (300, 390, 420, 390), ]
        # 画多条线 参数 linelist 存放多条线的坐标
        self.cav.lines(linelist=crosshairs)

        # self.show_cav()

    def draw_shape(self):
        # 绘制形状

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
        xlist = [10, 100, 190, 280]
        # ylist 中Y坐标轴数据等差 画等距地竖线
        ylist = [30, 120, 210, 300]
        self.cav.grid(xlist=xlist, ylist=ylist)

        # self.cav.bezier(x1=10, y1=10, x2=20, y2=20, x3=30, y3=30, x4=40, y4=40)

        # arc 在矩形x1，y1，x2，y2内画一个椭圆 从startAng度开始逆时针画extent度
        self.cav.arc(x1=0, y1=0, x2=590, y2=800, startAng=0, extent=360)

        # wedge 绘制一个扇形？参数同arc
        self.cav.wedge(x1=0, y1=0, x2=200, y2=500, startAng=0, extent=30)

        # rect 绘制矩形
        self.cav.rect(x=450, y=30, width=40, height=300, stroke=1, fill=0)

        # ellipse 在一个封闭的矩形内绘制一个椭圆
        self.cav.ellipse(x1=0, y1=0, x2=200, y2=300, stroke=1, fill=0)

        # circle 绘制一个圆形 x_cen 圆心的X坐标 y_cen圆心的Y坐标 r 圆的半径
        self.cav.circle(x_cen=100, y_cen=100, r=50, stroke=1, fill=0)

        # roundRect 绘制一个圆角的矩形 radius参数是矩形四个角圆形的半径 类似CSS的border-radius？
        self.cav.roundRect(x=300, y=300, width=200,
                           height=100, radius=50, stroke=1, fill=0)

    def draw_textobj(self):
        # text object beginText方法创建一个text对象 通过调研text对象的方法进行格式化文本，
        # 然后用drawText方法将text对象绘制到页面上
        textobj = self.cav.beginText(x=300, y=200, direction=None)
        # text 对象的一些方法：
        # setTextOrigin 重置 text对象的坐标
        textobj.setTextOrigin(x=0, y=0)
        # setTextTransform(a, b, c, d, e, f) 与setTextOrigin类似，但有旋转、缩放等功能
        # textobj.setTextTransform(a, b, c, d, e, f)
        # getCursor getX getY 获取text对象的坐标
        print("getCursor()方法 获取坐标tuple", textobj.getCursor())
        print("getX()方法 获取X坐标", textobj.getX())
        print("getY()方法 获取Y坐标", textobj.getY())
        # setFont 设置字体
        textobj.setFont(psfontname="simsun", size=50, leading=None)
        textobj.textLine(text="这是text对象")
        self.cav.drawText(aTextObject=textobj)

    def draw_pathobj(self):
        # path object类似于text object path对象提供了可以执行复杂图像绘制的方法，
        # beginPath方法 返回PDFPathObject
        path_obj = self.cav.beginPath()
        path_obj.circle(x_cen=50, y_cen=50, r=50)
        # drawPath方法绘制path object
        self.cav.drawPath(aPath=path_obj, stroke=1, fill=1, fillMode=None)

        # clipPath方法剪切path object？
        self.cav.clipPath(aPath=path_obj, stroke=1, fill=1, fillMode=None)

    def draw_image(self):
        # drawImage 在页面中绘制一个图像
        # 参数
        # image 一个ImageReader对象或者一个图片的文件名称
        # width|height 定义绘制图片的尺寸
        # mask
        from reportlab.lib.utils import ImageReader
        from io import BytesIO
        self.show_cav()

        image_path = "./img/logo.png"
        img = Image.open(image_path)
        width, height = img.size
        img_io = BytesIO()
        img.save(img_io, 'png')
        image = ImageReader(img_io)

        # image = "./img/logo.png"
        self.cav.drawImage(image=image, x=0, y=0, width=width, height=height,
                           mask=None, preserveAspectRatio=False, anchor='c',
                           anchorAtXY=False, showBoundary=False)

    def size(self):
        print("inch", inch)
        print("letter", letter)
        print("A4", A4)


if __name__ == "__main__":
    r = DemoReportLab()
    r.size()
    r.draw_PDF()
