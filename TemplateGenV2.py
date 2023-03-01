# A better template generator
# Includes support for generating .csproj for roslyn and/or compiled mods
# Then also generates example code for those mods
import shutil, json
import os
from xml.dom import minidom

template_mod = """
// Import the Space Warp mod API
using SpaceWarp.API.Mods;

namespace %NAMESPACE%;

// Define our mod class with the [MainMod] attribute
[MainMod]
public class %MODNAME%Mod : Mod {
    // This is our second stage initialization function, all assets and dependencies should be loaded by now.
    public override void OnInitialized() {
        // The mod class contains an Info and Logger class
        Logger.Info($"{Info.name} OnInitialized()");
    }
}
"""

template_configuration = """
using SpaceWarp.API.Configuration;
using Newtonsoft.Json;
namespace %NAMESPACE%;

// Define our config class with the [ModConfig] attribute
[ModConfig]
[JsonObject(MemberSerialization.OptOut)]
public class %MODNAME%Config {
    [ConfigField("funny number")]
    [ConfigDefaultValue(69)]
    public int funny_number;
}
"""

template_gitignore = """
## Ignore Visual Studio temporary files, build results, and
## files generated by popular Visual Studio add-ons.
##
## Get latest from https://github.com/github/gitignore/blob/master/VisualStudio.gitignore

# User-specific files
*.rsuser
*.suo
*.user
*.userosscache
*.sln.docstates

# User-specific files (MonoDevelop/Xamarin Studio)
*.userprefs

# Mono auto generated files
mono_crash.*

# Build results
[Dd]ebug/
[Dd]ebugPublic/
[Rr]elease/
[Rr]eleases/
x64/
x86/
[Aa][Rr][Mm]/
[Aa][Rr][Mm]64/
bld/
[Bb]in/
[Oo]bj/
[Ll]og/
[Ll]ogs/

# Visual Studio 2015/2017 cache/options directory
.vs/
.idea/
# Uncomment if you have tasks that create the project's static files in wwwroot
#wwwroot/

# Visual Studio 2017 auto generated files
Generated\ Files/

# MSTest test Results
[Tt]est[Rr]esult*/
[Bb]uild[Ll]og.*

# NUnit
*.VisualState.xml
TestResult.xml
nunit-*.xml

# Build Results of an ATL Project
[Dd]ebugPS/
[Rr]eleasePS/
dlldata.c

# Benchmark Results
BenchmarkDotNet.Artifacts/

# .NET Core
project.lock.json
project.fragment.lock.json
artifacts/

# StyleCop
StyleCopReport.xml

# Files built by Visual Studio
*_i.c
*_p.c
*_h.h
*.ilk
*.meta
*.obj
*.iobj
*.pch
*.pdb
*.ipdb
*.pgc
*.pgd
*.rsp
*.sbr
*.tlb
*.tli
*.tlh
*.tmp
*.tmp_proj
*_wpftmp.csproj
*.log
*.vspscc
*.vssscc
.builds
*.pidb
*.svclog
*.scc

# Chutzpah Test files
_Chutzpah*

# Visual C++ cache files
ipch/
*.aps
*.ncb
*.opendb
*.opensdf
*.sdf
*.cachefile
*.VC.db
*.VC.VC.opendb

# Visual Studio profiler
*.psess
*.vsp
*.vspx
*.sap

# Visual Studio Trace Files
*.e2e

# TFS 2012 Local Workspace
$tf/

# Guidance Automation Toolkit
*.gpState

# ReSharper is a .NET coding add-in
_ReSharper*/
*.[Rr]e[Ss]harper
*.DotSettings.user

# TeamCity is a build add-in
_TeamCity*

# DotCover is a Code Coverage Tool
*.dotCover

# AxoCover is a Code Coverage Tool
.axoCover/*
!.axoCover/settings.json

# Visual Studio code coverage results
*.coverage
*.coveragexml

# NCrunch
_NCrunch_*
.*crunch*.local.xml
nCrunchTemp_*

# MightyMoose
*.mm.*
AutoTest.Net/

# Web workbench (sass)
.sass-cache/

# Installshield output folder
[Ee]xpress/

# DocProject is a documentation generator add-in
DocProject/buildhelp/
DocProject/Help/*.HxT
DocProject/Help/*.HxC
DocProject/Help/*.hhc
DocProject/Help/*.hhk
DocProject/Help/*.hhp
DocProject/Help/Html2
DocProject/Help/html

# Click-Once directory
publish/

# Publish Web Output
*.[Pp]ublish.xml
*.azurePubxml
# Note: Comment the next line if you want to checkin your web deploy settings,
# but database connection strings (with potential passwords) will be unencrypted
*.pubxml
*.publishproj

# Microsoft Azure Web App publish settings. Comment the next line if you want to
# checkin your Azure Web App publish settings, but sensitive information contained
# in these scripts will be unencrypted
PublishScripts/

# NuGet Packages
*.nupkg
# NuGet Symbol Packages
*.snupkg
# The packages folder can be ignored because of Package Restore
**/[Pp]ackages/*
# except build/, which is used as an MSBuild target.
!**/[Pp]ackages/build/
# Uncomment if necessary however generally it will be regenerated when needed
#!**/[Pp]ackages/repositories.config
# NuGet v3's project.json files produces more ignorable files
*.nuget.props
*.nuget.targets

# Microsoft Azure Build Output
csx/
*.build.csdef

# Microsoft Azure Emulator
ecf/
rcf/

# Windows Store app package directories and files
AppPackages/
BundleArtifacts/
Package.StoreAssociation.xml
_pkginfo.txt
*.appx
*.appxbundle
*.appxupload

# Visual Studio cache files
# files ending in .cache can be ignored
*.[Cc]ache
# but keep track of directories ending in .cache
!?*.[Cc]ache/

# Others
ClientBin/
~$*
*~
*.dbmdl
*.dbproj.schemaview
*.jfm
*.pfx
*.publishsettings
orleans.codegen.cs

# Including strong name files can present a security risk
# (https://github.com/github/gitignore/pull/2483#issue-259490424)
#*.snk

# Since there are multiple workflows, uncomment next line to ignore bower_components
# (https://github.com/github/gitignore/pull/1529#issuecomment-104372622)
#bower_components/

# RIA/Silverlight projects
Generated_Code/

# Backup & report files from converting an old project file
# to a newer Visual Studio version. Backup files are not needed,
# because we have git ;-)
_UpgradeReport_Files/
Backup*/
UpgradeLog*.XML
UpgradeLog*.htm
ServiceFabricBackup/
*.rptproj.bak

# SQL Server files
*.mdf
*.ldf
*.ndf

# Business Intelligence projects
*.rdl.data
*.bim.layout
*.bim_*.settings
*.rptproj.rsuser
*- [Bb]ackup.rdl
*- [Bb]ackup ([0-9]).rdl
*- [Bb]ackup ([0-9][0-9]).rdl

# Microsoft Fakes
FakesAssemblies/

# GhostDoc plugin setting file
*.GhostDoc.xml

# Node.js Tools for Visual Studio
.ntvs_analysis.dat
node_modules/

# Visual Studio 6 build log
*.plg

# Visual Studio 6 workspace options file
*.opt

# Visual Studio 6 auto-generated workspace file (contains which files were open etc.)
*.vbw

# Visual Studio LightSwitch build output
**/*.HTMLClient/GeneratedArtifacts
**/*.DesktopClient/GeneratedArtifacts
**/*.DesktopClient/ModelManifest.xml
**/*.Server/GeneratedArtifacts
**/*.Server/ModelManifest.xml
_Pvt_Extensions

# Paket dependency manager
.paket/paket.exe
paket-files/

# FAKE - F# Make
.fake/

# CodeRush personal settings
.cr/personal

# Python Tools for Visual Studio (PTVS)
__pycache__/
*.pyc

# Cake - Uncomment if you are using it
# tools/**
# !tools/packages.config

# Tabs Studio
*.tss

# Telerik's JustMock configuration file
*.jmconfig

# BizTalk build output
*.btp.cs
*.btm.cs
*.odx.cs
*.xsd.cs

# OpenCover UI analysis results
OpenCover/

# Azure Stream Analytics local run output
ASALocalRun/

# MSBuild Binary and Structured Log
*.binlog

# NVidia Nsight GPU debugger configuration file
*.nvuser

# MFractors (Xamarin productivity tool) working folder
.mfractor/

# Local History for Visual Studio
.localhistory/

# BeatPulse healthcheck temp database
healthchecksdb

# Backup folder for Package Reference Convert tool in Visual Studio 2017
MigrationBackup/

# Ionide (cross platform F# VS Code tools) working folder
.ionide/

# Build script folder
build/

# Idea folder
.idea
"""

