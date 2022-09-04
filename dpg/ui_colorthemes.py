class colorTheme:
    def __init__(self):
        pass

class midnight_spark(colorTheme):
    name = "Midnight Spark"
    tag = "midnight_spark"
    white = "#ffffff"
    black = "#000000"
    window_background_color = "#26385a"
    node_grid_background_color = "#0a1c3d"
    node_grid_lines_color = "#112c5c"
    node_grid_alt_lines_color = "#234f9e"
    list_background_color = "#234f9e"
    window_text_color = "#8bdfc7"
    button_alt_color = "#93edd3"
    button_alt_text_color = "#30403b"
    
    node_selected_color = "#FF729F"
    node_socket_trigger_color = "#00EE88"
    node_socket_file_color = "#FF57A2"
    node_socket_object_color = "#FF7700"
    node_socket_number_color = "#009EFF"
    node_socket_text_color = "#FFE099"
    node_socket_list_color = "#968080"
    node_socket_boolean_color = "#2f3aa3"
    node_wire_error_color = "#EF3054"
    
    node_title_color = "#8bdfc7"
    node_title_background_color = "#0f3c91"
    node_background_color = "#144db8"
    node_text_color = "#8bdfc7"
    node_wire_color = "#f6faa7"
    
    unit_editor_rule_0 = "#E1E1B4"
    unit_editor_rule_1 = "#A5A960"
    unit_editor_rule_2 = "#377560"
    unit_editor_rule_3 = "#325066"
    unit_editor_rule_4 = "#306173"
    unit_editor_rule_5 = "#37715F"
    
    node_outliner_label_0 = "#AE462B"
    node_outliner_label_1 = "#534E70"
    node_outliner_label_2 = "#DDA448"
    node_outliner_label_3 = "#E2C044"
    
    unit_editor_slider_color_0 = "#f6faa7"
    unit_editor_slider_color_1 = "#EF3054"

    level_editor = ["level_editor", window_background_color,list_background_color,
                    window_text_color,
                    button_alt_color,button_alt_text_color]

    node_grid = ["node_grid",node_grid_background_color, node_grid_lines_color,
                 node_grid_alt_lines_color, node_selected_color, node_title_color,
                 node_title_background_color, node_background_color,
                 node_text_color, node_wire_color, node_socket_trigger_color,
                 node_socket_file_color, node_socket_object_color,
                 node_socket_number_color, node_socket_text_color, node_socket_list_color,
                 node_socket_boolean_color, node_wire_error_color,
                 node_outliner_label_0,node_outliner_label_1,node_outliner_label_2,
                 node_outliner_label_3]
    
    unit_editor = ["unit_editor", unit_editor_rule_0, unit_editor_rule_1, unit_editor_rule_2,
                   unit_editor_rule_3, unit_editor_rule_4, unit_editor_rule_5,
                   unit_editor_slider_color_0, unit_editor_slider_color_1]

    level_editor_labels = ["level_editor", "window_background_color",
                           "list_background_color",
                    "window_text_color",
                    "button_alt_color","button_alt_text_color"]

    node_grid_labels = ["node_grid","node_grid_background_color",
                        "node_grid_lines_color",
                 "node_grid_alt_lines_color", "node_selected_color","node_title_color",
                 "node_title_background_color", "node_background_color",
                 "node_text_color", "node_wire_color", "node_socket_trigger_color",
                 "node_socket_file_color", "node_socket_object_color",
                 "node_socket_number_color", "node_socket_text_color","node_socket_list_color",
                 "node_socket_boolean_color", "node_wire_error_color",
                        "node_outliner_label_0","node_outliner_label_1","node_outliner_label_2",
                        "node_outliner_label_3"]
    
    unit_editor_labels = ["unit_editor", "unit_editor_rule_0", "unit_editor_rule_1", "unit_editor_rule_2",
                   "unit_editor_rule_3", "unit_editor_rule_4", "unit_editor_rule_5",
                          "unit_editor_slider_color_0", "unit_editor_slider_color_1"]

    groups = [level_editor, node_grid, unit_editor]

