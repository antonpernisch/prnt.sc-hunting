import wx

class GUIPanel(wx.Panel):
    def __init__(self, parent):
        # declare sizer
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # insert objects

        self.attackType_box = wx.StaticBox(self, wx.ID_ANY, "Attack type selection", size=(240, 140))
        self.text_ctrl = wx.TextCtrl(self.attackType_box)
        main_sizer.Add(self.attackType_box, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(main_sizer)
        
class GUIFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, size=(400,600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX, title="Screenshot hunting tool (prnt.sc)")

        # set some shitty icon, honestly it sucks but whatever
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("Assets/app_icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        # post-init
        self.panel = GUIPanel(self)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = GUIFrame()
    app.MainLoop()