template_external_gitignore = """
*
!.gitignore
"""

def find_ksp2_install_path():
    # Checks if Operating System is NOT Windows
    if os.path != "nt":
        steam_install_folder = ""
        return steam_install_folder
    else:
        # Look for the game in Steam library folders
        steam_path = os.path.join(os.getenv("ProgramFiles(x86)"), "Steam")
        steam_library_folders_file = os.path.join(
            steam_path, "steamapps", "libraryfolders.vdf"
        )
        steam_install_folder = os.path.join(
            steam_path, "steamapps", "common", "Kerbal Space Program 2"
        )

        if os.path.exists(steam_library_folders_file):
            with open(steam_library_folders_file) as f:
                for line in f:
                    if "BaseInstallFolder" in line:
                        steam_library_path = line.strip().split('"')[3]
                        if os.path.exists(
                            os.path.join(
                                steam_library_path,
                                "steamapps",
                                "appmanifest_1406800.acf",
                            )
                        ):
                            steam_install_folder = os.path.join(
                                steam_library_path,
                                "steamapps",
                                "common",
                                "Kerbal Space Program 2",
                            )
                            break

        # Look for the game in default installation path
        if not os.path.exists(steam_install_folder):
            default_install_folder = os.path.join(
                os.getenv("ProgramFiles"), "Private Division", "Kerbal Space Program 2"
            )
            if os.path.exists(default_install_folder):
                steam_install_folder = default_install_folder

