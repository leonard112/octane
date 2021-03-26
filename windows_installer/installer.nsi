!define PACKAGE_NAME "octanescript-installer"
!define VERSION "DEV" 

Name "OctaneScript ${VERSION}"
OutFile "${PACKAGE_NAME}.exe"
InstallDir "C:\Program Files\OctaneScript"
ShowInstDetails Show

!include "MUI2.nsh"
!define MUI_ICON "../images/octanescript_logo.ico"
!define MUI_UNICON "../images/octanescript_logo.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "../images/octanescript-logo.bmp"
!define MUI_WELCOMEPAGE_TEXT "OctaneScript is a scripting language built from Python. OctaneScript is currenly in it's early alpha stages. Feel free to use this software for whatever you wish, but ensure that you review this software's license (MIT) if you consider using this software for anything more than exploration and learning."
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "OctaneScript"
!define MUI_LICENSEPAGE_TEXT_TOP "LICENSE INFORMATION"
!define MUI_LICENSEPAGE_TEXT_BOTTOM "By clicking 'I Agree', you accept the terms of the license."
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"
 
Section
    SetOutPath $INSTDIR
	
	File "os.exe"
	File "LICENSE"
 
    WriteUninstaller "$INSTDIR\uninstall.exe"
	EnVar::AddValue "PATH" "$INSTDIR\"
	Pop $0
	DetailPrint "EnVar::AddValue returned=|$0|"
	
SectionEnd
 
Section "uninstall"
    Delete "$INSTDIR\uninstall.exe"
	Delete "$INSTDIR\os.exe"
	Delete "$INSTDIR\LICENSE"
    RMDir $INSTDIR
	EnVar::DeleteValue "PATH" "$INSTDIR\"
	Pop $0
	DetailPrint "EnVar::DeleteValue returned=|$0|"
SectionEnd