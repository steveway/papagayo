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

# import os
import string
import math
# import wx
from PySide import QtCore, QtGui, QtUiTools
import webbrowser
import re
# from utilities import *
# begin wxGlade: dependencies
# from MouthView import MouthView
# from WaveformView import WaveformView
from WaveformViewQT import WaveformView
from MouthViewQT import MouthView
# end wxGlade

# from AboutBox import AboutBox
from LipsyncDoc import *

app_title = "Papagayo-NG"
lipsync_extension = "*.pgo"
audio_extensions = "*.wav *.mp3 *.aiff *.aif *.au *.snd *.mov *.m4a"
open_wildcard = "%s and sound files (%s %s)" % (app_title, audio_extensions, lipsync_extension)
audioExtensions = "*.wav;*.mp3;*.aiff;*.aif;*.au;*.snd;*.mov;*.m4a"
# openWildcard = "%s and sound files|*%s;%s" % (appTitle, lipsyncExtension, audioExtensions)
# openAudioWildcard = "Sound files|%s" % (audioExtensions)
# saveWildcard = "%s files (*%s)|*%s" % (appTitle, lipsyncExtension, lipsyncExtension)


class DigitOnlyValidator(wx.PyValidator):
    def __init__(self, flag=None, pyVar=None):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def clone(self):
        return DigitOnlyValidator()

    def validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        for x in val:
            if x not in string.digits:
                return False

        return True

    def on_char(self, event):
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