mode = 0 # 0 = roslyn, 1 = compiled, 2 = both (roslyn template), 3 = both (compiled template)

mod_id = ""
mod_name = ""
mod_author = ""

print("Space Warp Mod Setup Wizard")
while True:
    compilation_mode = input("Is this mod going to be (R)oslyn, (C)ompiled, or (B)oth: ")
    if not compilation_mode:
        print("Please input a mode")
    else:
        if compilation_mode.lower().startswith("r"):
            mode = 0
            break
        elif compilation_mode.lower().startswith("c"):
            mode = 1
            break
        elif compilation_mode.lower().startswith("b"):
            while True:
                template_mode = input("Do you want the template to be (R)oslyn or (C)ompiled: ")
                if not template_mode:
                    print("Please input a template mode")
                else:
                    if template_mode.lower().startswith("r"):
                        mode = 2
                        break
                    elif template_mode.lower().startswith("c"):
                        mode = 3
                        break
                    else:
                        print("Please input one of the available options")
            break
        print("Please input one of the available options")


while True:
    mod_id = input("What is the ID of the mod (This should be in snake_case): ")
    if not mod_id:
        print("Mod ID cannot be empty, please try again.")
    else:
        break



while True:
    mod_author = input("Who is the author of the mod: ")
    if not mod_author:
        print("Mod author cannot be empty, please try again.")
    else:
        break

while True:
    mod_name = input("What is the name of the mod: ")
    if not mod_name:
        print("Mod name cannot be empty, please try again.")
    else:
        break

mod_description = input("What is a short description of the mod: ")
mod_source = input("What is the source link of the mod: ")
mod_version = input("What is the starting version of the mod: ")
mod_ksp_min_version = input(
    "What is the minimum version of KSP2 this mod will accept: "
)
mod_ksp_max_version = input(
    "What is the maximum version of KSP2 this mod will accept: "
)

