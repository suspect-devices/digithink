The database created when upgrading the trac site does not work with wikiprintbook. 

Here is a workaround while I debug the issue.

	
	root@herbert:~# mkdir /tmp/docsdump
	root@herbert:~# trac-admin /var/trac/serverdocs/env wiki dump /tmp/docsdump/
	 WikiNewPage => /tmp/docsdump/WikiNewPage
	 PlatformIO => /tmp/docsdump/PlatformIO
	 GoodByeOpenstack => /tmp/docsdump/GoodByeOpenstack
	 Esp8266 => /tmp/docsdump/Esp8266
	 Mullein => /tmp/docsdump/Mullein
	 PageTemplates => /tmp/docsdump/PageTemplates
	 DockerInstallNotes => /tmp/docsdump/DockerInstallNotes
	 Ubuntu18.04Notes => /tmp/docsdump/Ubuntu18.04Notes
	 DL380RaidController => /tmp/docsdump/DL380RaidController
	 ResliverFailureNotes => /tmp/docsdump/ResliverFailureNotes
	 InitialImpressions => /tmp/docsdump/InitialImpressions
	 InterMapTxt => /tmp/docsdump/InterMapTxt
	 RecentChanges => /tmp/docsdump/RecentChanges
	 OpenWRTonLinkSysEA3500 => /tmp/docsdump/OpenWRTonLinkSysEA3500
	 OpenWRT => /tmp/docsdump/OpenWRT
	 ZFSDiskReplacement => /tmp/docsdump/ZFSDiskReplacement
	 InterWiki => /tmp/docsdump/InterWiki
	 BleedingEdgeServer => /tmp/docsdump/BleedingEdgeServer
	 DiskRecovery => /tmp/docsdump/DiskRecovery
	 CamelCase => /tmp/docsdump/CamelCase
	 WikiStart => /tmp/docsdump/WikiStart
	 7900NWashburne => /tmp/docsdump/7900NWashburne
	 Feurig => /tmp/docsdump/Feurig
	 ILO3Notes => /tmp/docsdump/ILO3Notes
	 SandBox => /tmp/docsdump/SandBox
	 LEDE => /tmp/docsdump/LEDE
	 FunWithLinuxDisks => /tmp/docsdump/FunWithLinuxDisks
	 OpenVPNOnLEDE => /tmp/docsdump/OpenVPNOnLEDE
	 ZFSMirroredFromExisting => /tmp/docsdump/ZFSMirroredFromExisting
	 ZFSNightmaresPorted2Linux => /tmp/docsdump/ZFSNightmaresPorted2Linux
	 LXDContainerWithDockerNotes => /tmp/docsdump/LXDContainerWithDockerNotes
	 MigratingServicesToLXC => /tmp/docsdump/MigratingServicesToLXC
	 kb2018InstallBashHistory => /tmp/docsdump/kb2018InstallBashHistory
	 MigrateUsers => /tmp/docsdump/MigrateUsers
	 ZFSHotSwappingMirrorsOnLivePools => /tmp/docsdump/ZFSHotSwappingMirrorsOnLivePools
	 CloudServerConfiguration => /tmp/docsdump/CloudServerConfiguration
	 ContainerShipInstallation => /tmp/docsdump/ContainerShipInstallation
	 OpenWrtE900FirmwareBuild => /tmp/docsdump/OpenWrtE900FirmwareBuild
	 InterTrac => /tmp/docsdump/InterTrac
	 BS2020InstallNotes => /tmp/docsdump/BS2020InstallNotes
	 TitleIndex => /tmp/docsdump/TitleIndex
	 UbuntuMailServerSetup => /tmp/docsdump/UbuntuMailServerSetup
	 Annie => /tmp/docsdump/Annie
	 GlassesOkay => /tmp/docsdump/GlassesOkay
	 CloudServerDocs => /tmp/docsdump/CloudServerDocs
	 TicketQuery => /tmp/docsdump/TicketQuery
	 OperationsGuide => /tmp/docsdump/OperationsGuide
	 DiskLayoutOnBS2020 => /tmp/docsdump/DiskLayoutOnBS2020
	 LXDContainersWithProfile => /tmp/docsdump/LXDContainersWithProfile
	 Nigel => /tmp/docsdump/Nigel
	 Idrac6 => /tmp/docsdump/Idrac6
	 AutoMatingContainerUpdates => /tmp/docsdump/AutoMatingContainerUpdates
	 OpenWRTonMR3020 => /tmp/docsdump/OpenWRTonMR3020
	 NewTracContainer => /tmp/docsdump/NewTracContainer
	 SuspectDevices => /tmp/docsdump/SuspectDevices
	 SystemUpdates => /tmp/docsdump/SystemUpdates
	 CaptiveRaidController => /tmp/docsdump/CaptiveRaidController
	
* clear out any existing pages on the disposable wiki site
	
	root@herbert:~# trac-admin /var/trac/devel/env wiki remove *
	
	Deleted pages
	---------------
	RecentChanges
	InterWiki
	TicketQuery
	CamelCase
	WikiStart
	PageTemplates
	InterTrac
	SandBox
	TitleIndex
	InterMapTxt
	OperationsGuide
	