class charcoal(colorTheme):
    name = "Charcoal"
    tag = "charcoal"
    white = "#ffffff"
    black = "#000000"
    window_background_color = "#222222"
    list_background_color = "#545454"
    button_alt_color = "#e6e6e6"
    button_alt_text_color = "#232323"
    node_grid_background_color = "#363636"
    node_selected_color = "#ffa754"
    window_text_color = "#c4c4c4"
    node_grid_alt_lines_color = "#292929"
    node_grid_lines_color = "#2f2f2f"
    node_title_color = "#ffffff"
    node_title_background_color = "#494949"
    node_background_color = "#323232"
    node_text_color = "#d0d0d0"
    node_wire_color = "#ACACAC"
    node_socket_trigger_color = "#00FF77"
    node_socket_file_color = "#FF57A2"
    node_socket_object_color = "#FF7700"
    node_socket_number_color = "#009EFF"
    node_socket_text_color = "#FFE099"
    node_socket_list_color = "#808080"
    node_socket_boolean_color = "#2f3aa3"
    node_wire_error_color = "#FF3333"
    node_outliner_label_0 = "#D95F80"
    node_outliner_label_1 = "#5a82d1"
    node_outliner_label_2 = "#F27B50"
    node_outliner_label_3 = "#D7D9D0"
    
    unit_editor_rule_0 = "#f5cc7f"
    unit_editor_rule_1 = "#edceb7"
    unit_editor_rule_2 = "#F2AE30"
    unit_editor_rule_3 = "#d97904"
    unit_editor_rule_4 = "#a35e07"
    unit_editor_rule_5 = "#262523"
    
    unit_editor_slider_color_0 = "#D95F80"
    unit_editor_slider_color_1 = "#5a82d1"

    level_editor = ["level_editor", window_background_color,list_background_color,
                    window_text_color,
                    button_alt_color,button_alt_text_color]

    node_grid = ["node_grid",node_grid_background_color, node_grid_lines_color,
                 node_grid_alt_lines_color, node_selected_color, node_title_color,
                 node_title_background_color, node_background_color,
                 node_text_color, node_wire_color, node_socket_trigger_color,
                 node_socket_file_color, node_socket_object_color,
                 node_socket_number_color, node_socket_text_color, node_socket_list_color,
                 node_socket_boolean_color, node_wire_error_color,
                 node_outliner_label_0,node_outliner_label_1,node_outliner_label_2,
                 node_outliner_label_3]
    
    unit_editor = ["unit_editor", unit_editor_rule_0, unit_editor_rule_1, unit_editor_rule_2,
                   unit_editor_rule_3, unit_editor_rule_4, unit_editor_rule_5,
                   unit_editor_slider_color_0, unit_editor_slider_color_1]

    level_editor_labels = ["level_editor", "window_background_color",
                           "list_background_color",
                    "window_text_color",
                    "button_alt_color","button_alt_text_color"]

    node_grid_labels = ["node_grid","node_grid_background_color",
                        "node_grid_lines_color",
                 "node_grid_alt_lines_color", "node_selected_color","node_title_color",
                 "node_title_background_color", "node_background_color",
                 "node_text_color", "node_wire_color", "node_socket_trigger_color",
                 "node_socket_file_color", "node_socket_object_color",
                 "node_socket_number_color", "node_socket_text_color","node_socket_list_color",
                 "node_socket_boolean_color", "node_wire_error_color",
                        "node_outliner_label_0","node_outliner_label_1","node_outliner_label_2",
                        "node_outliner_label_3"]
    
    unit_editor_labels = ["unit_editor", "unit_editor_rule_0", "unit_editor_rule_1", "unit_editor_rule_2",
                   "unit_editor_rule_3", "unit_editor_rule_4", "unit_editor_rule_5",
                          "unit_editor_slider_color_0", "unit_editor_slider_color_1"]

    groups = [level_editor, node_grid, unit_editor]
    
