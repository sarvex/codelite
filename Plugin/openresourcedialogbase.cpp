//////////////////////////////////////////////////////////////////////
// This file was auto-generated by codelite's wxCrafter Plugin
// wxCrafter project file: openresourcedialogbase.wxcp
// Do not modify this file by hand!
//////////////////////////////////////////////////////////////////////

#include "openresourcedialogbase.h"


// Declare the bitmap loading function
extern void wxCFB13InitBitmapResources();

static bool bBitmapLoaded = false;


OpenResourceDialogBase::OpenResourceDialogBase(wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style)
    : wxDialog(parent, id, title, pos, size, style)
{
    if ( !bBitmapLoaded ) {
        // We need to initialise the default bitmap handler
        wxXmlResource::Get()->AddHandler(new wxBitmapXmlHandler);
        wxCFB13InitBitmapResources();
        bBitmapLoaded = true;
    }
    
    wxBoxSizer* mainSizer = new wxBoxSizer(wxVERTICAL);
    this->SetSizer(mainSizer);
    
    m_textCtrlResourceName = new wxTextCtrl(this, wxID_ANY, wxT(""), wxDefaultPosition, wxSize(-1, -1), wxTE_PROCESS_ENTER);
    m_textCtrlResourceName->SetToolTip(_("Type resource name to open.\nYou may use a space delimited list of words to narrow down the list of choices\ne.g. Typing: 'Open Dialog' will include results that contain both words \"Open\" _and_ \"Dialog\""));
    m_textCtrlResourceName->SetFocus();
    #if wxVERSION_NUMBER >= 3000
    m_textCtrlResourceName->SetHint(wxT(""));
    #endif
    
    mainSizer->Add(m_textCtrlResourceName, 0, wxALL|wxEXPAND, 5);
    
    m_dataview = new wxDataViewCtrl(this, wxID_ANY, wxDefaultPosition, wxSize(-1,-1), wxDV_VERT_RULES|wxDV_ROW_LINES|wxDV_SINGLE);
    
    m_dataviewModel = new OpenResourceDialogModel;
    m_dataviewModel->SetColCount( 2 );
    m_dataview->AssociateModel(m_dataviewModel.get() );
    
    mainSizer->Add(m_dataview, 1, wxALL|wxEXPAND, 5);
    
    m_dataview->AppendIconTextColumn(_("Name"), m_dataview->GetColumnCount(), wxDATAVIEW_CELL_INERT, 200, wxALIGN_LEFT);
    m_dataview->AppendTextColumn(_("Full Name"), m_dataview->GetColumnCount(), wxDATAVIEW_CELL_INERT, 500, wxALIGN_LEFT);
    wxFlexGridSizer* fgSizer1 = new wxFlexGridSizer(0, 2, 0, 0);
    fgSizer1->SetFlexibleDirection( wxBOTH );
    fgSizer1->SetNonFlexibleGrowMode( wxFLEX_GROWMODE_SPECIFIED );
    
    mainSizer->Add(fgSizer1, 0, wxALL|wxALIGN_LEFT, 5);
    
    m_checkBoxFiles = new wxCheckBox(this, wxID_ANY, _("Show files"), wxDefaultPosition, wxSize(-1,-1), 0);
    m_checkBoxFiles->SetValue(false);
    
    fgSizer1->Add(m_checkBoxFiles, 0, wxALL|wxEXPAND, 5);
    
    m_checkBoxShowSymbols = new wxCheckBox(this, wxID_ANY, _("Show symbols"), wxDefaultPosition, wxSize(-1,-1), 0);
    m_checkBoxShowSymbols->SetValue(false);
    
    fgSizer1->Add(m_checkBoxShowSymbols, 0, wxALL|wxEXPAND, 5);
    
    m_stdBtnSizer2 = new wxStdDialogButtonSizer();
    
    mainSizer->Add(m_stdBtnSizer2, 0, wxALL|wxALIGN_CENTER_HORIZONTAL, 5);
    
    m_buttonOK = new wxButton(this, wxID_OK, wxT(""), wxDefaultPosition, wxSize(-1, -1), 0);
    m_buttonOK->SetDefault();
    m_stdBtnSizer2->AddButton(m_buttonOK);
    
    m_button6 = new wxButton(this, wxID_CANCEL, wxT(""), wxDefaultPosition, wxSize(-1, -1), 0);
    m_stdBtnSizer2->AddButton(m_button6);
    m_stdBtnSizer2->Realize();
    
    SetName(wxT("OpenResourceDialogBase"));
    SetMinSize( wxSize(400,300) );
    SetSizeHints(600,400);
    if ( GetSizer() ) {
         GetSizer()->Fit(this);
    }
    CentreOnParent(wxBOTH);
#if wxVERSION_NUMBER >= 2900
    if(!wxPersistenceManager::Get().Find(this)) {
        wxPersistenceManager::Get().RegisterAndRestore(this);
    } else {
        wxPersistenceManager::Get().Restore(this);
    }
#endif
    // Connect events
    m_textCtrlResourceName->Connect(wxEVT_KEY_DOWN, wxKeyEventHandler(OpenResourceDialogBase::OnKeyDown), NULL, this);
    m_textCtrlResourceName->Connect(wxEVT_COMMAND_TEXT_UPDATED, wxCommandEventHandler(OpenResourceDialogBase::OnText), NULL, this);
    m_textCtrlResourceName->Connect(wxEVT_COMMAND_TEXT_ENTER, wxCommandEventHandler(OpenResourceDialogBase::OnEnter), NULL, this);
    m_dataview->Connect(wxEVT_COMMAND_DATAVIEW_ITEM_ACTIVATED, wxDataViewEventHandler(OpenResourceDialogBase::OnEntryActivated), NULL, this);
    m_dataview->Connect(wxEVT_COMMAND_DATAVIEW_SELECTION_CHANGED, wxDataViewEventHandler(OpenResourceDialogBase::OnEntrySelected), NULL, this);
    m_checkBoxFiles->Connect(wxEVT_COMMAND_CHECKBOX_CLICKED, wxCommandEventHandler(OpenResourceDialogBase::OnCheckboxfilesCheckboxClicked), NULL, this);
    m_checkBoxShowSymbols->Connect(wxEVT_COMMAND_CHECKBOX_CLICKED, wxCommandEventHandler(OpenResourceDialogBase::OnCheckboxshowsymbolsCheckboxClicked), NULL, this);
    m_buttonOK->Connect(wxEVT_COMMAND_BUTTON_CLICKED, wxCommandEventHandler(OpenResourceDialogBase::OnOK), NULL, this);
    m_buttonOK->Connect(wxEVT_UPDATE_UI, wxUpdateUIEventHandler(OpenResourceDialogBase::OnOKUI), NULL, this);
    
}