* load the pages onto the new site.
( may be missing a step for the images )
	
	root@herbert:~# trac-admin /var/trac/devel/env wiki load /tmp/
	.ICE-unix/                                                                        env/
	.Test-unix/                                                                       files/
	.X11-unix/                                                                        netplan_141i3qzp/
	.XIM-unix/                                                                        systemd-private-a1ddddc0dcb0479fad96fa3c064e61e2-apache2.service-Icqav1/
	.font-unix/                                                                       systemd-private-a1ddddc0dcb0479fad96fa3c064e61e2-systemd-resolved.service-gIdUDr/
	docsdump/                                                                         tracback28nov18.tgz
	root@herbert:~# trac-admin /var/trac/devel/env wiki load /tmp/docsdump/
	  ZFSMirroredFromExisting imported from /tmp/docsdump/ZFSMirroredFromExisting
	  BS2020InstallNotes imported from /tmp/docsdump/BS2020InstallNotes
	  SandBox imported from /tmp/docsdump/SandBox
	  MigrateUsers imported from /tmp/docsdump/MigrateUsers
	  UbuntuMailServerSetup imported from /tmp/docsdump/UbuntuMailServerSetup
	  Idrac6 imported from /tmp/docsdump/Idrac6
	  DockerInstallNotes imported from /tmp/docsdump/DockerInstallNotes
	  WikiNewPage imported from /tmp/docsdump/WikiNewPage
	  WikiStart imported from /tmp/docsdump/WikiStart
	  kb2018InstallBashHistory imported from /tmp/docsdump/kb2018InstallBashHistory
	  Feurig imported from /tmp/docsdump/Feurig
	  PageTemplates imported from /tmp/docsdump/PageTemplates
	  ZFSHotSwappingMirrorsOnLivePools imported from /tmp/docsdump/ZFSHotSwappingMirrorsOnLivePools
	  ILO3Notes imported from /tmp/docsdump/ILO3Notes
	  SystemUpdates imported from /tmp/docsdump/SystemUpdates
	  OperationsGuide imported from /tmp/docsdump/OperationsGuide
	  CaptiveRaidController imported from /tmp/docsdump/CaptiveRaidController
	  DL380RaidController imported from /tmp/docsdump/DL380RaidController
	  OpenWRTonMR3020 imported from /tmp/docsdump/OpenWRTonMR3020
	  OpenWRT imported from /tmp/docsdump/OpenWRT
	  RecentChanges imported from /tmp/docsdump/RecentChanges
	  LEDE imported from /tmp/docsdump/LEDE
	  CloudServerConfiguration imported from /tmp/docsdump/CloudServerConfiguration
	  GlassesOkay imported from /tmp/docsdump/GlassesOkay
	  OpenWRTonLinkSysEA3500 imported from /tmp/docsdump/OpenWRTonLinkSysEA3500
	  AutoMatingContainerUpdates imported from /tmp/docsdump/AutoMatingContainerUpdates
	  DiskLayoutOnBS2020 imported from /tmp/docsdump/DiskLayoutOnBS2020
	  CamelCase imported from /tmp/docsdump/CamelCase
	  MigratingServicesToLXC imported from /tmp/docsdump/MigratingServicesToLXC
	  SuspectDevices imported from /tmp/docsdump/SuspectDevices
	  Esp8266 imported from /tmp/docsdump/Esp8266
	  CloudServerDocs imported from /tmp/docsdump/CloudServerDocs
	  Annie imported from /tmp/docsdump/Annie
	  GoodByeOpenstack imported from /tmp/docsdump/GoodByeOpenstack
	  TicketQuery imported from /tmp/docsdump/TicketQuery
	  OpenWrtE900FirmwareBuild imported from /tmp/docsdump/OpenWrtE900FirmwareBuild
	  FunWithLinuxDisks imported from /tmp/docsdump/FunWithLinuxDisks
	  InterMapTxt imported from /tmp/docsdump/InterMapTxt
	  Ubuntu18.04Notes imported from /tmp/docsdump/Ubuntu18.04Notes
	  ZFSDiskReplacement imported from /tmp/docsdump/ZFSDiskReplacement
	  DiskRecovery imported from /tmp/docsdump/DiskRecovery
	  InterTrac imported from /tmp/docsdump/InterTrac
	  NewTracContainer imported from /tmp/docsdump/NewTracContainer
	  ZFSNightmaresPorted2Linux imported from /tmp/docsdump/ZFSNightmaresPorted2Linux
	  ContainerShipInstallation imported from /tmp/docsdump/ContainerShipInstallation
	  PlatformIO imported from /tmp/docsdump/PlatformIO
	  Nigel imported from /tmp/docsdump/Nigel
	  TitleIndex imported from /tmp/docsdump/TitleIndex
	  LXDContainerWithDockerNotes imported from /tmp/docsdump/LXDContainerWithDockerNotes
	  BleedingEdgeServer imported from /tmp/docsdump/BleedingEdgeServer
	  OpenVPNOnLEDE imported from /tmp/docsdump/OpenVPNOnLEDE
	  InterWiki imported from /tmp/docsdump/InterWiki
	  LXDContainersWithProfile imported from /tmp/docsdump/LXDContainersWithProfile
	  Mullein imported from /tmp/docsdump/Mullein
	  ResliverFailureNotes imported from /tmp/docsdump/ResliverFailureNotes
	  InitialImpressions imported from /tmp/docsdump/InitialImpressions
	  7900NWashburne imported from /tmp/docsdump/7900NWashburne
	root@herbert:~#
	 
Then go to the [/devel devel] site and print the book.