class ocean_waves(colorTheme):
    name = "Ocean Waves"
    tag = "ocean_waves"
    white = "#ffffff"
    black = "#000000"
    window_background_color = "#568EBF"
    button_alt_color = "#D2F2F9"
    button_alt_text_color = "#7AA6CD"
    list_background_color = "#394159"
    window_text_color = "#DCEEF2"
    node_grid_lines_color = "#7AA6CD"
    node_grid_alt_lines_color = "#5c8fbd"
    node_grid_background_color = "#6b9dc9"
    node_selected_color = "#78ffe8"
    node_title_color = "#ffffff"
    node_title_background_color = "#568EBF"
    node_background_color = "#394159"
    node_text_color = "#7AA6CD"
    node_wire_color = "#394159"
    node_socket_trigger_color = "#00FF77"
    node_socket_file_color = "#FF57A2"
    node_socket_object_color = "#FF7700"
    node_socket_number_color = "#009EFF"
    node_socket_text_color = "#FFE099"
    node_socket_list_color = "#FFFFFF"
    node_socket_boolean_color = "#2f3aa3"
    node_wire_error_color = "#C02D0C"
    node_outliner_label_0 = "#F29472"
    node_outliner_label_1 = "#5FE3E3"
    node_outliner_label_2 = "#009EFF"
    node_outliner_label_3 = "#F2D49B"
    
    unit_editor_rule_0 = "#D9D4D2"
    unit_editor_rule_1 = "#9BBFB2"
    unit_editor_rule_2 = "#60A69F"
    unit_editor_rule_3 = "#4D6873"
    unit_editor_rule_4 = "#1B4859"
    unit_editor_rule_5 = "#0a1e26"
    
    unit_editor_slider_color_0 = "#F29472"
    unit_editor_slider_color_1 = "#5FE3E3"

    level_editor = ["level_editor", window_background_color,list_background_color,
                    window_text_color,
                    button_alt_color,button_alt_text_color]

    node_grid = ["node_grid",node_grid_background_color, node_grid_lines_color,
                 node_grid_alt_lines_color, node_selected_color, node_title_color,
                 node_title_background_color, node_background_color,
                 node_text_color, node_wire_color, node_socket_trigger_color,
                 node_socket_file_color, node_socket_object_color,
                 node_socket_number_color, node_socket_text_color, node_socket_list_color,
                 node_socket_boolean_color, node_wire_error_color,
                 node_outliner_label_0,node_outliner_label_1,node_outliner_label_2,
                 node_outliner_label_3]
    
    unit_editor = ["unit_editor", unit_editor_rule_0, unit_editor_rule_1, unit_editor_rule_2,
                   unit_editor_rule_3, unit_editor_rule_4, unit_editor_rule_5,
                   unit_editor_slider_color_0, unit_editor_slider_color_1]

    level_editor_labels = ["level_editor", "window_background_color",
                           "list_background_color",
                    "window_text_color",
                    "button_alt_color","button_alt_text_color"]

    node_grid_labels = ["node_grid","node_grid_background_color",
                        "node_grid_lines_color",
                 "node_grid_alt_lines_color", "node_selected_color","node_title_color",
                 "node_title_background_color", "node_background_color",
                 "node_text_color", "node_wire_color", "node_socket_trigger_color",
                 "node_socket_file_color", "node_socket_object_color",
                 "node_socket_number_color", "node_socket_text_color","node_socket_list_color",
                 "node_socket_boolean_color", "node_wire_error_color",
                        "node_outliner_label_0","node_outliner_label_1","node_outliner_label_2",
                        "node_outliner_label_3"]
    
    unit_editor_labels = ["unit_editor", "unit_editor_rule_0", "unit_editor_rule_1", "unit_editor_rule_2",
                   "unit_editor_rule_3", "unit_editor_rule_4", "unit_editor_rule_5",
                          "unit_editor_slider_color_0", "unit_editor_slider_color_1"]

    groups = [level_editor, node_grid, unit_editor]
    