OpenResourceDialogBase::~OpenResourceDialogBase()
{
    m_textCtrlResourceName->Disconnect(wxEVT_KEY_DOWN, wxKeyEventHandler(OpenResourceDialogBase::OnKeyDown), NULL, this);
    m_textCtrlResourceName->Disconnect(wxEVT_COMMAND_TEXT_UPDATED, wxCommandEventHandler(OpenResourceDialogBase::OnText), NULL, this);
    m_textCtrlResourceName->Disconnect(wxEVT_COMMAND_TEXT_ENTER, wxCommandEventHandler(OpenResourceDialogBase::OnEnter), NULL, this);
    m_dataview->Disconnect(wxEVT_COMMAND_DATAVIEW_ITEM_ACTIVATED, wxDataViewEventHandler(OpenResourceDialogBase::OnEntryActivated), NULL, this);
    m_dataview->Disconnect(wxEVT_COMMAND_DATAVIEW_SELECTION_CHANGED, wxDataViewEventHandler(OpenResourceDialogBase::OnEntrySelected), NULL, this);
    m_checkBoxFiles->Disconnect(wxEVT_COMMAND_CHECKBOX_CLICKED, wxCommandEventHandler(OpenResourceDialogBase::OnCheckboxfilesCheckboxClicked), NULL, this);
    m_checkBoxShowSymbols->Disconnect(wxEVT_COMMAND_CHECKBOX_CLICKED, wxCommandEventHandler(OpenResourceDialogBase::OnCheckboxshowsymbolsCheckboxClicked), NULL, this);
    m_buttonOK->Disconnect(wxEVT_COMMAND_BUTTON_CLICKED, wxCommandEventHandler(OpenResourceDialogBase::OnOK), NULL, this);
    m_buttonOK->Disconnect(wxEVT_UPDATE_UI, wxUpdateUIEventHandler(OpenResourceDialogBase::OnOKUI), NULL, this);
    
}
