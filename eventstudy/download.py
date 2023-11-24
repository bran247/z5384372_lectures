{"payload":{"allShortcutsEnabled":true,"fileTree":{"event_study":{"items":[{"name":"__init__.py","path":"event_study/__init__.py","contentType":"file"},{"name":"_scratch.py","path":"event_study/_scratch.py","contentType":"file"},{"name":"config.py","path":"event_study/config.py","contentType":"file"},{"name":"download.py","path":"event_study/download.py","contentType":"file"},{"name":"main.py","path":"event_study/main.py","contentType":"file"},{"name":"mk_cars.py","path":"event_study/mk_cars.py","contentType":"file"},{"name":"mk_events.py","path":"event_study/mk_events.py","contentType":"file"},{"name":"mk_rets.py","path":"event_study/mk_rets.py","contentType":"file"},{"name":"test_hypo.py","path":"event_study/test_hypo.py","contentType":"file"}],"totalCount":9},"":{"items":[{"name":"event_study","path":"event_study","contentType":"directory"},{"name":"lectures","path":"lectures","contentType":"directory"},{"name":"webinars","path":"webinars","contentType":"directory"},{"name":"main.py","path":"main.py","contentType":"file"},{"name":"toolkit_config.py","path":"toolkit_config.py","contentType":"file"}],"totalCount":5}},"fileTreeProcessingTime":4.528893,"foldersToFetch":[],"reducedMotionEnabled":"system","repo":{"id":715396917,"defaultBranch":"master","name":"z5416840_lectures","ownerLogin":"lilyyyg","currentUserCanPush":false,"isFork":false,"isEmpty":false,"createdAt":"2023-11-07T14:51:57.000+11:00","ownerAvatar":"https://avatars.githubusercontent.com/u/150103061?v=4","public":true,"private":false,"isOrgOwned":false},"symbolsExpanded":false,"treeExpanded":true,"refInfo":{"name":"master","listCacheKey":"v0:1699329193.0","canEdit":true,"refType":"branch","currentOid":"ed5f9bfb60a8b1fcffcbd5a2550662caf44e8abf"},"path":"event_study/download.py","currentUser":{"id":150109314,"login":"bran247","userEmail":"brandon7gunawan@gmail.com"},"blob":{"rawLines":["\"\"\" download.py","","Utilities to download data from Yahoo Finance","\"\"\"","import yfinance as yf","","from event_study import config as cfg","","# --------------------------------------------------------","#   Function to download recommendations","# --------------------------------------------------------","def yf_rec_to_csv(tic, pth,","                  start=None,","                  end=None):","    \"\"\" Downloads analysts recommendation from Yahoo Finance and saves the","    information in a CSV file","","    Parameters","    ----------","    tic : str","        Ticker","","    pth : str","        Location of the output CSV file","","    start: str, optional","        Download start date string (YYYY-MM-DD)","        If None (the default), start is set to '1900-01-01'","","    end: str, optional","        Download end date string (YYYY-MM-DD)","        If None (the default), end is set to the most current date available","    \"\"\"","    c = yf.Ticker(tic)","    c.history(start=start, end=end).tz_localize(None)","    # Make sure we only relevant dates","    if start is not None and end is not None:","        df = c.recommendations.loc[start:end]","    elif start is not None:","        df = c.recommendations.loc[start:]","    elif end is not None:","        df = c.recommendations.loc[:end]","    else:","        df = c.recommendations","    df.to_csv(pth)"],"stylingDirectives":[[{"start":0,"end":15,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":45,"cssClass":"pl-s"}],[{"start":0,"end":3,"cssClass":"pl-s"}],[{"start":0,"end":6,"cssClass":"pl-k"},{"start":7,"end":15,"cssClass":"pl-s1"},{"start":16,"end":18,"cssClass":"pl-k"},{"start":19,"end":21,"cssClass":"pl-s1"}],[],[{"start":0,"end":4,"cssClass":"pl-k"},{"start":5,"end":16,"cssClass":"pl-s1"},{"start":17,"end":23,"cssClass":"pl-k"},{"start":24,"end":30,"cssClass":"pl-s1"},{"start":31,"end":33,"cssClass":"pl-k"},{"start":34,"end":37,"cssClass":"pl-s1"}],[],[{"start":0,"end":58,"cssClass":"pl-c"}],[{"start":0,"end":40,"cssClass":"pl-c"}],[{"start":0,"end":58,"cssClass":"pl-c"}],[{"start":0,"end":3,"cssClass":"pl-k"},{"start":4,"end":17,"cssClass":"pl-en"},{"start":18,"end":21,"cssClass":"pl-s1"},{"start":23,"end":26,"cssClass":"pl-s1"}],[{"start":18,"end":23,"cssClass":"pl-s1"},{"start":23,"end":24,"cssClass":"pl-c1"},{"start":24,"end":28,"cssClass":"pl-c1"}],[{"start":18,"end":21,"cssClass":"pl-s1"},{"start":21,"end":22,"cssClass":"pl-c1"},{"start":22,"end":26,"cssClass":"pl-c1"}],[{"start":4,"end":74,"cssClass":"pl-s"}],[{"start":0,"end":29,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":13,"cssClass":"pl-s"}],[{"start":0,"end":14,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":13,"cssClass":"pl-s"}],[{"start":0,"end":39,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":24,"cssClass":"pl-s"}],[{"start":0,"end":47,"cssClass":"pl-s"}],[{"start":0,"end":59,"cssClass":"pl-s"}],[{"start":0,"end":0,"cssClass":"pl-s"}],[{"start":0,"end":22,"cssClass":"pl-s"}],[{"start":0,"end":45,"cssClass":"pl-s"}],[{"start":0,"end":76,"cssClass":"pl-s"}],[{"start":0,"end":7,"cssClass":"pl-s"}],[{"start":4,"end":5,"cssClass":"pl-s1"},{"start":6,"end":7,"cssClass":"pl-c1"},{"start":8,"end":10,"cssClass":"pl-s1"},{"start":11,"end":17,"cssClass":"pl-v"},{"start":18,"end":21,"cssClass":"pl-s1"}],[{"start":4,"end":5,"cssClass":"pl-s1"},{"start":6,"end":13,"cssClass":"pl-en"},{"start":14,"end":19,"cssClass":"pl-s1"},{"start":19,"end":20,"cssClass":"pl-c1"},{"start":20,"end":25,"cssClass":"pl-s1"},{"start":27,"end":30,"cssClass":"pl-s1"},{"start":30,"end":31,"cssClass":"pl-c1"},{"start":31,"end":34,"cssClass":"pl-s1"},{"start":36,"end":47,"cssClass":"pl-en"},{"start":48,"end":52,"cssClass":"pl-c1"}],[{"start":4,"end":38,"cssClass":"pl-c"}],[{"start":4,"end":6,"cssClass":"pl-k"},{"start":7,"end":12,"cssClass":"pl-s1"},{"start":13,"end":15,"cssClass":"pl-c1"},{"start":16,"end":19,"cssClass":"pl-c1"},{"start":20,"end":24,"cssClass":"pl-c1"},{"start":25,"end":28,"cssClass":"pl-c1"},{"start":29,"end":32,"cssClass":"pl-s1"},{"start":33,"end":35,"cssClass":"pl-c1"},{"start":36,"end":39,"cssClass":"pl-c1"},{"start":40,"end":44,"cssClass":"pl-c1"}],[{"start":8,"end":10,"cssClass":"pl-s1"},{"start":11,"end":12,"cssClass":"pl-c1"},{"start":13,"end":14,"cssClass":"pl-s1"},{"start":15,"end":30,"cssClass":"pl-s1"},{"start":31,"end":34,"cssClass":"pl-s1"},{"start":35,"end":40,"cssClass":"pl-s1"},{"start":41,"end":44,"cssClass":"pl-s1"}],[{"start":4,"end":8,"cssClass":"pl-k"},{"start":9,"end":14,"cssClass":"pl-s1"},{"start":15,"end":17,"cssClass":"pl-c1"},{"start":18,"end":21,"cssClass":"pl-c1"},{"start":22,"end":26,"cssClass":"pl-c1"}],[{"start":8,"end":10,"cssClass":"pl-s1"},{"start":11,"end":12,"cssClass":"pl-c1"},{"start":13,"end":14,"cssClass":"pl-s1"},{"start":15,"end":30,"cssClass":"pl-s1"},{"start":31,"end":34,"cssClass":"pl-s1"},{"start":35,"end":40,"cssClass":"pl-s1"}],[{"start":4,"end":8,"cssClass":"pl-k"},{"start":9,"end":12,"cssClass":"pl-s1"},{"start":13,"end":15,"cssClass":"pl-c1"},{"start":16,"end":19,"cssClass":"pl-c1"},{"start":20,"end":24,"cssClass":"pl-c1"}],[{"start":8,"end":10,"cssClass":"pl-s1"},{"start":11,"end":12,"cssClass":"pl-c1"},{"start":13,"end":14,"cssClass":"pl-s1"},{"start":15,"end":30,"cssClass":"pl-s1"},{"start":31,"end":34,"cssClass":"pl-s1"},{"start":36,"end":39,"cssClass":"pl-s1"}],[{"start":4,"end":8,"cssClass":"pl-k"}],[{"start":8,"end":10,"cssClass":"pl-s1"},{"start":11,"end":12,"cssClass":"pl-c1"},{"start":13,"end":14,"cssClass":"pl-s1"},{"start":15,"end":30,"cssClass":"pl-s1"}],[{"start":4,"end":6,"cssClass":"pl-s1"},{"start":7,"end":13,"cssClass":"pl-en"},{"start":14,"end":17,"cssClass":"pl-s1"}],[]],"csv":null,"csvError":null,"dependabotInfo":{"showConfigurationBanner":false,"configFilePath":null,"networkDependabotPath":"/lilyyyg/z5416840_lectures/network/updates","dismissConfigurationNoticePath":"/settings/dismiss-notice/dependabot_configuration_notice","configurationNoticeDismissed":false,"repoAlertsPath":"/lilyyyg/z5416840_lectures/security/dependabot","repoSecurityAndAnalysisPath":"/lilyyyg/z5416840_lectures/settings/security_analysis","repoOwnerIsOrg":false,"currentUserCanAdminRepo":false},"displayName":"download.py","displayUrl":"https://github.com/lilyyyg/z5416840_lectures/blob/master/event_study/download.py?raw=true","headerInfo":{"blobSize":"1.26 KB","deleteInfo":{"deleteTooltip":"Fork this repository and delete the file"},"editInfo":{"editTooltip":"Fork this repository and edit the file"},"ghDesktopPath":"https://desktop.github.com","gitLfsPath":null,"onBranch":true,"shortPath":"51e7531","siteNavLoginPath":"/login?return_to=https%3A%2F%2Fgithub.com%2Flilyyyg%2Fz5416840_lectures%2Fblob%2Fmaster%2Fevent_study%2Fdownload.py","isCSV":false,"isRichtext":false,"toc":null,"lineInfo":{"truncatedLoc":"46","truncatedSloc":"38"},"mode":"file"},"image":false,"isCodeownersFile":null,"isPlain":false,"isValidLegacyIssueTemplate":false,"issueTemplateHelpUrl":"https://docs.github.com/articles/about-issue-and-pull-request-templates","issueTemplate":null,"discussionTemplate":null,"language":"Python","languageID":303,"large":false,"loggedIn":true,"newDiscussionPath":"/lilyyyg/z5416840_lectures/discussions/new","newIssuePath":"/lilyyyg/z5416840_lectures/issues/new","planSupportInfo":{"repoIsFork":null,"repoOwnedByCurrentUser":null,"requestFullPath":"/lilyyyg/z5416840_lectures/blob/master/event_study/download.py","showFreeOrgGatedFeatureMessage":null,"showPlanSupportBanner":null,"upgradeDataAttributes":null,"upgradePath":null},"publishBannersInfo":{"dismissActionNoticePath":"/settings/dismiss-notice/publish_action_from_dockerfile","dismissStackNoticePath":"/settings/dismiss-notice/publish_stack_from_file","releasePath":"/lilyyyg/z5416840_lectures/releases/new?marketplace=true","showPublishActionBanner":false,"showPublishStackBanner":false},"rawBlobUrl":"https://github.com/lilyyyg/z5416840_lectures/raw/master/event_study/download.py","renderImageOrRaw":false,"richText":null,"renderedFileInfo":null,"shortPath":null,"tabSize":8,"topBannersInfo":{"overridingGlobalFundingFile":false,"globalPreferredFundingPath":null,"repoOwner":"lilyyyg","repoName":"z5416840_lectures","showInvalidCitationWarning":false,"citationHelpUrl":"https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/about-citation-files","showDependabotConfigurationBanner":false,"actionsOnboardingTip":null},"truncated":false,"viewable":true,"workflowRedirectUrl":null,"symbols":{"timedOut":false,"notAnalyzed":false,"symbols":[{"name":"yf_rec_to_csv","kind":"function","identStart":292,"identEnd":305,"extentStart":288,"extentEnd":1289,"fullyQualifiedName":"yf_rec_to_csv","identUtf16":{"start":{"lineNumber":11,"utf16Col":4},"end":{"lineNumber":11,"utf16Col":17}},"extentUtf16":{"start":{"lineNumber":11,"utf16Col":0},"end":{"lineNumber":44,"utf16Col":18}}}]}},"copilotInfo":{"documentationUrl":"https://docs.github.com/copilot/overview-of-github-copilot/about-github-copilot-for-individuals","notices":{"codeViewPopover":{"dismissed":false,"dismissPath":"/settings/dismiss-notice/code_view_copilot_popover"}},"userAccess":{"accessAllowed":false,"hasSubscriptionEnded":false,"orgHasCFBAccess":false,"userHasCFIAccess":false,"userHasOrgs":false,"userIsOrgAdmin":false,"userIsOrgMember":false,"business":null,"featureRequestInfo":null}},"copilotAccessAllowed":false,"csrf_tokens":{"/lilyyyg/z5416840_lectures/branches":{"post":"AUtHcjXonZUYrSU3xqTj3Avg_F7yv6HyHau00fZyu_it0xgN-WtWi_z2WebifbBk0Vm1KeYFiehF0R-9TrWbwQ"},"/repos/preferences":{"post":"CUUepd0evvCYIlvF4xxtIRVx0Hey3amSPIK3RIJOnyxFfDCnj2BWZStKSMhzsNJHqxo88Pd6p4rhM2GW0GZZwA"}}},"title":"z5416840_lectures/event_study/download.py at master · lilyyyg/z5416840_lectures"}