class chocolate(colorTheme):
    name = "Chocolate"
    tag = "chocolate"
    white = "#ffffff"
    black = "#000000"
    window_background_color = "#5c2e24"
    list_background_color = "#733A2D"
    window_text_color = "#DB8C50"
    workspace_background_color = "#994E33"
    
    button_alt_color = "#F9C27E"
    button_alt_text_color = "#512C2A"

    node_grid_lines_color = "#b86748"
    node_grid_alt_lines_color = "#914e34"
    node_grid_background_color = "#A65638"
    node_selected_color = "#F9C27E"
    node_title_color = "#DB8C50"
    node_title_background_color = "#59302C"
    node_background_color = "#512C2A"
    node_text_color = "#FBF4EB"
    node_wire_color = "#DB8C50"
    
    node_socket_trigger_color = "#00EE88"
    node_socket_file_color = "#FF57A2"
    node_socket_object_color = "#FF7700"
    node_socket_number_color = "#009EFF"
    node_socket_text_color = "#FFE099"
    node_socket_list_color = "#968080"
    node_socket_boolean_color = "#2f3aa3"

    node_wire_error_color = "#7B2523"
    
    node_outliner_label_0 = "#EF965E"
    node_outliner_label_1 = "#F9C27E"
    node_outliner_label_2 = "#C3BCAC"
    node_outliner_label_3 = "#5FE3E3"

    unit_editor_rule_0 = "#A1BBBB"
    unit_editor_rule_1 = "#DBD4C5"
    unit_editor_rule_2 = "#C95341"
    unit_editor_rule_3 = "#C0414A"
    unit_editor_rule_4 = "#655B59"
    unit_editor_rule_5 = "#943F5F"
    
    unit_editor_slider_color_0 = "#EF965E"
    unit_editor_slider_color_1 = "#5fe3e3"

    level_editor = ["level_editor", window_background_color,list_background_color,
                    window_text_color,
                    button_alt_color,button_alt_text_color]

    node_grid = ["node_grid",node_grid_background_color, node_grid_lines_color,
                 node_grid_alt_lines_color, node_selected_color, node_title_color,
                 node_title_background_color, node_background_color,
                 node_text_color, node_wire_color, node_socket_trigger_color,
                 node_socket_file_color, node_socket_object_color,
                 node_socket_number_color, node_socket_text_color, node_socket_list_color,
                 node_socket_boolean_color, node_wire_error_color,
                 node_outliner_label_0,node_outliner_label_1,node_outliner_label_2,
                 node_outliner_label_3]
    
    unit_editor = ["unit_editor", unit_editor_rule_0, unit_editor_rule_1, unit_editor_rule_2,
                   unit_editor_rule_3, unit_editor_rule_4, unit_editor_rule_5,
                   unit_editor_slider_color_0, unit_editor_slider_color_1]

    level_editor_labels = ["level_editor", "window_background_color",
                           "list_background_color",
                    "window_text_color",
                    "button_alt_color","button_alt_text_color"]

    node_grid_labels = ["node_grid","node_grid_background_color",
                        "node_grid_lines_color",
                 "node_grid_alt_lines_color", "node_selected_color","node_title_color",
                 "node_title_background_color", "node_background_color",
                 "node_text_color", "node_wire_color", "node_socket_trigger_color",
                 "node_socket_file_color", "node_socket_object_color",
                 "node_socket_number_color", "node_socket_text_color","node_socket_list_color",
                 "node_socket_boolean_color", "node_wire_error_color",
                        "node_outliner_label_0","node_outliner_label_1","node_outliner_label_2",
                        "node_outliner_label_3"]
    
    unit_editor_labels = ["unit_editor", "unit_editor_rule_0", "unit_editor_rule_1", "unit_editor_rule_2",
                   "unit_editor_rule_3", "unit_editor_rule_4", "unit_editor_rule_5",
                          "unit_editor_slider_color_0", "unit_editor_slider_color_1"]

    groups = [level_editor, node_grid, unit_editor]