steam_install_folder = find_ksp2_install_path()

if os.path.exists(steam_install_folder):
    print(f"Kerbal Space Program 2 is installed at {steam_install_folder}")
else:
    steam_install_folder = input(
        "Could not find the installation path for Kerbal Space Program 2.\nPlease enter the path to the KSP2 installation folder manually: "
    )

managed_path = os.path.join(steam_install_folder, "KSP2_x64_Data", "Managed")
space_warp_path = ""
bepinex_path = ""
use_bepinex = False
if os.path.exists(os.path.join(steam_install_folder, "SpaceWarp", "core")):
    space_warp_path = os.path.join(steam_install_folder, "SpaceWarp", "core")
elif os.path.exists(os.path.join(steam_install_folder,"BepInEx","SpaceWarp")):
    space_warp_path = os.path.join(steam_install_folder, "BepInEx","SpaceWarp")
    use_bepinex = True
    bepinex_path = os.path.join(steam_install_folder,"BepInEx","core")
else:
    print("Could not find a space warp installation, are you sure space warp is installed?")

def touch(name):
    open(name,"w").close()

mod_id_title = mod_id.replace("_", " ").title().replace(" ", "")

os.mkdir(mod_id)
os.mkdir(f"{mod_id}/external_dlls")
os.mkdir(f"{mod_id}/{mod_id}")
os.mkdir(f"{mod_id}/{mod_id}/assets")
os.mkdir(f"{mod_id}/{mod_id}/assets/bundles")
touch(f"{mod_id}/{mod_id}/assets/bundles/BUNDLES_HERE")
os.mkdir(f"{mod_id}/{mod_id}/bin")
touch(f"{mod_id}/{mod_id}/bin/BINARIES_HERE")
os.mkdir(f"{mod_id}/{mod_id}/config")
touch(f"{mod_id}/{mod_id}/config/CONFIGURATION_HERE")
os.mkdir(f"{mod_id}/{mod_id}/localization")
touch(f"{mod_id}/{mod_id}/localization/LOCALIZATION_HERE")
os.mkdir(f"{mod_id}/{mod_id}/addressables")
touch(f"{mod_id}/{mod_id}/localization/ADDRESSABLES_HERE")
if mode == 0 or mode >= 2:
    os.mkdir(f"{mod_id}/{mod_id}/src")
    os.mkdir(f"{mod_id}/{mod_id}/src/{mod_id_title}")
if mode == 1 or mode >= 2:
    os.mkdir(f"{mod_id}/{mod_id_title}Project")
    os.mkdir(f"{mod_id}/{mod_id_title}Project/{mod_id_title}")


external_dlls = f"{mod_id}/external_dlls"
release_folder = f"{mod_id}/{mod_id}"

dll_list = []


for filename in os.listdir(space_warp_path):
    if (filename.endswith(".dll")):
        shutil.copy2(os.path.join(space_warp_path, filename), external_dlls)
        dll_list.append(filename)

if use_bepinex:
    for filename in os.listdir(bepinex_path):
        if filename.endswith(".dll") and filename.lower().find("bepinex") == -1:
            shutil.copy2(os.path.join(bepinex_path, filename), external_dlls)
            dll_list.append(filename)
    
for filename in os.listdir(managed_path):
    if filename.endswith(".dll"):
        shutil.copy2(os.path.join(managed_path, filename), external_dlls)
        dll_list.append(filename)

with open(f"{external_dlls}/.gitignore", "w") as external_gitignore:
    external_gitignore.write(template_external_gitignore)

with open(f"{mod_id}/.gitignore","w") as main_gitignore:
    main_gitignore.write(template_gitignore)

with open(f"{release_folder}/modinfo.json", "w") as modinfo:
    modinfo.write(
        json.dumps(
            {
                "mod_id": mod_id,
                "author": mod_author,
                "name": mod_name,
                "description": mod_description,
                "source": mod_source,
                "version": mod_version,
                "dependencies": [],
                "ksp2_version": {
                    "min": mod_ksp_min_version,
                    "max": mod_ksp_max_version,
                },
            },
            indent=4,
        )
    )

