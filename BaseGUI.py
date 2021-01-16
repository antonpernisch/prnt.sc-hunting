import wx

class GUIPanel(wx.Panel):
    def __init__(self, parent):
        # declare sizer
        super().__init__(parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)


        # create StaticBox for attack pattern
        self.attackPatternBox = wx.StaticBox(self, -1, "Attack Pattern")
        self.attackPatternBox_sizer = wx.StaticBoxSizer(self.attackPatternBox, wx.VERTICAL)

        self.apbox_content_sizer = wx.BoxSizer(wx.VERTICAL)

        # insert objects into attack pattern box
        self.text_ctrl = wx.TextCtrl(self, -1, style=wx.ALIGN_LEFT)
        self.apbox_content_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.LEFT, 10)
        self.attackPatternBox_sizer.Add(self.apbox_content_sizer, 0, wx.ALL | wx.LEFT, 10)

        # add objects to sizers
        self.main_sizer.Add(self.attackPatternBox_sizer, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(self.main_sizer)
        
class GUIFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, size=(400,600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX, title="Screenshot hunting tool (prnt.sc)")

        # set some shitty icon, honestly it sucks but whatever
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("Assets/app_icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        # post-init
        self.panel = GUIPanel(self)
        self.create_menu()
        self.Show()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        help_menu = wx.Menu()
        about__help_menu_item = help_menu.Append(wx.ID_ANY, "About", "Show info about current build and author")
        menu_bar.Append(help_menu, "&Help")
        self.Bind(event=wx.EVT_MENU, handler=self.on_about_open, source=about__help_menu_item)
        self.SetMenuBar(menu_bar)

    def on_about_open(self, event):
        AboutDialog(self).ShowModal()

class AboutDialog(wx.Dialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent, title="About", size=(250,150))
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self)

        aboutText = wx.StaticText(panel, -1, "aa\ndd")
        self.about_btn = wx.Button(panel, wx.ID_CANCEL, label = "Cancel")

        self.hsizer.Add(self.about_btn, 0, wx.ALL|wx.EXPAND, 5)
        self.hsizer2.Add(aboutText, 0, wx.ALL|wx.EXPAND, 5)

        self.vsizer.Add(self.hsizer2, 1, wx.EXPAND)
        self.vsizer.Add(self.hsizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        panel.SetSizer(self.vsizer)


if __name__ == "__main__":
    app = wx.App(False)
    frame = GUIFrame()
    app.MainLoop()