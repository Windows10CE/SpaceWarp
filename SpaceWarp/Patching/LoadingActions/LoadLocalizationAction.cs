﻿using System;
using KSP.Game.Flow;
using SpaceWarp.API;
using SpaceWarp.API.Managers;
using SpaceWarp.API.Mods.JSON;

namespace SpaceWarp.Patching.LoadingActions;

public class LoadLocalizationAction : FlowAction
{
    private string _modID;
    private ModInfo _info;

    public LoadLocalizationAction(string name, string modID, ModInfo info) : base(name)
    {
        _modID = modID;
        _info = info;
    }

    public override void DoAction(Action resolve, Action<string> reject)
    {
        ManagerLocator.TryGet(out SpaceWarpManager spaceWarpManager);

        try
        {
            spaceWarpManager.LoadSingleModLocalization(_modID,_info);
            resolve();
        }
        catch (Exception e)
        {
            reject(e.ToString());
        }
    }
}