class chili_pepper(colorTheme):
    name = "Chili Pepper"
    tag = "chili_pepper"
    white = "#ffffff"
    black = "#000000"
    window_background_color = "#C0414A"
    list_background_color = "#f2eae4"
    window_text_color = "#262523"
    
    button_alt_color = "#000000"
    button_alt_text_color = "#FFFFFF"

    node_grid_lines_color = "#F9ECD6"
    node_grid_alt_lines_color = "#e3d0b1"
    node_grid_background_color = "#E8DBC5"
    node_selected_color = "#434F5D"
    node_title_color = "#333333"
    node_title_background_color = "#FFE0B5"
    node_background_color = "#fae7cd"
    node_text_color = "#333333"
    node_wire_color = "#632533"
    
    node_socket_trigger_color = "#00EE88"
    node_socket_file_color = "#FF57A2"
    node_socket_object_color = "#FF7700"
    node_socket_number_color = "#009EFF"
    node_socket_text_color = "#FFE099"
    node_socket_list_color = "#968080"
    node_socket_boolean_color = "#2f3aa3"
    node_wire_error_color = "#b8304e"
    
    node_outliner_label_0 = "#A59A6F"
    node_outliner_label_1 = "#D48D8D"
    node_outliner_label_2 = "#C5B99B"
    node_outliner_label_3 = "#699987"
    
    unit_editor_rule_0 = "#8C8C87"
    unit_editor_rule_1 = "#F1D8C8"
    unit_editor_rule_2 = "#3F1019"
    unit_editor_rule_3 = "#8C8C87"
    unit_editor_rule_4 = "#595952"
    unit_editor_rule_5 = "#262621"
    
    unit_editor_slider_color_0 = "#F1D8C8"
    unit_editor_slider_color_1 = "#A62C3D"

    level_editor = ["level_editor", window_background_color,list_background_color,
                    window_text_color,
                    button_alt_color,button_alt_text_color]

    node_grid = ["node_grid",node_grid_background_color, node_grid_lines_color,
                 node_grid_alt_lines_color, node_selected_color, node_title_color,
                 node_title_background_color, node_background_color,
                 node_text_color, node_wire_color, node_socket_trigger_color,
                 node_socket_file_color, node_socket_object_color,
                 node_socket_number_color, node_socket_text_color, node_socket_list_color,
                 node_socket_boolean_color, node_wire_error_color,
                 node_outliner_label_0,node_outliner_label_1,node_outliner_label_2,
                 node_outliner_label_3]
    
    unit_editor = ["unit_editor", unit_editor_rule_0, unit_editor_rule_1, unit_editor_rule_2,
                   unit_editor_rule_3, unit_editor_rule_4, unit_editor_rule_5,
                   unit_editor_slider_color_0, unit_editor_slider_color_1]

    level_editor_labels = ["level_editor", "window_background_color",
                           "list_background_color",
                    "window_text_color",
                    "button_alt_color","button_alt_text_color"]

    node_grid_labels = ["node_grid","node_grid_background_color",
                        "node_grid_lines_color",
                 "node_grid_alt_lines_color", "node_selected_color","node_title_color",
                 "node_title_background_color", "node_background_color",
                 "node_text_color", "node_wire_color", "node_socket_trigger_color",
                 "node_socket_file_color", "node_socket_object_color",
                 "node_socket_number_color", "node_socket_text_color","node_socket_list_color",
                 "node_socket_boolean_color", "node_wire_error_color",
                        "node_outliner_label_0","node_outliner_label_1","node_outliner_label_2",
                        "node_outliner_label_3"]
    
    unit_editor_labels = ["unit_editor", "unit_editor_rule_0", "unit_editor_rule_1", "unit_editor_rule_2",
                   "unit_editor_rule_3", "unit_editor_rule_4", "unit_editor_rule_5",
                          "unit_editor_slider_color_0", "unit_editor_slider_color_1"]

    groups = [level_editor, node_grid, unit_editor]

