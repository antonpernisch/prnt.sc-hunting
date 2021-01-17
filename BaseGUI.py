import wx
import wx.lib.agw.pygauge as PG

class ValuesBin:
    def __init__(self):
        self.textCtrl__letters = ""
        self.spinCtrl__startNum = ""
        self.spinCtrl__amount = ""
        self.pattern_example_text__example = ""
        self.textCtrl__output = ""
        self.progressBar = ""
        self.startBtn = ""
        self.attackPattern = ""
        return

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
        ValuesBin.attackPattern = wx.ComboBox(self, choices=self.attack_patterns, style=wx.CB_READONLY)
        ValuesBin.attackPattern.SetSelection(0)
        ValuesBin.attackPattern.Bind(wx.EVT_COMBOBOX, self.update_pattern_example)

        self.pattern_example_text__guide = wx.StaticText(self, -1, "Example of selected pattern:")
        ValuesBin.pattern_example_text__example = wx.StaticText(self, -1, label="https://prnt.sc/hw6372")

        self.apbox_content_sizer.Add(self.choose_attackPattern_text, 0, wx.BOTTOM, border=5)
        self.apbox_content_sizer.Add(ValuesBin.attackPattern, 0, wx.ALL | wx.EXPAND)

        self.apbox_content_sizer.Add(self.pattern_example_text__guide, 0, wx.TOP, border=15)
        self.apbox_content_sizer.Add(ValuesBin.pattern_example_text__example, 0, wx.TOP, border=5)

        self.attackPatternBox_sizer.Add(self.apbox_content_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # add objects to sizers
        self.main_sizer.Add(self.attackPatternBox_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # continue adding to attack options box
        self.attackOptionsBox = wx.StaticBox(self, -1, "ATTACK OPTIONS")
        self.attackOptionsBox_sizer = wx.StaticBoxSizer(self.attackOptionsBox, wx.VERTICAL)

        self.flex_hbox_options = wx.BoxSizer(wx.HORIZONTAL)
        self.flex_options = wx.FlexGridSizer(2, 2, 10,50)
        
        # sub-sizers for labels of options
        sizer__letters = wx.BoxSizer(wx.HORIZONTAL)
        sizer__startNum = wx.BoxSizer(wx.HORIZONTAL)
        sizer__blank = wx.BoxSizer(wx.HORIZONTAL)
        sizer__amount = wx.BoxSizer(wx.HORIZONTAL)

        # options
        self.label__letters = wx.StaticText(self, -1, "Letters:")
        ValuesBin.textCtrl__letters = wx.TextCtrl(self, size=(35, 22))
        
        self.label__startNum = wx.StaticText(self, -1, "Start from:")
        ValuesBin.spinCtrl__startNum = wx.SpinCtrl(self, -1, min=0, max=8999, initial=0)

        self.label__amount = wx.StaticText(self, -1, "Download amount:")
        ValuesBin.spinCtrl__amount = wx.SpinCtrl(self, -1, min=7, max=1000, initial=200)

        sizer__letters.Add(self.label__letters, 0, wx.RIGHT, 10)
        sizer__letters.Add(ValuesBin.textCtrl__letters, 0, wx.ALL, 0)
        sizer__startNum.Add(self.label__startNum, 0, wx.RIGHT, 10)
        sizer__startNum.Add(ValuesBin.spinCtrl__startNum, 0, wx.ALL, 0)
        sizer__amount.Add(self.label__amount, 0, wx.RIGHT, 10)
        sizer__amount.Add(ValuesBin.spinCtrl__amount, 0, wx.ALL, 0)

        # flexbox
        self.flex_options.AddMany([(sizer__letters), (sizer__startNum), (sizer__blank), (sizer__amount)])
        self.flex_hbox_options.Add(self.flex_options, proportion=2, flag=wx.ALL|wx.EXPAND, border=15)
        self.attackOptionsBox_sizer.Add(self.flex_hbox_options, 0, wx.EXPAND)

        self.main_sizer.Add(self.attackOptionsBox_sizer, 0, wx.ALL | wx.EXPAND, 10)

        # progress bar
        ValuesBin.progressBar = wx.Gauge(self, -1)
        self.main_sizer.Add(ValuesBin.progressBar, 0, wx.ALL | wx.EXPAND, 10)

        # output
        sizer__output = wx.BoxSizer(wx.HORIZONTAL)
        self.textCtrl__output_title = wx.StaticText(self, -1, "Output:")
        ValuesBin.textCtrl__output = wx.StaticText(self, -1, "Waiting for user...")
        ValuesBin.textCtrl__output.SetForegroundColour((100,100,100))
        sizer__output.Add(self.textCtrl__output_title, 0)
        sizer__output.Add(ValuesBin.textCtrl__output, 0, wx.LEFT, 15)

        self.main_sizer.Add(sizer__output, 0, wx.LEFT | wx.EXPAND, 10)

        # start button
        text__blank = wx.StaticText(self, -1, "")
        ValuesBin.startBtn = wx.Button(self, label="Start downloading", size=(0,80))
        ValuesBin.startBtn.Bind(wx.EVT_BUTTON, self.on_startBtn)
        self.main_sizer.Add(text__blank, 0, wx.TOP, 10)
        self.main_sizer.Add(ValuesBin.startBtn, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)

        self.SetSizer(self.main_sizer)

    def on_startBtn(self, event):
        HunterBridge()

    def update_pattern_example(self, event):
        # too lazy to randomize it, maybe later lol
        if ValuesBin.attackPattern.GetSelection() == 0:
            ValuesBin.pattern_example_text__example.SetLabel("https://prnt.sc/hw6372")
            ValuesBin.textCtrl__letters.Enable(True)
            ValuesBin.spinCtrl__startNum.Enable(True)
        elif ValuesBin.attackPattern.GetSelection() == 1:
            ValuesBin.pattern_example_text__example.SetLabel("https://prnt.sc/7da52c")
            ValuesBin.textCtrl__letters.Enable(False)
            ValuesBin.spinCtrl__startNum.Enable(False)
        
class GUIFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, size=(400,520), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX, title="Screenshot hunting tool (prnt.sc)")

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
        file_menu = wx.Menu()
        about__help_menu_item = help_menu.Append(wx.ID_ANY, "About", "Show info about current build and author")
        download_folder__file_menu_item = file_menu.Append(wx.ID_ANY, "Download folder", "Let's you choose download folder")
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")
        self.Bind(event=wx.EVT_MENU, handler=self.on_about_open, source=about__help_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_download_folder_open, source=download_folder__file_menu_item)
        self.SetMenuBar(menu_bar)

    def on_about_open(self, event):
        AboutDialog(self).ShowModal()

    def on_download_folder_open(self, event):
        dlg = wx.DirDialog(self, "Choose where the downloaded screenshots will go:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.download_folder_path = dlg.GetPath()
        dlg.Destroy()

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

class HunterBridge:
    def __init__(self):
        from Hunter import Hunter
        ValuesBin.startBtn.Enable(False)
        ValuesBin.textCtrl__output.SetLabel("Sending values to Hunter, expecting response...")
        ValuesBin.textCtrl__output.SetForegroundColour((0, 153, 204))
        ValuesBin.progressBar.Pulse()
        Hunter.pattern = ValuesBin.attackPattern.GetSelection()
        Hunter.letters = ValuesBin.textCtrl__letters.GetValue()
        Hunter.startingNum = ValuesBin.spinCtrl__startNum.GetValue()
        Hunter.amount = ValuesBin.spinCtrl__amount.GetValue()
        Hunter.startup(Hunter)

if __name__ == "__main__":
    app = wx.App(False)
    frame = GUIFrame()
    app.MainLoop()