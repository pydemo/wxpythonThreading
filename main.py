import wx
from threading import Thread
from wx.lib.newevent import NewEvent
import sysinfo


class ThreadClass(Thread):
    # Custom event for data sharing
    pc_info, EVT_DATA = NewEvent()

    def __init__(self, parent):
        Thread.__init__(self)
        self.parent = parent
        # local thread flag
        self.threadFlag = False

    def setThreadFlag(self,s):
        # Set function to control local thread flag
        self.threadFlag = s

    def run(self):
        # check local thread flag
        while self.threadFlag:
            # do the work under this thread instance
            cpu = sysinfo.getCPU()
            ram = sysinfo.getRAM()
            result = {'cpu': cpu, 'ram': ram}
            # update custom event pointer
            wx.PostEvent(self.parent, self.pc_info(data=result))

    def close(self):
        # Set thread flag for terminating
        self.threadFlag = False
        # Terminate thread instance
        self.join(1)


class widgetPanel(wx.Panel):
    """
    Custom widget panel
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.uiInit()
        # Thread class flag
        self.threadcls = None

        # Bind the thread class custom event to this panel
        self.Bind(ThreadClass.EVT_DATA, self.updateUi)
        # Toggle button to launch/terminate single thread
        self.m_button1.Bind(wx.EVT_TOGGLEBUTTON, self.onToggle)

    def uiInit(self):
        """
        :return:
        UI designed using wxFormBuilder
        """
        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"CPU Usage", wx.DefaultPosition, wx.DefaultSize,wx.ALIGN_CENTER_HORIZONTAL)
        # self.m_staticText1.Wrap(-1)

        self.m_staticText1.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,False, wx.EmptyString))
        self.m_staticText1.SetMinSize(wx.Size(100, -1))

        bSizer5.Add(self.m_staticText1, 0, wx.ALL | wx.LEFT, 5)

        self.gauge = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        # self.gauge.SetValue(0)
        self.gauge.SetMinSize(wx.Size(250, 20))

        bSizer5.Add(self.gauge, 0, wx.ALL, 5)

        bSizer2.Add(bSizer5, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"RAM", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.m_staticText2.Wrap(-1)

        self.m_staticText2.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,False, wx.EmptyString))
        self.m_staticText2.SetMinSize(wx.Size(100, -1))

        bSizer3.Add(self.m_staticText2, 0, wx.ALL | wx.LEFT, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.a = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.a.Wrap(-1)

        bSizer4.Add(self.a, 0, wx.ALL, 5)

        self.b = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.b.Wrap(-1)

        bSizer4.Add(self.b, 0, wx.ALL, 5)

        self.c = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.c.Wrap(-1)

        bSizer4.Add(self.c, 0, wx.ALL, 5)

        self.d = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.d.Wrap(-1)

        bSizer4.Add(self.d, 0, wx.ALL, 5)

        self.e = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.e.Wrap(-1)

        bSizer4.Add(self.e, 0, wx.ALL, 5)

        bSizer3.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer2.Add(bSizer3, 1, wx.EXPAND, 5)

        self.m_button1 = wx.ToggleButton(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button1.SetMinSize(wx.Size(50, 50))

        bSizer2.Add(self.m_button1, 0, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

    def updateUi(self, event):
        """
        :param event:
        :return:
        """
        print(event.data)
        # total = 12792926208, available = 8587247616, percent = 32.9, used = 4205678592, free = 8587247616
        self.gauge.SetValue(event.data['cpu'])
        self.a.SetLabel(str(event.data['ram']['total']))
        self.b.SetLabel(str(event.data['ram']['available']))
        self.c.SetLabel(str(event.data['ram']['percent']))
        self.d.SetLabel(str(event.data['ram']['used']))
        self.e.SetLabel(str(event.data['ram']['free']))

    def onToggle(self, event):
        """
        :param event:
        :return:
        """
        # Get toggle button status
        toggleBtnstate = event.GetEventObject().GetValue()

        print(toggleBtnstate)
        if toggleBtnstate is True:
            # Init a Thread
            self.threadcls = ThreadClass(self)
            # Toggle button caption
            self.m_button1.SetLabel("Stop")
            # Thread class flag for Run
            self.threadcls.setThreadFlag(True)
            # Start thread
            self.threadcls.start()

        else:
            # Toggle button caption
            self.m_button1.SetLabel("Start")
            # Thread class flag for Run
            self.threadcls.setThreadFlag(False)
            # Terminate thread
            self.threadcls.close()

    def close(self):
        # class thread flag
        if self.threadcls is not None:
            # Terminate thread
            self.threadcls.close()
        # Terminate widget on application exit
        self.Destroy()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='wxpython single threading', size=(560, 300))
        # widget panel instance
        self.panel = panel = widgetPanel(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        # Terminate Frame on close
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        # close widget panel
        self.panel.close()
        # terminate frame on application closing
        self.Destroy()


def app0():
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    app0()