class turnroot(colorTheme):
    name = "Turnroot"
    tag = "turnroot"
    white = "#ffffff"
    black = "#000000"
    window_background_color = "#5b6067"
    node_grid_background_color = "#5b6067"
    node_grid_lines_color = "#6b7077"
    node_grid_alt_lines_color = "#4b5057"
    list_background_color = "#43a188"
    window_text_color = "#f8f5Da"
    button_alt_color = "#f8f5Da"
    button_alt_text_color = "#5b6067"
    
    node_selected_color = "#99d3ae"
    node_socket_trigger_color = "#00EE88"
    node_socket_file_color = "#FF57A2"
    node_socket_object_color = "#FF7700"
    node_socket_number_color = "#009EFF"
    node_socket_text_color = "#FFE099"
    node_socket_list_color = "#968080"
    node_socket_boolean_color = "#2f3aa3"
    node_wire_error_color = "#EF3054"
    
    node_title_color = "#f8f5da"
    node_title_background_color = "#79a38e"
    node_background_color = "#43a188"
    node_text_color = "#f8f5da"
    node_wire_color = "#f8f5da"
    
    unit_editor_rule_0 = "#E1E1B4"
    unit_editor_rule_1 = "#99d3ae"
    unit_editor_rule_2 = "#377560"
    unit_editor_rule_3 = "#325066"
    unit_editor_rule_4 = "#306173"
    unit_editor_rule_5 = "#37715F"
    
    node_outliner_label_0 = "#eef797"
    node_outliner_label_1 = "#c2ed7b"
    node_outliner_label_2 = "#54d66c"
    node_outliner_label_3 = "#29c287"
    
    unit_editor_slider_color_0 = "#78f0bc"
    unit_editor_slider_color_1 = "#eef7c1"

    level_editor = ["level_editor", window_background_color,list_background_color,
                    window_text_color,
                    button_alt_color,button_alt_text_color]

    node_grid = ["node_grid",node_grid_background_color, node_grid_lines_color,
                 node_grid_alt_lines_color, node_selected_color, node_title_color,
                 node_title_background_color, node_background_color,
                 node_text_color, node_wire_color, node_socket_trigger_color,
                 node_socket_file_color, node_socket_object_color,
                 node_socket_number_color, node_socket_text_color, node_socket_list_color,
                 node_socket_boolean_color, node_wire_error_color,
                 node_outliner_label_0,node_outliner_label_1,node_outliner_label_2,
                 node_outliner_label_3]
    
    unit_editor = ["unit_editor", unit_editor_rule_0, unit_editor_rule_1, unit_editor_rule_2,
                   unit_editor_rule_3, unit_editor_rule_4, unit_editor_rule_5,
                   unit_editor_slider_color_0, unit_editor_slider_color_1]

    level_editor_labels = ["level_editor", "window_background_color",
                           "list_background_color",
                    "window_text_color",
                    "button_alt_color","button_alt_text_color"]

    node_grid_labels = ["node_grid","node_grid_background_color",
                        "node_grid_lines_color",
                 "node_grid_alt_lines_color", "node_selected_color","node_title_color",
                 "node_title_background_color", "node_background_color",
                 "node_text_color", "node_wire_color", "node_socket_trigger_color",
                 "node_socket_file_color", "node_socket_object_color",
                 "node_socket_number_color", "node_socket_text_color","node_socket_list_color",
                 "node_socket_boolean_color", "node_wire_error_color",
                        "node_outliner_label_0","node_outliner_label_1","node_outliner_label_2",
                        "node_outliner_label_3"]
    
    unit_editor_labels = ["unit_editor", "unit_editor_rule_0", "unit_editor_rule_1", "unit_editor_rule_2",
                   "unit_editor_rule_3", "unit_editor_rule_4", "unit_editor_rule_5",
                          "unit_editor_slider_color_0", "unit_editor_slider_color_1"]

    groups = [level_editor, node_grid, unit_editor]