with open(f"{mod_id}/README.md", "w") as readme:
    readme.write("# Usage")
    readme.write("Copy all space warp dlls and ksp dlls into external dlls")
    readme.write(
        "# Template Mod"
    )


with open(f"{release_folder}/README.json", "w") as readme:
    readme.write("# Default Readme")
code_folder = ""
if mode == 1 or mode == 3:
    code_folder = f"{mod_id}/{mod_id_title}Project/{mod_id_title}"
else:
    code_folder = f"{mod_id}/{mod_id}/src"

with open(f"{code_folder}/{mod_id_title}Mod.cs", "w") as default_code:
    default_code.write(
        template_mod.replace("%NAMESPACE%",mod_id_title).replace("%MODNAME%",mod_id_title)
    )

with open(f"{code_folder}/{mod_id_title}Config.cs", "w") as default_code:
    default_code.write(
        template_configuration.replace("%NAMESPACE%",mod_id_title).replace("%MODNAME%",mod_id_title)
    )

if mode == 0 or mode >= 2:

    with open(f"{mod_id}/{mod_id}/.gitignore","w") as main_gitignore:
        main_gitignore.write(template_gitignore)

if mode == 1 or mode >= 2:
    with open(f"{mod_id}/{mod_id_title}Project/.gitignore","w") as main_gitignore:
        main_gitignore.write(template_gitignore)



def quick_create_property(root, name, text):
    a = root.createElement(name)
    b = root.createTextNode(text)
    a.appendChild(b)
    return a


def gen_csproj(csproj_name, dll_list, is_compiled=False):
    root = minidom.Document()
    xml = root.createElement("Project")
    xml.setAttribute("Sdk", "Microsoft.NET.Sdk")
    root.appendChild(xml)
    propertyGroup = root.createElement("PropertyGroup")
    xml.appendChild(propertyGroup)
    propertyGroup.appendChild(
        quick_create_property(root, "TargetFramework", "net472")
    )
    propertyGroup.appendChild(quick_create_property(root, "AllowUnsafeBlocks", "true"))
    propertyGroup.appendChild(quick_create_property(root, "LangVersion", "latest"))
    propertyGroup.appendChild(quick_create_property(root, "ImplicitUsings", "true"))

    itemGroup = root.createElement("ItemGroup")
    xml.appendChild(itemGroup)

    refs = [
        os.path.join("..","external_dlls",f"{dll}") for dll in dll_list
    ]

    for ref in refs:
        element = root.createElement("Reference")
        element.setAttribute("Include", ref)
        itemGroup.appendChild(element)

    if is_compiled:
        after_build_group = root.createElement("PropertyGroup")
        xml.appendChild(after_build_group)
        after_build_group.appendChild(
            quick_create_property(root,"PostBuildEvent","""
"$(ProjectDir)pdb2mdb\\pdb2mdb.exe" "$(TargetPath)"
copy /Y "$(TargetDir)$(ProjectName).dll" "../%MOD_ID%/bin/$(ProjectName).dll"
copy /Y "$(TargetDir)$(ProjectName).pdb" "../%MOD_ID%/bin/$(ProjectName).pdb"
copy /Y "$(TargetDir)$(ProjectName).dll.mdb" "../%MOD_ID%/bin/$(ProjectName).dll.mdb"
""".replace("%MOD_ID%",mod_id))
        )

    xml_str = root.toprettyxml(indent="  ")
    with open(csproj_name + ".csproj", "w") as csproj:
        csproj.write(xml_str)

if mode == 0 or mode >= 2:
    gen_csproj(f"{mod_id}/{mod_id}/{mod_id_title}",dll_list,False)
if mode == 1 or mode >= 2:
    gen_csproj(f"{mod_id}/{mod_id_title}Project/{mod_id_title}",dll_list,True)