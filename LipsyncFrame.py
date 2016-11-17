# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.3.5.1 on Wed Apr 13 16:04:35 2005

# Papagayo-NG, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
# Contact information at http://www.lostmarble.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#import os
import string
import math
#import wx
import webbrowser
import re
# from utilities import *
# begin wxGlade: dependencies
from MouthView import MouthView
from WaveformView import WaveformView
# end wxGlade

from AboutBox import AboutBox
from LipsyncDoc import *

appTitle = "Papagayo-NG"
lipsyncExtension = ".pgo"
audioExtensions = "*.wav;*.mp3;*.aiff;*.aif;*.au;*.snd;*.mov;*.m4a"
openWildcard = "%s and sound files|*%s;%s" % (appTitle, lipsyncExtension, audioExtensions)
openAudioWildcard = "Sound files|%s" % (audioExtensions)
saveWildcard = "%s files (*%s)|*%s" % (appTitle, lipsyncExtension, lipsyncExtension)


class DigitOnlyValidator(wx.PyValidator):
    def __init__(self, flag=None, pyVar=None):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return DigitOnlyValidator()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        for x in val:
            if x not in string.digits:
                return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits:
            event.Skip()
            return

        # Returning without calling event.Skip() eats the event before it
        # gets to the text control
        return


class LipsyncFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: LipsyncFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        # Menu Bar
        self.mainFrame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_OPEN, _("&Open...\tCtrl+O"), _("Open a sound file or Papagayo-NG project"),
                                wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_SAVE, _("&Save\tCtrl+S"), _("Save this lipsync project"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_SAVEAS, _("Save &As..."), _("Save this Papagayo-NG project under a new name"),
                                wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_EXIT, _("Exit"), _("Quit Papagayo-NG"), wx.ITEM_NORMAL)
        self.mainFrame_menubar.Append(wxglade_tmp_menu, _("&File"))
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_UNDO, _("&Undo\tCtrl+Z"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_CUT, _("Cu&t\tCtrl+X"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_COPY, _("&Copy\tCtrl+C"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_PASTE, _("&Paste\tCtrl+V"), "", wx.ITEM_NORMAL)
        self.mainFrame_menubar.Append(wxglade_tmp_menu, _("&Edit"))
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_HELP, _("&Help Topics"), _("Open the user's manual"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(wx.ID_ABOUT, _("&About Papagayo-NG..."), _("Display information about Papagayo-NG"),
                                wx.ITEM_NORMAL)
        self.mainFrame_menubar.Append(wxglade_tmp_menu, _("&Help"))
        self.SetMenuBar(self.mainFrame_menubar)
        # Menu Bar end
        self.mainFrame_statusbar = self.CreateStatusBar(2)

        # Tool Bar
        self.mainFrame_toolbar = wx.ToolBar(self, -1, style=wx.TB_FLAT | wx.TB_HORIZONTAL)
        self.SetToolBar(self.mainFrame_toolbar)
        global ID_PLAY
        ID_PLAY = wx.NewId()
        global ID_STOP
        ID_STOP = wx.NewId()
        global ID_ZOOMIN
        ID_ZOOMIN = wx.NewId()
        global ID_ZOOMOUT
        ID_ZOOMOUT = wx.NewId()
        global ID_ZOOM1
        ID_ZOOM1 = wx.NewId()
        self.mainFrame_toolbar.AddLabelTool(wx.ID_OPEN, _("Open"),
                                            wx.Bitmap(os.path.join(get_main_dir(), "rsrc/open.png")), wx.NullBitmap,
                                            wx.ITEM_NORMAL, _("Open"), _("Open a sound file or Papagayo-NG project"))
        self.mainFrame_toolbar.AddLabelTool(wx.ID_SAVE, _("Save"),
                                            wx.Bitmap(os.path.join(get_main_dir(), "rsrc/save.png")), wx.NullBitmap,
                                            wx.ITEM_NORMAL, _("Save"), _("Save this Papagayo-NG project"))
        self.mainFrame_toolbar.AddSeparator()
        self.mainFrame_toolbar.AddLabelTool(ID_PLAY, _("Play"),
                                            wx.Bitmap(os.path.join(get_main_dir(), "rsrc/play.png")), wx.NullBitmap,
                                            wx.ITEM_NORMAL, _("Play"), _("Play the sound clip"))
        self.mainFrame_toolbar.AddLabelTool(ID_STOP, _("Stop"),
                                            wx.Bitmap(os.path.join(get_main_dir(), "rsrc/stop.png")), wx.NullBitmap,
                                            wx.ITEM_NORMAL, _("Stop"), _("Stop playing audio"))
        self.mainFrame_toolbar.AddSeparator()
        self.mainFrame_toolbar.AddLabelTool(ID_ZOOMIN, _("Zoom In"),
                                            wx.Bitmap(os.path.join(get_main_dir(), "rsrc/zoom_in.png")), wx.NullBitmap,
                                            wx.ITEM_NORMAL, _("Zoom In"), _("Zoom in on the waveform"))
        self.mainFrame_toolbar.AddLabelTool(ID_ZOOMOUT, _("Zoom Out"),
                                            wx.Bitmap(os.path.join(get_main_dir(), "rsrc/zoom_out.png")), wx.NullBitmap,
                                            wx.ITEM_NORMAL, _("Zoom Out"), _("Zoom out of the waveform"))
        self.mainFrame_toolbar.AddLabelTool(ID_ZOOM1, _("Reset Zoom"),
                                            wx.Bitmap(os.path.join(get_main_dir(), "rsrc/zoom_1.png")), wx.NullBitmap,
                                            wx.ITEM_NORMAL, _("Reset Zoom"), _("Reset the zoomed view of the waveform"))
        # Tool Bar end
        self.panel_2 = wx.Panel(self, wx.ID_ANY)
        self.waveformView = WaveformView(self.panel_2, wx.ID_ANY)
        self.label_2 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Voice name:"))
        global ID_VOICENAME
        ID_VOICENAME = wx.NewId()
        self.voiceName = wx.TextCtrl(self.panel_2, ID_VOICENAME, "")
        self.label_1 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Spoken text:"))
        global ID_VOICETEXT
        ID_VOICETEXT = wx.NewId()
        self.voiceText = wx.TextCtrl(self.panel_2, ID_VOICETEXT, "", style=wx.TE_MULTILINE)
        self.label_4 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Phonetic breakdown:"))
        global ID_LANGUAGECHOICE
        ID_LANGUAGECHOICE = wx.NewId()
        self.languageChoice = wx.Choice(self.panel_2, ID_LANGUAGECHOICE, choices=[])
        global ID_PHONEMESETCHOICE
        ID_PHONEMESETCHOICE = wx.NewId()
        self.phonemesetChoice = wx.Choice(self.panel_2, ID_PHONEMESETCHOICE, choices=[])
        global ID_BREAKDOWN
        ID_BREAKDOWN = wx.NewId()
        self.breakdownBut = wx.Button(self.panel_2, ID_BREAKDOWN, _("Breakdown"))
        global ID_RELOADDICT
        ID_RELOADDICT = wx.NewId()
        self.reloaddictBut = wx.Button(self.panel_2, ID_RELOADDICT, _("Reload Dictionary"))
        self.label_5 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Export:"))
        global ID_EXPORTCHOICE
        ID_EXPORTCHOICE = wx.NewId()
        self.exportChoice = wx.Choice(self.panel_2, ID_EXPORTCHOICE, choices=[])
        global ID_EXPORT
        ID_EXPORT = wx.NewId()
        self.exportBut = wx.Button(self.panel_2, ID_EXPORT, _("Export..."))
        global ID_VOICEIMAGE
        ID_VOICEIMAGE = wx.NewId()
        self.voiceimageBut = wx.Button(self.panel_2, ID_VOICEIMAGE, _("Choose image set..."))
        self.sizer_7_staticbox = wx.StaticBox(self.panel_2, wx.ID_ANY, _("Current Voice"))
        self.label_3 = wx.StaticText(self.panel_2, wx.ID_ANY, _("Fps:"))
        global ID_FPS
        ID_FPS = wx.NewId()
        self.fpsCtrl = wx.TextCtrl(self.panel_2, ID_FPS, "")
        global ID_MOUTHCHOICE
        ID_MOUTHCHOICE = wx.NewId()
        self.mouthChoice = wx.Choice(self.panel_2, ID_MOUTHCHOICE, choices=[])
        self.mouthView = MouthView(self.panel_2, wx.ID_ANY)
        global ID_VOICELIST
        ID_VOICELIST = wx.NewId()
        self.voiceList = wx.ListBox(self.panel_2, ID_VOICELIST, choices=[])
        global ID_NEWVOICE
        ID_NEWVOICE = wx.NewId()
        self.newVoiceBut = wx.Button(self.panel_2, ID_NEWVOICE, _("New"))
        global ID_DELVOICE
        ID_DELVOICE = wx.NewId()
        self.delVoiceBut = wx.Button(self.panel_2, ID_DELVOICE, _("Delete"))
        self.sizer_5_staticbox = wx.StaticBox(self.panel_2, wx.ID_ANY, _("Voice List"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        # Other initialization
        self.SetMinSize(wx.Size(500, 450))
        self.fpsCtrl.SetValidator(DigitOnlyValidator())
        self.waveformView.mouthView = self.mouthView
        self.doc = None
        self.OnClose()
        mouthList = list(self.mouthView.mouths.keys())
        mouthList.sort()
        print(mouthList)
        for mouth in mouthList:
            self.mouthChoice.Append(mouth)
        self.mouthChoice.SetSelection(0)
        self.mouthView.currentMouth = self.mouthChoice.GetStringSelection()

        # setup language initialisation here
        self.langman = LanguageManager()
        self.langman.InitLanguages()
        languageList = list(self.langman.language_table.keys())
        languageList.sort()
        c = 0
        select = 0
        for language in languageList:
            self.languageChoice.Append(language)
            if language == "English":
                select = c
            c += 1
        self.languageChoice.SetSelection(select)

        # setup phonemeset initialisation here
        self.phonemeset = PhonemeSet()
        for name in self.phonemeset.alternatives:
            self.phonemesetChoice.Append(name)
        self.phonemesetChoice.SetSelection(0)

        # setup export initialisation here
        exporterList = ["MOHO", "ALELO", "Images"]
        c = 0
        select = 0
        for exporter in exporterList:
            self.exportChoice.Append(exporter)
            if exporter == "MOHO":
                select = c
            c += 1
        self.exportChoice.SetSelection(select)

        self.ignoreTextChanges = False
        self.config = wx.Config("Papagayo-NG", "Lost Marble")
        self.curFrame = 0
        self.timer = None

        # Connect event handlers
        global ID_PLAY_TICK
        ID_PLAY_TICK = wx.NewId()
        # window events
        wx.EVT_CLOSE(self, self.CloseOK)
        self.Bind(wx.EVT_TIMER, self.OnPlayTick)
        # wx.EVT_TIMER(self, ID_PLAY_TICK, self.OnPlayTick)
        # menus
        wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, wx.ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, wx.ID_SAVEAS, self.OnSaveAs)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnQuit)
        wx.EVT_MENU(self, wx.ID_HELP, self.OnHelp)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        # tools
        wx.EVT_TOOL(self, ID_PLAY, self.OnPlay)
        wx.EVT_TOOL(self, ID_STOP, self.OnStop)
        wx.EVT_TOOL(self, ID_ZOOMIN, self.waveformView.OnZoomIn)
        wx.EVT_TOOL(self, ID_ZOOMOUT, self.waveformView.OnZoomOut)
        wx.EVT_TOOL(self, ID_ZOOM1, self.waveformView.OnZoom1)
        # voice settings
        wx.EVT_CHOICE(self, ID_MOUTHCHOICE, self.OnMouthChoice)
        wx.EVT_CHOICE(self, ID_EXPORTCHOICE, self.OnExportChoice)
        wx.EVT_TEXT(self, ID_VOICENAME, self.OnVoiceName)
        wx.EVT_TEXT(self, ID_VOICETEXT, self.OnVoiceText)
        wx.EVT_BUTTON(self, ID_BREAKDOWN, self.OnVoiceBreakdown)
        wx.EVT_BUTTON(self, ID_RELOADDICT, self.OnReloadDictionary)
        wx.EVT_BUTTON(self, ID_EXPORT, self.OnVoiceExport)
        wx.EVT_BUTTON(self, ID_VOICEIMAGE, self.OnVoiceimagechoose)
        wx.EVT_TEXT(self, ID_FPS, self.OnFps)
        wx.EVT_LISTBOX(self, ID_VOICELIST, self.OnSelVoice)
        wx.EVT_BUTTON(self, ID_NEWVOICE, self.OnNewVoice)
        wx.EVT_BUTTON(self, ID_DELVOICE, self.OnDelVoice)

    def __del__(self):
        try:
            self.config.Flush()
        except AttributeError:
            print("Error")

    def __set_properties(self):
        # begin wxGlade: LipsyncFrame.__set_properties
        self.SetTitle(_("Papagayo-NG"))
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(os.path.join(get_main_dir(), "rsrc/window_icon.bmp")))
        self.SetIcon(_icon)
        self.SetSize((850, 630))
        self.mainFrame_statusbar.SetStatusWidths([-1, 96])

        # statusbar fields
        mainFrame_statusbar_fields = [_("Papagayo-NG"), _("Stopped")]
        for i in range(len(mainFrame_statusbar_fields)):
            self.mainFrame_statusbar.SetStatusText(mainFrame_statusbar_fields[i], i)
        self.mainFrame_toolbar.SetToolBitmapSize((16, 16))
        self.mainFrame_toolbar.Realize()
        self.voiceText.SetMinSize((128, 128))
        self.voiceList.SetMinSize((195, 133))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: LipsyncFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_5_staticbox.Lower()
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_7_staticbox.Lower()
        sizer_7 = wx.StaticBoxSizer(self.sizer_7_staticbox, wx.VERTICAL)
        sizer_9_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.waveformView, 1, wx.EXPAND, 0)
        sizer_8.Add(self.label_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 0)
        sizer_8.Add((8, 8), 0, wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 0)
        sizer_8.Add(self.voiceName, 0, wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 0)
        sizer_7.Add(sizer_8, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 4)
        sizer_7.Add(self.label_1, 0, wx.FIXED_MINSIZE | wx.LEFT | wx.TOP, 4)
        sizer_7.Add(self.voiceText, 1, wx.EXPAND | wx.FIXED_MINSIZE | wx.LEFT | wx.RIGHT | wx.TOP, 4)
        sizer_7.Add(self.label_4, 0, wx.FIXED_MINSIZE | wx.LEFT | wx.TOP, 4)
        sizer_9.Add(self.languageChoice, 0, 0, 0)
        sizer_9.Add(self.phonemesetChoice, 0, 0, 0)
        sizer_9.Add((20, 20), 0, 0, 0)
        sizer_9.Add(self.breakdownBut, 0, wx.FIXED_MINSIZE, 0)
        sizer_9.Add(self.reloaddictBut, 0, 0, 0)
        sizer_7.Add(sizer_9, 0, wx.ALL | wx.EXPAND, 4)
        sizer_7.Add(self.label_5, 0, wx.FIXED_MINSIZE | wx.LEFT | wx.TOP, 4)
        sizer_9_copy.Add(self.exportChoice, 0, 0, 0)
        sizer_9_copy.Add((20, 20), 0, 0, 0)
        sizer_9_copy.Add(self.exportBut, 0, 0, 0)
        sizer_9_copy.Add(self.voiceimageBut, 0, 0, 0)
        sizer_7.Add(sizer_9_copy, 0, wx.ALL | wx.EXPAND, 4)
        sizer_3.Add(sizer_7, 1, wx.ALL | wx.EXPAND, 4)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_10.Add(self.label_3, 0, wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 0)
        sizer_10.Add((8, 8), 0, wx.ALIGN_CENTER_VERTICAL | wx.FIXED_MINSIZE, 0)
        sizer_10.Add(self.fpsCtrl, 0, wx.FIXED_MINSIZE, 0)
        sizer_4.Add(sizer_10, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 4)
        sizer_4.Add(self.mouthChoice, 0, wx.BOTTOM | wx.EXPAND | wx.FIXED_MINSIZE | wx.LEFT | wx.RIGHT, 4)
        sizer_4.Add(self.mouthView, 0, wx.EXPAND, 0)
        sizer_5.Add(self.voiceList, 1, wx.ALL | wx.EXPAND | wx.FIXED_MINSIZE, 4)
        sizer_6.Add(self.newVoiceBut, 0, wx.FIXED_MINSIZE, 0)
        sizer_6.Add((20, 20), 0, wx.FIXED_MINSIZE, 0)
        sizer_6.Add(self.delVoiceBut, 0, wx.FIXED_MINSIZE, 0)
        sizer_5.Add(sizer_6, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 4)
        sizer_4.Add(sizer_5, 1, wx.ALL | wx.EXPAND, 4)
        sizer_2.Add(sizer_4, 0, wx.EXPAND | wx.LEFT, 4)
        self.panel_2.SetSizer(sizer_2)
        sizer_1.Add(self.panel_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade

    def CloseOK(self, event):
        if not event.CanVeto():
            self.OnClose()
            event.Skip()
            return
        if not self.CloseDocOK():
            event.Veto()
            return
        self.OnClose()
        event.Skip()

    def CloseDocOK(self):
        if self.doc is not None:
            if not self.doc.dirty:
                return True
            dlg = wx.MessageDialog(self, _('Save changes to this project?'), appTitle,
                                   wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_YES:
                self.OnSave()
                if not self.doc.dirty:
                    self.config.Write("LastFPS", str(self.doc.fps))
                    return True
                else:
                    return False
            elif result == wx.ID_NO:
                self.config.Write("LastFPS", str(self.doc.fps))
                return True
            elif result == wx.ID_CANCEL:
                return False
        else:
            return True

    def OnOpen(self, event=None):
        if not self.CloseDocOK():
            return
        dlg = wx.FileDialog(
            self, message=_("Open Audio or %s File") % appTitle, defaultDir=self.config.Read("WorkingDir", get_main_dir()),
            defaultFile="", wildcard=openWildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.OnStop()
            self.OnClose()
            self.config.Write("WorkingDir", dlg.GetDirectory())
            paths = dlg.GetPaths()
            self.Open(paths[0])
        dlg.Destroy()

    def Open(self, path):
        self.doc = LipsyncDoc(self.langman, self)
        if path.endswith(lipsyncExtension):
            # open a lipsync project
            self.doc.Open(path)
            while self.doc.sound is None:
                # if no sound file found, then ask user to specify one
                dlg = wx.MessageDialog(self, _('Please load correct audio file'), appTitle,
                                       wx.OK | wx.ICON_WARNING)
                result = dlg.ShowModal()
                dlg.Destroy()
                dlg = wx.FileDialog(
                    self, message=_("Open Audio"), defaultDir=self.config.Read("WorkingDir", get_main_dir()),
                    defaultFile="", wildcard=openAudioWildcard,
                    style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST)
                if dlg.ShowModal() == wx.ID_OK:
                    self.config.Write("WorkingDir", dlg.GetDirectory())
                    paths = dlg.GetPaths()
                    self.doc.OpenAudio(paths[0])
                dlg.Destroy()
        else:
            # open an audio file
            self.doc.fps = int(self.config.Read("LastFPS", "24"))
            self.doc.OpenAudio(path)
            if self.doc.sound is None:
                self.doc = None
            else:
                self.doc.voices.append(LipsyncVoice("Voice 1"))
                self.doc.currentVoice = self.doc.voices[0]
                # check for a .trans file with the same name as the doc
                try:
                    txtFile = file(path[0].rsplit('.', 1)[0] + ".trans", 'r')  # TODO: Check if path is correct
                    for line in txtFile:
                        self.voiceText.AppendText(line)
                except:  # TODO: except is too broad
                    pass

        if self.doc is not None:
            self.SetTitle("%s [%s] - %s" % (self.doc.name, path, appTitle))
            self.waveformView.SetDocument(self.doc)
            self.mouthView.SetDocument(self.doc)
            # menus
            self.mainFrame_menubar.Enable(wx.ID_SAVE, True)
            self.mainFrame_menubar.Enable(wx.ID_SAVEAS, True)
            # toolbar buttons
            self.mainFrame_toolbar.EnableTool(wx.ID_SAVE, True)
            if self.doc.sound is not None:
                self.mainFrame_toolbar.EnableTool(ID_PLAY, True)
                self.mainFrame_toolbar.EnableTool(ID_ZOOMIN, True)
                self.mainFrame_toolbar.EnableTool(ID_ZOOMOUT, True)
                self.mainFrame_toolbar.EnableTool(ID_ZOOM1, True)
            # voice list
            self.voiceList.Enable(True)
            self.newVoiceBut.Enable(True)
            self.delVoiceBut.Enable(True)
            for voice in self.doc.voices:
                self.voiceList.Insert(voice.name, self.voiceList.GetCount())
            self.voiceList.SetSelection(0)
            # voice controls
            self.fpsCtrl.Enable(True)
            self.fpsCtrl.SetValue(str(self.doc.fps))
            self.voiceName.Enable(True)
            self.voiceName.SetValue(self.doc.currentVoice.name)
            self.voiceText.Enable(True)
            self.voiceText.SetValue(self.doc.currentVoice.text)
            self.languageChoice.Enable(True)
            self.phonemesetChoice.Enable(True)
            self.breakdownBut.Enable(True)
            self.reloaddictBut.Enable(True)
            self.exportChoice.Enable(True)
            self.exportBut.Enable(True)
            self.voiceimageBut.Enable(False)

    def OnSave(self, event=None):
        if self.doc is None:
            return
        if self.doc.path is None:
            self.OnSaveAs()
            return
        self.doc.Save(self.doc.path)

    def OnSaveAs(self, event=None):
        if self.doc is None:
            return
        dlg = wx.FileDialog(
            self, message=_("Save %s File") % appTitle, defaultDir=self.config.Read("WorkingDir", get_main_dir()),
            defaultFile="%s" % self.doc.soundPath.rsplit('.', 1)[0] + ".pgo", wildcard=saveWildcard,
            style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.config.Write("WorkingDir", dlg.GetDirectory())
            self.doc.Save(dlg.GetPaths()[0])
            self.SetTitle("%s [%s] - %s" % (self.doc.name, dlg.GetPaths()[0], appTitle))
        dlg.Destroy()

    def OnClose(self):
        if self.doc is not None:
            self.config.Write("LastFPS", str(self.doc.fps))
            del self.doc
        self.doc = None
        self.waveformView.SetDocument(self.doc)
        # menus
        self.mainFrame_menubar.Enable(wx.ID_SAVE, False)
        self.mainFrame_menubar.Enable(wx.ID_SAVEAS, False)
        # toolbar buttons
        self.mainFrame_toolbar.EnableTool(wx.ID_SAVE, False)
        self.mainFrame_toolbar.EnableTool(ID_PLAY, False)
        self.mainFrame_toolbar.EnableTool(ID_STOP, False)
        self.mainFrame_toolbar.EnableTool(ID_ZOOMIN, False)
        self.mainFrame_toolbar.EnableTool(ID_ZOOMOUT, False)
        self.mainFrame_toolbar.EnableTool(ID_ZOOM1, False)
        # voice controls
        self.voiceName.Clear()
        self.voiceName.Enable(False)
        self.voiceText.Clear()
        self.voiceText.Enable(False)
        self.languageChoice.Enable(False)
        self.phonemesetChoice.Enable(False)
        self.breakdownBut.Enable(False)
        self.reloaddictBut.Enable(False)
        self.exportChoice.Enable(False)
        self.exportBut.Enable(False)
        self.voiceimageBut.Enable(False)
        # voice list
        self.fpsCtrl.Clear()
        self.fpsCtrl.Enable(False)
        self.voiceList.Clear()
        self.voiceList.Enable(False)
        self.newVoiceBut.Enable(False)
        self.delVoiceBut.Enable(False)

    def OnQuit(self, event=None):
        self.OnClose()
        self.Close(True)

    def OnHelp(self, event=None):
        webbrowser.open(r"https://github.com/morevnaproject/papagayo-ng")
        #webbrowser.open("file://%s" % os.path.join(get_main_dir(), "help/index.html"))  # TODO: Fix path

    def OnAbout(self, event=None):
        dlg = AboutBox(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnPlay(self, event=None):
        if (self.doc is not None) and (self.doc.sound is not None):
            self.curFrame = -1
            self.mainFrame_toolbar.EnableTool(ID_PLAY, False)
            self.mainFrame_toolbar.EnableTool(ID_STOP, True)
            self.doc.sound.SetCurTime(0)
            self.doc.sound.Play(False)
            self.timer = wx.Timer(self, ID_PLAY_TICK)
            self.timer.Start(250.0 / self.doc.fps)

    def OnStop(self, event=None):
        if (self.doc is not None) and (self.doc.sound is not None):
            self.doc.sound.Stop()
            self.doc.sound.SetCurTime(0)
            self.mouthView.SetFrame(0)
            self.waveformView.SetFrame(0)
            self.mainFrame_toolbar.EnableTool(ID_PLAY, True)
            self.mainFrame_toolbar.EnableTool(ID_STOP, False)
            self.mainFrame_statusbar.SetStatusText("Stopped", 1)

    def OnPlayTick(self, event):
        if (self.doc is not None) and (self.doc.sound is not None):
            if self.doc.sound.IsPlaying():
                curFrame = int(math.floor(self.doc.sound.CurrentTime() * self.doc.fps))
                if curFrame != self.curFrame:
                    self.curFrame = curFrame
                    self.mouthView.SetFrame(self.curFrame)
                    self.waveformView.SetFrame(self.curFrame)
                    self.mainFrame_statusbar.SetStatusText("Frame: %d" % (curFrame + 1), 1)
            else:
                self.OnStop()
                self.timer.Stop()
                del self.timer

    def OnMouthChoice(self, event):
        self.mouthView.currentMouth = self.mouthChoice.GetStringSelection()
        self.mouthView.DrawMe()
    
    def OnExportChoice(self, event):
        if self.exportChoice.GetStringSelection() == "Images":
            self.voiceimageBut.Enable(True)
        else:
            self.voiceimageBut.Enable(False)
            

    def OnVoiceName(self, event):
        if (self.doc is not None) and (self.doc.currentVoice is not None):
            self.doc.dirty = True
            self.doc.currentVoice.name = self.voiceName.GetValue()
            self.voiceList.SetString(self.voiceList.GetSelection(), self.doc.currentVoice.name)

    def OnVoiceText(self, event):
        if self.ignoreTextChanges:
            return
        if (self.doc is not None) and (self.doc.currentVoice is not None):
            self.doc.dirty = True
            self.doc.currentVoice.text = self.voiceText.GetValue()

    def OnVoiceBreakdown(self, event=None):
        if (self.doc is not None) and (self.doc.currentVoice is not None):
            language = self.languageChoice.GetStringSelection()
            phonemeset_name = self.phonemesetChoice.GetStringSelection()
            self.phonemeset.Load(phonemeset_name)
            self.doc.dirty = True
            self.doc.currentVoice.RunBreakdown(self.doc.soundDuration, self, language, self.langman, self.phonemeset)
            self.waveformView.UpdateDrawing()
            self.ignoreTextChanges = True
            self.voiceText.SetValue(self.doc.currentVoice.text)
            self.ignoreTextChanges = False

    def OnVoiceExport(self, event):
        language = self.languageChoice.GetStringSelection()
        if (self.doc is not None) and (self.doc.currentVoice is not None):
            exporter = self.exportChoice.GetStringSelection()
            if exporter == "MOHO":
                dlg = wx.FileDialog(
                    self, message=_("Export Lipsync Data (MOHO)"),
                    defaultDir=self.config.Read("WorkingDir", get_main_dir()),
                    defaultFile="%s" % self.doc.soundPath.rsplit('.', 1)[0] + ".dat",
                    wildcard="Moho switch files (*.dat)|*.dat",
                    style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
                if dlg.ShowModal() == wx.ID_OK:
                    self.config.Write("WorkingDir", dlg.GetDirectory())
                    self.doc.currentVoice.Export(dlg.GetPaths()[0])
                dlg.Destroy()
            elif exporter == "ALELO":
                fps = int(self.fpsCtrl.GetValue())
                if fps != 100:
                    dlg = wx.MessageDialog(self, _('FPS is NOT 100 continue? (You will have issues downstream.)'),
                                           appTitle,
                                           wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_WARNING)
                    result = dlg.ShowModal()
                    dlg.Destroy()
                else:
                    result = wx.ID_YES
                if result == wx.ID_YES:
                    dlg = wx.FileDialog(
                        self, message=_("Export Lipsync Data (ALELO)"),
                        defaultDir=self.config.Read("WorkingDir", get_main_dir()),
                        defaultFile="%s" % self.doc.soundPath.rsplit('.', 1)[0] + ".txt",
                        wildcard="Alelo timing files (*.txt)|*.txt",
                        style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
                    if dlg.ShowModal() == wx.ID_OK:
                        self.config.Write("WorkingDir", dlg.GetDirectory())
                        self.doc.currentVoice.ExportAlelo(dlg.GetPaths()[0], language, self.langman)
                    dlg.Destroy()
            elif exporter == "Images":
                dlg = wx.FileDialog(
                    self, message=_("Export Image Strip"), defaultDir=self.config.Read("WorkingDir", get_main_dir()),
                    defaultFile="%s" % self.doc.soundPath.rsplit('.', 1)[0],
                    style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
                if dlg.ShowModal() == wx.ID_OK:
                    self.config.Write("WorkingDir", dlg.GetDirectory())
                    self.doc.currentVoice.ExportImages(dlg.GetPaths()[0], self.mouthChoice.GetStringSelection())
                dlg.Destroy()

    def OnVoiceimagechoose(self, event):
        language = self.languageChoice.GetStringSelection()
        if (self.doc is not None) and (self.doc.currentVoice is not None):
            voiceimagepath = wx.DirDialog(
                self, message=_("Choose Path for Images"), defaultPath=self.config.Read("MouthDir", os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "rsrc/mouths/")),
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.DD_DIR_MUST_EXIST)
            if voiceimagepath.ShowModal() == wx.ID_OK:
                self.config.Write("MouthDir", voiceimagepath.GetPath())
                print(voiceimagepath.GetPath())
                full_pattern = re.compile('[^a-zA-Z0-9.\\\/]|_')
                supportedimagetypes = re.sub(full_pattern, '', wx.Image.GetImageExtWildcard()).split(".")
                for directory, dirnames, filenames in os.walk(voiceimagepath.GetPath()):
                    self.mouthView.ProcessMouthDir(directory, filenames, supportedimagetypes)
                mouthList = list(self.mouthView.mouths.keys())
                mouthList.sort()
                print(mouthList)
                self.mouthChoice.Clear()
                for mouth in mouthList:
                    self.mouthChoice.Append(mouth)
                self.mouthChoice.SetSelection(0)
                self.mouthView.currentMouth = self.mouthChoice.GetStringSelection()
            voiceimagepath.Destroy()

    def OnFps(self, event):
        if self.doc is None:
            return
        try:
            newFps = int(self.fpsCtrl.GetValue())
        except:  # TODO: except is too broad
            newFps = self.doc.fps
        if newFps == self.doc.fps:
            return
        self.doc.dirty = True
        self.doc.fps = newFps
        if self.doc.fps < 1:
            self.doc.fps = 1
        if self.doc.fps > 120:
            self.doc.fps = 120
        # refresh the document properties
        self.doc.OpenAudio(self.doc.soundPath)
        self.waveformView.SetDocument(None)
        self.waveformView.SetDocument(self.doc)
        self.mouthView.DrawMe()

    def OnSelVoice(self, event):
        if self.doc is None:
            return
        self.ignoreTextChanges = True
        self.doc.currentVoice = self.doc.voices[self.voiceList.GetSelection()]
        self.voiceName.SetValue(self.doc.currentVoice.name)
        self.voiceText.SetValue(self.doc.currentVoice.text)
        self.ignoreTextChanges = False
        self.waveformView.UpdateDrawing()
        self.mouthView.DrawMe()

    def OnNewVoice(self, event):
        if self.doc is None:
            return
        self.doc.dirty = True
        self.doc.voices.append(LipsyncVoice("Voice %d" % (len(self.doc.voices) + 1)))
        self.doc.currentVoice = self.doc.voices[-1]
        self.voiceList.Insert(self.doc.currentVoice.name, self.voiceList.GetCount())
        self.voiceList.SetSelection(self.voiceList.GetCount() - 1)
        self.ignoreTextChanges = True
        self.voiceName.SetValue(self.doc.currentVoice.name)
        self.voiceText.SetValue(self.doc.currentVoice.text)
        self.ignoreTextChanges = False
        self.waveformView.UpdateDrawing()
        self.mouthView.DrawMe()

    def OnDelVoice(self, event):
        if (self.doc is None) or (len(self.doc.voices) == 1):
            return
        self.doc.dirty = True
        newIndex = self.doc.voices.index(self.doc.currentVoice)
        if newIndex > 0:
            newIndex -= 1
        else:
            newIndex = 0
        self.doc.voices.remove(self.doc.currentVoice)
        self.doc.currentVoice = self.doc.voices[newIndex]
        self.voiceList.Clear()
        for voice in self.doc.voices:
            self.voiceList.Insert(voice.name, self.voiceList.GetCount())
        self.voiceList.SetSelection(newIndex)
        self.voiceName.SetValue(self.doc.currentVoice.name)
        self.voiceText.SetValue(self.doc.currentVoice.text)
        self.waveformView.UpdateDrawing()
        self.mouthView.DrawMe()

    def OnReloadDictionary(self, event):
        print("reload the dictionary")
        lang_config = self.doc.language_manager.language_table[self.languageChoice.GetStringSelection()]
        self.doc.language_manager.LoadLanguage(lang_config, force=True)

# end of class LipsyncFrame