class custom(colorTheme):
    name = "Custom"
    tag = "custom"
    white = "#ffffff"
    black = "#000000"
    window_background_color = "#000000"
    button_alt_color = "#000000"
    button_alt_text_color = "#FFFFFF"
    list_background_color = "#000000"
    window_text_color = "#FFFFFF"
    node_grid_lines_color = "#000000"
    node_grid_alt_lines_color = "#000000"
    node_grid_background_color = "#000000"
    node_selected_color = "#000000"
    node_title_color = "#000000"
    node_title_background_color = "#000000"
    node_background_color = "#000000"
    node_text_color = "#FFFFFF"
    node_wire_color = "#000000"
    node_socket_trigger_color = "#000000"
    node_socket_file_color = "#000000"
    node_socket_object_color = "#000000"
    node_socket_number_color = "#000000"
    node_socket_text_color = "#000000"
    node_socket_list_color = "#000000"
    node_socket_boolean_color = "#000000"
    node_wire_error_color = "#000000"
    node_outliner_label_0 = ""
    node_outliner_label_1 = ""
    node_outliner_label_2 = ""
    node_outliner_label_3 = ""

    unit_editor_rule_0 = "#FFFFFF"
    unit_editor_rule_1 = "#FFFFFF"
    unit_editor_rule_2 = "#000000"
    unit_editor_rule_3 = "#000000"
    unit_editor_rule_4 = "#000000"
    unit_editor_rule_5 = "#000000"

    level_editor = ["level_editor", window_background_color,list_background_color,
                    window_text_color,
                    button_alt_color,button_alt_text_color]

    node_grid = ["node_grid",node_grid_background_color, node_grid_lines_color,
                 node_grid_alt_lines_color, node_selected_color, node_title_color,
                 node_title_background_color, node_background_color,
                 node_text_color, node_wire_color, node_socket_trigger_color,
                 node_socket_file_color, node_socket_object_color,
                 node_socket_number_color, node_socket_text_color, node_socket_list_color,
                 node_socket_boolean_color, node_wire_error_color,
                 node_outliner_label_0,node_outliner_label_1,node_outliner_label_2,
                 node_outliner_label_3]
    
    unit_editor = ["unit_editor", unit_editor_rule_0, unit_editor_rule_1, unit_editor_rule_2,
                   unit_editor_rule_3, unit_editor_rule_4, unit_editor_rule_5]

    level_editor_labels = ["level_editor", "window_background_color",
                           "list_background_color",
                    "window_text_color",
                    "button_alt_color","button_alt_text_color"]

    node_grid_labels = ["node_grid","node_grid_background_color",
                        "node_grid_lines_color",
                 "node_grid_alt_lines_color", "node_selected_color","node_title_color",
                 "node_title_background_color", "node_background_color",
                 "node_text_color", "node_wire_color", "node_socket_trigger_color",
                 "node_socket_file_color", "node_socket_object_color",
                 "node_socket_number_color", "node_socket_text_color","node_socket_list_color",
                 "node_socket_boolean_color", "node_wire_error_color",
                        "node_outliner_label_0","node_outliner_label_1","node_outliner_label_2",
                        "node_outliner_label_3"]
    
    unit_editor_labels = ["unit_editor", "unit_editor_rule_0", "unit_editor_rule_1", "unit_editor_rule_2",
                   "unit_editor_rule_3", "unit_editor_rule_4", "unit_editor_rule_5"]

    groups = [level_editor, node_grid, unit_editor]


colorthemes = {"midnight_spark": midnight_spark(),
               "charcoal": charcoal(), 
               "ocean_waves": ocean_waves(), 
               "chocolate": chocolate(), 
               "chili_pepper": chili_pepper(), 
               "turnroot": turnroot(), 
               "custom": custom(), 
               }




