class LipsyncFrame:
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.main_window = self.load_ui_widget("./rsrc/papagayo-ng2.ui")
        self.main_window.setWindowTitle("%s" % app_title)
        self.loader = None
        self.ui_file = None
        self.ui = None
        self.doc = None
        self.config = QtCore.QSettings(app_title, "Lost Marble")

        # TODO: need a good description for this stuff
        self.langman = LanguageManager()
        self.langman.InitLanguages()
        language_list = list(self.langman.language_table.keys())
        language_list.sort()

        c = 0
        select = 0
        for language in language_list:
            self.main_window.language_choice.addItem(language)
            if language == "English":
                select = c
            c += 1
        self.main_window.language_choice.setCurrentIndex(select)

        # This adds our statuses to the statusbar
        self.mainframe_statusbar_fields = [app_title, "Stopped"]
        self.play_status = QtGui.QLabel()
        self.play_status.setText(self.mainframe_statusbar_fields[1])
        # An empty Label to add a separator
        self.sep_status = QtGui.QLabel()
        self.sep_status.setText(u"")
        self.main_window.statusbar.addPermanentWidget(self.sep_status)
        self.main_window.statusbar.addPermanentWidget(self.play_status)
        self.main_window.statusbar.showMessage(self.mainframe_statusbar_fields[0])
        # Connect Events
        self.main_window.action_play.triggered.connect(self.test_button_event)
        self.main_window.action_exit.triggered.connect(self.quit_application)
        self.main_window.action_open.triggered.connect(self.on_open)
        self.main_window.action_save.triggered.connect(self.on_save)

        # self.main_window.vertical_layout_left.addWidget(self.waveform_view)

    def load_ui_widget(self, ui_filename, parent=None):
        self.loader = QtUiTools.QUiLoader()
        self.ui_file = QtCore.QFile(ui_filename)
        self.ui_file.open(QtCore.QFile.ReadOnly)
        self.loader.registerCustomWidget(WaveformView)
        self.loader.registerCustomWidget(MouthView)
        self.ui = self.loader.load(self.ui_file, parent)
        self.ui_file.close()
        return self.ui

    def test_button_event(self):
        self.play_status.setText("Running")

    def close_doc_ok(self):
        if self.doc is not None:
            if not self.doc.dirty:
                return True
            dlg = QtGui.QMessageBox()
            dlg.setText("Save changes to this project?")
            dlg.setStandardButtons(QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            dlg.setDefaultButton(QtGui.QMessageBox.Yes)
            dlg.setIcon(QtGui.QMessageBox.Question)
            result = dlg.exec_()
            if result == QtGui.QMessageBox.Yes:
                self.on_save()
                if not self.doc.dirty:
                    self.config.setValue("LastFPS", str(self.doc.fps))
                    return True
                else:
                    return False
            elif result == QtGui.QMessageBox.No:
                self.config.setValue("LastFPS", str(self.doc.fps))
                return True
            elif result == QtGui.QMessageBox.Cancel:
                return False
        else:
            return True
        #     dlg = wx.MessageDialog(self, _('Save changes to this project?'), appTitle,
        #                            wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_QUESTION)
        #     result = dlg.ShowModal()
        #     dlg.Destroy()
        #     if result == wx.ID_YES:
        #         self.OnSave()
        #         if not self.doc.dirty:
        #             self.config.Write("LastFPS", str(self.doc.fps))
        #             return True
        #         else:
        #             return False
        #     elif result == wx.ID_NO:
        #         self.config.Write("LastFPS", str(self.doc.fps))
        #         return True
        #     elif result == wx.ID_CANCEL:
        #         return False
        # else:
        #     return True

    def on_open(self):
        if not self.close_doc_ok():
            return
        file_path, _ = QtGui.QFileDialog.getOpenFileName(self.main_window,
                                                         "Open Audio or %s File" % app_title,
                                                         self.config.value("WorkingDir", get_main_dir()),
                                                         open_wildcard)
        if file_path:
            print(file_path)
            self.config.setValue("WorkingDir", os.path.dirname(file_path))
            print(os.path.dirname(file_path))
            self.open(file_path)
        # dlg = wx.FileDialog(
        #     self, message=_("Open Audio or %s File") % appTitle, defaultDir=self.config.Read("WorkingDir", get_main_dir()),
        #     defaultFile="", wildcard=openWildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST)
        # if dlg.ShowModal() == wx.ID_OK:
        #     self.OnStop()
        #     self.OnClose()
        #     self.config.Write("WorkingDir", dlg.GetDirectory())
        #     paths = dlg.GetPaths()
        #     self.Open(paths[0])
        # dlg.Destroy()

    def open(self, path):
        self.doc = LipsyncDoc(self.langman, self)
        if path.endswith(lipsync_extension):
            # open a lipsync project
            self.doc.open(path)
            while self.doc.sound is None:
                # if no sound file found, then ask user to specify one
                dlg = QtGui.QMessageBox(self.main_window)
                dlg.setText('Please load correct audio file')
                dlg.setWindowTitle(app_title)
                dlg.setIcon(QtGui.QMessageBox.Warning)
                dlg.exec_()  # This should open it as a modal blocking window
                dlg.destroy()  # Untested, might not need it
                file_path, _ = QtGui.QFileDialog(self.main_window,
                                        "Open Audio",
                                        self.config.value("WorkingDir", get_main_dir()),
                                        open_wildcard)
                if file_path:
                    self.config.setValue("WorkingDir", os.path.dirname(file_path))
                    self.doc.open_audio(file_path)
        else:
            # open an audio file
            self.doc.fps = int(self.config.value("LastFPS", 24))
            self.doc.open_audio(path)
            if self.doc.sound is None:
                self.doc = None
            else:
                self.doc.voices.append(LipsyncVoice("Voice 1"))
                self.doc.current_voice = self.doc.voices[0]
                # check for a .trans file with the same name as the doc
                try:
                    txt_file = open(path[0].rsplit('.', 1)[0] + ".trans", 'r')  # TODO: Check if path is correct
                    for line in txt_file:
                        self.main_window.voice_list.appendRow(QtGui.QStandardItem(line))
                except:
                    pass
        if self.doc is not None:
            self.main_window.setWindowTitle("%s [%s] - %s" % (self.doc.name, path, app_title))
            self.main_window.waveform_view.SetDocument(self.doc)
            self.main_window.mouth_view.SetDocument(self.doc)
            # Reenable all disabled widgets TODO: Can likely be reduced
            self.main_window.vertical_layout_right.setEnabled(True)
            self.main_window.vertical_layout_left.setEnabled(True)
            self.main_window.volume_slider.setEnabled(True)
            self.main_window.action_save.setEnabled(True)
            self.main_window.action_save_as.setEnabled(True)
            self.main_window.menu_edit.setEnabled(True)
            if self.doc.sound is not None:
                self.main_window.action_play.setEnabled(True)
                self.main_window.action_stop.setEnabled(True)
                self.main_window.action_zoom_in.setEnabled(True)
                self.main_window.action_zoom_out.setEnabled(True)
                self.main_window.action_reset_zoom.setEnabled(True)

            self.main_window.voice_list.clear()
            for voice in self.doc.voices:
                self.main_window.voice_list.addItem(voice.name)
            self.main_window.voice_list.setCurrentRow(0)
            self.main_window.fps_input.setText(str(self.doc.fps))
            self.main_window.voice_name_input.setText(self.doc.current_voice.name)
            self.main_window.text_edit.setText(self.doc.current_voice.text)
            # reload dictionary
            self.on_reload_dictionary()

    def on_save(self):
        # Test Drawing on the WaveformView
        self.main_window.waveform_view.scene().clear()
        self.main_window.waveform_view.scene().addText("Test")
        wvheight = self.main_window.waveform_view.height()-self.main_window.waveform_view.horizontalScrollBar().height()
        print(wvheight)

        for i in range(50):
            self.main_window.waveform_view.scene().addLine(50*i, 0, 50*i, wvheight)
        pass

    def on_reload_dictionary(self, event = None):
        # print("reload the dictionary")
        lang_config = self.doc.language_manager.language_table[self.main_window.language_choice.currentText()]
        self.doc.language_manager.LoadLanguage(lang_config, force=True)

    def quit_application(self):
        sys.exit(self.app.exec_())


class LipsyncFrameold(wx.Frame):
    def __init__(self, *args, **kwds):

        # self.waveformView = WaveformView(self.panel_2, wx.ID_ANY)

        self.fpsCtrl.SetValidator(DigitOnlyValidator())

        self.doc = None
        mouthList = list(self.mouthView.mouths.keys())
        mouthList.sort()
        print(mouthList)

        # setup language initialisation here

        self.langman = LanguageManager()
        self.langman.InitLanguages()
        languageList = list(self.langman.language_table.keys())
        languageList.sort()
        # setup phonemeset initialisation here
        self.phonemeset = PhonemeSet()
        # setup export initialisation here
        exporterList = ["MOHO", "ALELO", "Images"]

        self.ignoreTextChanges = False
        # self.config = wx.Config("Papagayo-NG", "Lost Marble")
        self.curFrame = 0
        self.timer = None

        # # Connect event handlers
        # global ID_PLAY_TICK
        # ID_PLAY_TICK = wx.NewId()
        # # window events
        # wx.EVT_CLOSE(self, self.CloseOK)
        # self.Bind(wx.EVT_TIMER, self.OnPlayTick)
        # # wx.EVT_TIMER(self, ID_PLAY_TICK, self.OnPlayTick)
        # # menus
        # wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)
        # wx.EVT_MENU(self, wx.ID_SAVE, self.OnSave)
        # wx.EVT_MENU(self, wx.ID_SAVEAS, self.OnSaveAs)
        # wx.EVT_MENU(self, wx.ID_EXIT, self.OnQuit)
        # wx.EVT_MENU(self, wx.ID_HELP, self.OnHelp)
        # wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        # # tools
        # wx.EVT_TOOL(self, ID_PLAY, self.OnPlay)
        # wx.EVT_TOOL(self, ID_STOP, self.OnStop)
        # wx.EVT_TOOL(self, ID_ZOOMIN, self.waveformView.OnZoomIn)
        # wx.EVT_TOOL(self, ID_ZOOMOUT, self.waveformView.OnZoomOut)
        # wx.EVT_TOOL(self, ID_ZOOM1, self.waveformView.OnZoom1)
        # # voice settings
        # wx.EVT_CHOICE(self, ID_MOUTHCHOICE, self.OnMouthChoice)
        # wx.EVT_CHOICE(self, ID_EXPORTCHOICE, self.OnExportChoice)
        # wx.EVT_TEXT(self, ID_VOICENAME, self.OnVoiceName)
        # wx.EVT_TEXT(self, ID_VOICETEXT, self.OnVoiceText)
        # wx.EVT_BUTTON(self, ID_BREAKDOWN, self.OnVoiceBreakdown)
        # wx.EVT_BUTTON(self, ID_RELOADDICT, self.OnReloadDictionary)
        # wx.EVT_BUTTON(self, ID_EXPORT, self.OnVoiceExport)
        # wx.EVT_BUTTON(self, ID_VOICEIMAGE, self.OnVoiceimagechoose)
        # wx.EVT_TEXT(self, ID_FPS, self.OnFps)
        # wx.EVT_LISTBOX(self, ID_VOICELIST, self.OnSelVoice)
        # wx.EVT_BUTTON(self, ID_NEWVOICE, self.OnNewVoice)
        # wx.EVT_BUTTON(self, ID_DELVOICE, self.OnDelVoice)
        # wx.EVT_SLIDER(self, ID_VOLSLIDER, self.ChangeVolume)

    def __del__(self):
        try:
            self.config.Flush()
        except AttributeError:
            print("Error")

    def __set_properties(self):
        # begin wxGlade: LipsyncFrame.__set_properties
        # self.SetTitle(_("Papagayo-NG"))
        # _icon = wx.EmptyIcon()
        # _icon.CopyFromBitmap(wx.Bitmap(os.path.join(get_main_dir(), "rsrc/window_icon.bmp")))
        # self.SetIcon(_icon)
        pass
        # end wxGlade

    def __do_layout(self):
        pass

    def ChangeVolume(self, event):
        # if self.doc and self.doc.sound:
        #     self.doc.sound.volume = int(self.volume_slider.GetValue())
        #     #print(self.doc.sound.volume)
        pass

    def CloseOK(self, event):
        # if not event.CanVeto():
        #     self.OnClose()
        #     event.Skip()
        #     return
        # if not self.CloseDocOK():
        #     event.Veto()
        #     return
        # self.OnClose()
        # event.Skip()
        pass

    def CloseDocOK(self):
        # if self.doc is not None:
        #     if not self.doc.dirty:
        #         return True
        #     dlg = wx.MessageDialog(self, _('Save changes to this project?'), appTitle,
        #                            wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_QUESTION)
        #     result = dlg.ShowModal()
        #     dlg.Destroy()
        #     if result == wx.ID_YES:
        #         self.OnSave()
        #         if not self.doc.dirty:
        #             self.config.Write("LastFPS", str(self.doc.fps))
        #             return True
        #         else:
        #             return False
        #     elif result == wx.ID_NO:
        #         self.config.Write("LastFPS", str(self.doc.fps))
        #         return True
        #     elif result == wx.ID_CANCEL:
        #         return False
        # else:
        #     return True
        pass

    def OnOpen(self, event=None):
        # if not self.CloseDocOK():
        #     return
        # dlg = wx.FileDialog(
        #     self, message=_("Open Audio or %s File") % appTitle, defaultDir=self.config.Read("WorkingDir", get_main_dir()),
        #     defaultFile="", wildcard=openWildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST)
        # if dlg.ShowModal() == wx.ID_OK:
        #     self.OnStop()
        #     self.OnClose()
        #     self.config.Write("WorkingDir", dlg.GetDirectory())
        #     paths = dlg.GetPaths()
        #     self.Open(paths[0])
        # dlg.Destroy()
        pass

    def Open(self, path):
        # self.doc = LipsyncDoc(self.langman, self)
        # if path.endswith(lipsyncExtension):
        #     # open a lipsync project
        #     self.doc.Open(path)
        #     while self.doc.sound is None:
        #         # if no sound file found, then ask user to specify one
        #         dlg = wx.MessageDialog(self, _('Please load correct audio file'), appTitle,
        #                                wx.OK | wx.ICON_WARNING)
        #         result = dlg.ShowModal()
        #         dlg.Destroy()
        #         dlg = wx.FileDialog(
        #             self, message=_("Open Audio"), defaultDir=self.config.Read("WorkingDir", get_main_dir()),
        #             defaultFile="", wildcard=openAudioWildcard,
        #             style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST)
        #         if dlg.ShowModal() == wx.ID_OK:
        #             self.config.Write("WorkingDir", dlg.GetDirectory())
        #             paths = dlg.GetPaths()
        #             self.doc.OpenAudio(paths[0])
        #         dlg.Destroy()
        # else:
        #     # open an audio file
        #     self.doc.fps = int(self.config.Read("LastFPS", "24"))
        #     self.doc.OpenAudio(path)
        #     if self.doc.sound is None:
        #         self.doc = None
        #     else:
        #         self.doc.voices.append(LipsyncVoice("Voice 1"))
        #         self.doc.currentVoice = self.doc.voices[0]
        #         # check for a .trans file with the same name as the doc
        #         try:
        #             txtFile = file(path[0].rsplit('.', 1)[0] + ".trans", 'r')  # TODO: Check if path is correct
        #             for line in txtFile:
        #                 self.voiceText.AppendText(line)
        #         except:  # TODO: except is too broad
        #             pass
        #
        # if self.doc is not None:
        #     self.SetTitle("%s [%s] - %s" % (self.doc.name, path, appTitle))
        #     self.waveformView.SetDocument(self.doc)
        #     self.mouthView.SetDocument(self.doc)
        #     # menus
        #     self.mainFrame_menubar.Enable(wx.ID_SAVE, True)
        #     self.mainFrame_menubar.Enable(wx.ID_SAVEAS, True)
        #     # toolbar buttons
        #     self.mainFrame_toolbar.EnableTool(wx.ID_SAVE, True)
        #     if self.doc.sound is not None:
        #         self.mainFrame_toolbar.EnableTool(ID_PLAY, True)
        #         self.mainFrame_toolbar.EnableTool(ID_ZOOMIN, True)
        #         self.mainFrame_toolbar.EnableTool(ID_ZOOMOUT, True)
        #         self.mainFrame_toolbar.EnableTool(ID_ZOOM1, True)
        #     # voice list
        #     self.voiceList.Enable(True)
        #     self.newVoiceBut.Enable(True)
        #     self.delVoiceBut.Enable(True)
        #     for voice in self.doc.voices:
        #         self.voiceList.Insert(voice.name, self.voiceList.GetCount())
        #     self.voiceList.SetSelection(0)
        #     # voice controls
        #     self.fpsCtrl.Enable(True)
        #     self.fpsCtrl.SetValue(str(self.doc.fps))
        #     self.voiceName.Enable(True)
        #     self.voiceName.SetValue(self.doc.currentVoice.name)
        #     self.voiceText.Enable(True)
        #     self.voiceText.SetValue(self.doc.currentVoice.text)
        #     self.languageChoice.Enable(True)
        #     self.phonemesetChoice.Enable(True)
        #     self.breakdownBut.Enable(True)
        #     self.reloaddictBut.Enable(True)
        #     self.exportChoice.Enable(True)
        #     self.exportBut.Enable(True)
        #     self.voiceimageBut.Enable(False)
        #     # reload dictionary
        #     self.OnReloadDictionary()
        pass

    def OnSave(self, event=None):
        if self.doc is None:
            return
        if self.doc.path is None:
            self.OnSaveAs()
            return
        self.doc.Save(self.doc.path)

    def OnSaveAs(self, event=None):
        # if self.doc is None:
        #     return
        # dlg = wx.FileDialog(
        #     self, message=_("Save %s File") % appTitle, defaultDir=self.config.Read("WorkingDir", get_main_dir()),
        #     defaultFile="%s" % self.doc.soundPath.rsplit('.', 1)[0] + ".pgo", wildcard=saveWildcard,
        #     style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
        # if dlg.ShowModal() == wx.ID_OK:
        #     self.config.Write("WorkingDir", dlg.GetDirectory())
        #     self.doc.Save(dlg.GetPaths()[0])
        #     self.SetTitle("%s [%s] - %s" % (self.doc.name, dlg.GetPaths()[0], appTitle))
        # dlg.Destroy()
        pass

    def OnClose(self):
        # if self.doc is not None:
        #     self.config.Write("LastFPS", str(self.doc.fps))
        #     del self.doc
        # self.doc = None
        # self.waveformView.SetDocument(self.doc)
        # # menus
        # self.mainFrame_menubar.Enable(wx.ID_SAVE, False)
        # self.mainFrame_menubar.Enable(wx.ID_SAVEAS, False)
        # # toolbar buttons
        # self.mainFrame_toolbar.EnableTool(wx.ID_SAVE, False)
        # self.mainFrame_toolbar.EnableTool(ID_PLAY, False)
        # self.mainFrame_toolbar.EnableTool(ID_STOP, False)
        # self.mainFrame_toolbar.EnableTool(ID_ZOOMIN, False)
        # self.mainFrame_toolbar.EnableTool(ID_ZOOMOUT, False)
        # self.mainFrame_toolbar.EnableTool(ID_ZOOM1, False)
        # # voice controls
        # self.voiceName.Clear()
        # self.voiceName.Enable(False)
        # self.voiceText.Clear()
        # self.voiceText.Enable(False)
        # self.languageChoice.Enable(False)
        # self.phonemesetChoice.Enable(False)
        # self.breakdownBut.Enable(False)
        # self.reloaddictBut.Enable(False)
        # self.exportChoice.Enable(False)
        # self.exportBut.Enable(False)
        # self.voiceimageBut.Enable(False)
        # # voice list
        # self.fpsCtrl.Clear()
        # self.fpsCtrl.Enable(False)
        # self.voiceList.Clear()
        # self.voiceList.Enable(False)
        # self.newVoiceBut.Enable(False)
        # self.delVoiceBut.Enable(False)
        pass

    def OnQuit(self, event=None):
        self.OnClose()
        self.Close(True)

    def OnHelp(self, event=None):
        webbrowser.open("file://%s" % os.path.join(get_main_dir(), "help/index.html"))  # TODO: Fix path

    def OnAbout(self, event=None):
        # dlg = AboutBox(self)
        # dlg.ShowModal()
        # dlg.Destroy()
        pass

    def OnPlay(self, event=None):
        # if (self.doc is not None) and (self.doc.sound is not None):
        #     self.curFrame = -1
        #     self.mainFrame_toolbar.EnableTool(ID_PLAY, False)
        #     self.mainFrame_toolbar.EnableTool(ID_STOP, True)
        #     self.doc.sound.SetCurTime(0)
        #     self.doc.sound.Play(False)
        #     self.timer = wx.Timer(self, ID_PLAY_TICK)
        #     self.timer.Start(250.0 / self.doc.fps)
        pass

    def OnStop(self, event=None):
        # if (self.doc is not None) and (self.doc.sound is not None):
        #     self.doc.sound.Stop()
        #     self.doc.sound.SetCurTime(0)
        #     self.mouthView.SetFrame(0)
        #     self.waveformView.SetFrame(0)
        #     self.mainFrame_toolbar.EnableTool(ID_PLAY, True)
        #     self.mainFrame_toolbar.EnableTool(ID_STOP, False)
        #     self.mainFrame_statusbar.SetStatusText("Stopped", 1)
        pass

    def OnPlayTick(self, event):
        # if (self.doc is not None) and (self.doc.sound is not None):
        #     if self.doc.sound.IsPlaying():
        #         curFrame = int(math.floor(self.doc.sound.CurrentTime() * self.doc.fps))
        #         if curFrame != self.curFrame:
        #             self.curFrame = curFrame
        #             self.mouthView.SetFrame(self.curFrame)
        #             self.waveformView.SetFrame(self.curFrame)
        #             self.mainFrame_statusbar.SetStatusText("Frame: %d" % (curFrame + 1), 1)
        #     else:
        #         self.OnStop()
        #         self.timer.Stop()
        #         del self.timer
        pass

    def OnMouthChoice(self, event):
        # self.mouthView.currentMouth = self.mouthChoice.GetStringSelection()
        # self.mouthView.DrawMe()
        pass
    
    def OnExportChoice(self, event):
        # if self.exportChoice.GetStringSelection() == "Images":
        #     self.voiceimageBut.Enable(True)
        # else:
        #     self.voiceimageBut.Enable(False)
        pass
            

    def OnVoiceName(self, event):
        # if (self.doc is not None) and (self.doc.currentVoice is not None):
        #     self.doc.dirty = True
        #     self.doc.currentVoice.name = self.voiceName.GetValue()
        #     self.voiceList.SetString(self.voiceList.GetSelection(), self.doc.currentVoice.name)
        pass

    def OnVoiceText(self, event):
        # if self.ignoreTextChanges:
        #     return
        # if (self.doc is not None) and (self.doc.currentVoice is not None):
        #     self.doc.dirty = True
        #     self.doc.currentVoice.text = self.voiceText.GetValue()
        pass

    def OnVoiceBreakdown(self, event=None):
        # if (self.doc is not None) and (self.doc.currentVoice is not None):
        #     language = self.languageChoice.GetStringSelection()
        #     phonemeset_name = self.phonemesetChoice.GetStringSelection()
        #     self.phonemeset.Load(phonemeset_name)
        #     self.doc.dirty = True
        #     self.doc.currentVoice.RunBreakdown(self.doc.soundDuration, self, language, self.langman, self.phonemeset)
        #     self.waveformView.UpdateDrawing()
        #     self.ignoreTextChanges = True
        #     self.voiceText.SetValue(self.doc.currentVoice.text)
        #     self.ignoreTextChanges = False
        pass

    def OnVoiceExport(self, event):
        # language = self.languageChoice.GetStringSelection()
        # if (self.doc is not None) and (self.doc.currentVoice is not None):
        #     exporter = self.exportChoice.GetStringSelection()
        #     if exporter == "MOHO":
        #         dlg = wx.FileDialog(
        #             self, message=_("Export Lipsync Data (MOHO)"),
        #             defaultDir=self.config.Read("WorkingDir", get_main_dir()),
        #             defaultFile="%s" % self.doc.soundPath.rsplit('.', 1)[0] + ".dat",
        #             wildcard="Moho switch files (*.dat)|*.dat",
        #             style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
        #         if dlg.ShowModal() == wx.ID_OK:
        #             self.config.Write("WorkingDir", dlg.GetDirectory())
        #             self.doc.currentVoice.Export(dlg.GetPaths()[0])
        #         dlg.Destroy()
        #     elif exporter == "ALELO":
        #         fps = int(self.fpsCtrl.GetValue())
        #         if fps != 100:
        #             dlg = wx.MessageDialog(self, _('FPS is NOT 100 continue? (You will have issues downstream.)'),
        #                                    appTitle,
        #                                    wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_WARNING)
        #             result = dlg.ShowModal()
        #             dlg.Destroy()
        #         else:
        #             result = wx.ID_YES
        #         if result == wx.ID_YES:
        #             dlg = wx.FileDialog(
        #                 self, message=_("Export Lipsync Data (ALELO)"),
        #                 defaultDir=self.config.Read("WorkingDir", get_main_dir()),
        #                 defaultFile="%s" % self.doc.soundPath.rsplit('.', 1)[0] + ".txt",
        #                 wildcard="Alelo timing files (*.txt)|*.txt",
        #                 style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
        #             if dlg.ShowModal() == wx.ID_OK:
        #                 self.config.Write("WorkingDir", dlg.GetDirectory())
        #                 self.doc.currentVoice.ExportAlelo(dlg.GetPaths()[0], language, self.langman)
        #             dlg.Destroy()
        #     elif exporter == "Images":
        #         dlg = wx.FileDialog(
        #             self, message=_("Export Image Strip"), defaultDir=self.config.Read("WorkingDir", get_main_dir()),
        #             defaultFile="%s" % self.doc.soundPath.rsplit('.', 1)[0],
        #             style=wx.FD_SAVE | wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT)
        #         if dlg.ShowModal() == wx.ID_OK:
        #             self.config.Write("WorkingDir", dlg.GetDirectory())
        #             self.doc.currentVoice.ExportImages(dlg.GetPaths()[0], self.mouthChoice.GetStringSelection())
        #         dlg.Destroy()
        pass

    def OnVoiceimagechoose(self, event):
        # language = self.languageChoice.GetStringSelection()
        # if (self.doc is not None) and (self.doc.currentVoice is not None):
        #     voiceimagepath = wx.DirDialog(
        #         self, message=_("Choose Path for Images"), defaultPath=self.config.Read("MouthDir", os.path.join(
        #             os.path.dirname(os.path.abspath(__file__)), "rsrc/mouths/")),
        #         style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.DD_DIR_MUST_EXIST)
        #     if voiceimagepath.ShowModal() == wx.ID_OK:
        #         self.config.Write("MouthDir", voiceimagepath.GetPath())
        #         print(voiceimagepath.GetPath())
        #         full_pattern = re.compile('[^a-zA-Z0-9.\\\/]|_')
        #         supportedimagetypes = re.sub(full_pattern, '', wx.Image.GetImageExtWildcard()).split(".")
        #         for directory, dirnames, filenames in os.walk(voiceimagepath.GetPath()):
        #             self.mouthView.ProcessMouthDir(directory, filenames, supportedimagetypes)
        #         mouthList = list(self.mouthView.mouths.keys())
        #         mouthList.sort()
        #         print(mouthList)
        #         self.mouthChoice.Clear()
        #         for mouth in mouthList:
        #             self.mouthChoice.Append(mouth)
        #         self.mouthChoice.SetSelection(0)
        #         self.mouthView.currentMouth = self.mouthChoice.GetStringSelection()
        #     voiceimagepath.Destroy()
        pass

    def OnFps(self, event):
        # if self.doc is None:
        #     return
        # try:
        #     newFps = int(self.fpsCtrl.GetValue())
        # except:  # TODO: except is too broad
        #     newFps = self.doc.fps
        # if newFps == self.doc.fps:
        #     return
        # self.doc.dirty = True
        # self.doc.fps = newFps
        # if self.doc.fps < 1:
        #     self.doc.fps = 1
        # if self.doc.fps > 120:
        #     self.doc.fps = 120
        # # refresh the document properties
        # self.doc.OpenAudio(self.doc.soundPath)
        # self.waveformView.SetDocument(None)
        # self.waveformView.SetDocument(self.doc)
        # self.mouthView.DrawMe()
        pass

    def OnSelVoice(self, event):
        # if self.doc is None:
        #     return
        # self.ignoreTextChanges = True
        # self.doc.currentVoice = self.doc.voices[self.voiceList.GetSelection()]
        # self.voiceName.SetValue(self.doc.currentVoice.name)
        # self.voiceText.SetValue(self.doc.currentVoice.text)
        # self.ignoreTextChanges = False
        # self.waveformView.UpdateDrawing()
        # self.mouthView.DrawMe()
        pass

    def OnNewVoice(self, event):
        # if self.doc is None:
        #     return
        # self.doc.dirty = True
        # self.doc.voices.append(LipsyncVoice("Voice %d" % (len(self.doc.voices) + 1)))
        # self.doc.currentVoice = self.doc.voices[-1]
        # self.voiceList.Insert(self.doc.currentVoice.name, self.voiceList.GetCount())
        # self.voiceList.SetSelection(self.voiceList.GetCount() - 1)
        # self.ignoreTextChanges = True
        # self.voiceName.SetValue(self.doc.currentVoice.name)
        # self.voiceText.SetValue(self.doc.currentVoice.text)
        # self.ignoreTextChanges = False
        # self.waveformView.UpdateDrawing()
        # self.mouthView.DrawMe()
        pass

    def OnDelVoice(self, event):
        # if (self.doc is None) or (len(self.doc.voices) == 1):
        #     return
        # self.doc.dirty = True
        # newIndex = self.doc.voices.index(self.doc.currentVoice)
        # if newIndex > 0:
        #     newIndex -= 1
        # else:
        #     newIndex = 0
        # self.doc.voices.remove(self.doc.currentVoice)
        # self.doc.currentVoice = self.doc.voices[newIndex]
        # self.voiceList.Clear()
        # for voice in self.doc.voices:
        #     self.voiceList.Insert(voice.name, self.voiceList.GetCount())
        # self.voiceList.SetSelection(newIndex)
        # self.voiceName.SetValue(self.doc.currentVoice.name)
        # self.voiceText.SetValue(self.doc.currentVoice.text)
        # self.waveformView.UpdateDrawing()
        # self.mouthView.DrawMe()
        pass

    def on_reload_dictionary(self, event = None):
        # print("reload the dictionary")
        # lang_config = self.doc.language_manager.language_table[self.languageChoice.GetStringSelection()]
        # self.doc.language_manager.LoadLanguage(lang_config, force=True)
        pass

# end of class LipsyncFrame
