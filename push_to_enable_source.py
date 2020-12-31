import obspython as obs
import ntpath

hotkey_id_array = []
hotkey_names_by_id = {}

source_to_toggle = None
invert_bool = False


def script_load(settings):
    print("--- " + ntpath.basename(__file__) + " loaded ---")

    # create Hotkey in global OBS Settings
    hotkey_id_array.append(obs.obs_hotkey_register_frontend("SHORTCUT 1", "Push to Enable Source Key", hotkey_1_callback))
    hotkey_names_by_id[hotkey_id_array[len(hotkey_id_array)-1]] = "SHORTCUT 1"

    # load hotkeys from script save file
    for hotkey_id in hotkey_id_array:
        # get the hotkeys data_array from the script settings (was saved under the hotkeys name)  !! find way to use obs_hotkey_get_name instead of tracking the name manually
        hotkey_data_array_from_settings = obs.obs_data_get_array(settings, hotkey_names_by_id[hotkey_id])
        # load the saved hotkeys data_array to the new created hotkey associated with the "hotkey_id"
        obs.obs_hotkey_load(hotkey_id, hotkey_data_array_from_settings)

        obs.obs_data_array_release(hotkey_data_array_from_settings)


def script_save(settings):
    # save hotkeys in script properties
    for hotkey_id in hotkey_id_array:
        # save each hotkeys data_array into script settings by the hotkeys name  !! find way to use obs_hotkey_get_name instead of tracking the name manually
        obs.obs_data_set_array(settings, hotkey_names_by_id[hotkey_id], obs.obs_hotkey_save(hotkey_id))


def script_update(settings):
    # print("script update")
    global source_to_toggle, invert_bool

    source_to_toggle = obs.obs_data_get_string(settings, "source_select_list")
    # print("source_to_toggle", source_to_toggle)
    if source_to_toggle == "":
        source_to_toggle = None

    invert_bool = obs.obs_data_get_bool(settings, "invert_bool")
    enable_source(invert_bool)


def script_properties():
    # print("script props")
    props = obs.obs_properties_create()

    drop_list = obs.obs_properties_add_list(props, "source_select_list", "Source to toggle", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_list_add_string(drop_list, "", "")

    sources = obs.obs_enum_sources()
    for src in sources:
        obs.obs_property_list_add_string(drop_list, obs.obs_source_get_name(src), obs.obs_source_get_name(src))
    obs.source_list_release(sources)

    obs.obs_properties_add_bool(props, "invert_bool", "Invert behaviour")

    return props


def hotkey_1_callback(is_pressed):
    # print(f"-- Shortcut 1 ; Data: {data}")
    if is_pressed:
        enable_source(not invert_bool)
    else:
        enable_source(invert_bool)


def enable_source(boolean):
    scene_sources = obs.obs_frontend_get_scenes()
    for scn_src in scene_sources:
        scn = obs.obs_scene_from_source(scn_src)
        scn_items = obs.obs_scene_enum_items(scn)
        for itm in scn_items:
            itm_src = obs.obs_sceneitem_get_source(itm)
            if obs.obs_source_get_name(itm_src) == source_to_toggle:
                obs.obs_sceneitem_set_visible(itm, boolean)

        obs.sceneitem_list_release(scn_items)
    obs.source_list_release(scene_sources)


