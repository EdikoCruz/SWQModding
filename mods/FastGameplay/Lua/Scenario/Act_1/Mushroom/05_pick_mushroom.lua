if SetPlotFlag("mushrooms_05_pick_mushroom") then
	StartCutscene()

	EndCutsceneWithBattle {
		encounter = "mushroomAx1",
		inherit = { actors.boss },
		post_script = "Lua/Scenario/Act_1/Mushroom/05_after_mushroom.lua"
	}
end
