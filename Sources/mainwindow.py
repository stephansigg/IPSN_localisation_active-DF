import wx
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname=''       
        wx.Frame.__init__(self, parent, title=title, size=(200,-1))
        #self.quote = wx.StaticText(self, label="Your quote :", pos=(20, 30))

        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, pos=(500,20), size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

        #  button
        self.button =wx.Button(self, label="Start Recording", pos=(50, 100))
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
        
        self.button =wx.Button(self, label="Stop Recording", pos=(200, 100))
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
        
        self.button =wx.Button(self, label="Pause", pos=(350, 100))
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

        # the edit control - one line version.
        self.lblname = wx.StaticText(self, label="Coodinator (Room, Row, Column)  :", pos=(20,60))
        self.editname = wx.TextCtrl(self, value="Enter Coordinator", pos=(270, 60), size=(200,-1))
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)
    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
app = wx.App(False)
frame = MainWindow(None, "Indoor Location Learning")
frame.Show()
app.MainLoop()
  
