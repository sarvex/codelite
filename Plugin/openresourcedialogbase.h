//////////////////////////////////////////////////////////////////////
// This file was auto-generated by codelite's wxCrafter Plugin
// wxCrafter project file: openresourcedialogbase.wxcp
// Do not modify this file by hand!
//////////////////////////////////////////////////////////////////////

#ifndef CODELITE_PLUGIN_OPENRESOURCEDIALOGBASE_BASE_CLASSES_H
#define CODELITE_PLUGIN_OPENRESOURCEDIALOGBASE_BASE_CLASSES_H

#include <wx/settings.h>
#include <wx/xrc/xmlres.h>
#include <wx/xrc/xh_bmp.h>
#include <wx/dialog.h>
#include <wx/iconbndl.h>
#include <wx/artprov.h>
#include <wx/sizer.h>
#include <wx/textctrl.h>
#include <wx/dataview.h>
#include "openresourcedialogmodel.h"
#include <wx/checkbox.h>
#include <wx/button.h>
#if wxVERSION_NUMBER >= 2900
#include <wx/persist.h>
#include <wx/persist/toplevel.h>
#include <wx/persist/bookctrl.h>
#include <wx/persist/treebook.h>
#endif

class OpenResourceDialogBase : public wxDialog
{
protected:
    wxTextCtrl* m_textCtrlResourceName;
    wxDataViewCtrl* m_dataview;
    wxObjectDataPtr<OpenResourceDialogModel> m_dataviewModel;

    wxCheckBox* m_checkBoxFiles;
    wxCheckBox* m_checkBoxShowSymbols;
    wxStdDialogButtonSizer* m_stdBtnSizer2;
    wxButton* m_buttonOK;
    wxButton* m_button6;

protected:
    virtual void OnKeyDown(wxKeyEvent& event) { event.Skip(); }
    virtual void OnText(wxCommandEvent& event) { event.Skip(); }
    virtual void OnEnter(wxCommandEvent& event) { event.Skip(); }
    virtual void OnEntryActivated(wxDataViewEvent& event) { event.Skip(); }
    virtual void OnEntrySelected(wxDataViewEvent& event) { event.Skip(); }
    virtual void OnCheckboxfilesCheckboxClicked(wxCommandEvent& event) { event.Skip(); }
    virtual void OnCheckboxshowsymbolsCheckboxClicked(wxCommandEvent& event) { event.Skip(); }
    virtual void OnOK(wxCommandEvent& event) { event.Skip(); }
    virtual void OnOKUI(wxUpdateUIEvent& event) { event.Skip(); }

public:
    wxTextCtrl* GetTextCtrlResourceName() { return m_textCtrlResourceName; }
    wxDataViewCtrl* GetDataview() { return m_dataview; }
    wxCheckBox* GetCheckBoxFiles() { return m_checkBoxFiles; }
    wxCheckBox* GetCheckBoxShowSymbols() { return m_checkBoxShowSymbols; }
    OpenResourceDialogBase(wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = _("Open Resource"), const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize(600,400), long style = wxDEFAULT_DIALOG_STYLE|wxRESIZE_BORDER);
    virtual ~OpenResourceDialogBase();
};

#endif
