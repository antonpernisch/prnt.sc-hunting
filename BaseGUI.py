import wx

class GUIPanel(wx.Panel):
    def __init__(self, parent):
        # declare sizer
        super().__init__(parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)


        # create StaticBox for attack pattern
        self.attackPatternBox = wx.StaticBox(self, -1, "ATTACK PATTERN")
        self.attackPatternBox_sizer = wx.StaticBoxSizer(self.attackPatternBox, wx.VERTICAL)

        self.apbox_content_sizer = wx.BoxSizer(wx.VERTICAL)

        # insert objects into attack pattern box
        self.choose_attackPattern_text = wx.StaticText(self, -1, "Choose attack pattern:")
        self.attack_patterns = ["Two letters at the beggining, followed by 4 numbers", "Random 6-digit sequence"]
        self.attackPattern = wx.ComboBox(self, choices=self.attack_patterns, style=wx.CB_READONLY)
        self.attackPattern.SetSelection(0)
        self.attackPattern.Bind(wx.EVT_COMBOBOX, self.update_pattern_example)

        self.pattern_example_text__guide = wx.StaticText(self, -1, "Example of selected pattern:")
        self.pattern_example_text__example = wx.StaticText(self, -1, label="https://prnt.sc/hw6372")

        self.apbox_content_sizer.Add(self.choose_attackPattern_text, 0, wx.BOTTOM, border=5)
        self.apbox_content_sizer.Add(self.attackPattern, 0, wx.ALL | wx.EXPAND)

        self.apbox_content_sizer.Add(self.pattern_example_text__guide, 0, wx.TOP, border=15)
        self.apbox_content_sizer.Add(self.pattern_example_text__example, 0, wx.TOP, border=5)

        self.attackPatternBox_sizer.Add(self.apbox_content_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # add objects to sizers
        self.main_sizer.Add(self.attackPatternBox_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # continue adding to attack options box
        self.attackOptionsBox = wx.StaticBox(self, -1, "ATTACK OPTIONS")
        self.attackOptionsBox_sizer = wx.StaticBoxSizer(self.attackOptionsBox, wx.VERTICAL)

        self.aobox_content_sizer = wx.BoxSizer(wx.VERTICAL)

        self.main_sizer.Add(self.attackOptionsBox_sizer, 0, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(self.main_sizer)

    def update_pattern_example(self, event):
        # too lazy to randomize it, maybe later lol
        if self.attackPattern.GetSelection() == 0:
            self.pattern_example_text__example.SetLabel("https://prnt.sc/hw6372")
        elif self.attackPattern.GetSelection() == 1:
            self.pattern_example_text__example.SetLabel("https://prnt.sc/7da52c")
        
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
        super(AboutDialog, self).__init__(parent, title="About", size=(300,250))
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self)

        aboutText = wx.StaticText(panel, -1, "Screenshot hunting tool\nfor hunting personal information\nfrom prnt.sc service.\nCreated and developed by Anton Pernisch\n\n\n\nSoftware under GNU GPLv3 license.\n(c) Anton Pernisch 2021")
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