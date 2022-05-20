if SetPlotFlag("mushrooms_02_coglins") then
	StartCutscene()

	EndCutsceneWithBattle {
		encounter="goblinAx2",
		inherit={actors.coglin_right, actors.coglin_left},
		post_conversation="ch1_defeated_coglin",
	}
end
