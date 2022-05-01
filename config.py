from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

import subprocess

eww_config = "/etc/nixos/qtile/eww"


def eww_update(key, value):
    subprocess.run(["eww", "-c", eww_config, "update", f"{key}={value}"])


mod = "mod4"
terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="""
        Move window to the left
    """),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="""
        Move window to the right
    """),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="""
        Move window down
    """),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="""
        Grow window to the left
    """),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="""
        Grow window to the right
    """),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="""
        Grow window down
    """),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "space", lazy.spawn("rofi -modi drun -show drun"), desc="""
        Spawn a command using a prompt widget
    """),
]

volumeup = "XF86AudioRaiseVolume"
volumeupcmd = "pactl -- set-sink-volume @DEFAULT_SINK@ +1%"

volumedown = "XF86AudioLowerVolume"
volumedowncmd = "pactl -- set-sink-volume @DEFAULT_SINK@ -1%"


def lower_volume(qtile):
    subprocess.run(volumedowncmd.split(' '))


def raise_volume(qtile):
    subprocess.run(volumeupcmd.split(' '))


keys.extend(
        [
            Key([], volumeup, lazy.function(raise_volume)),
            Key([], volumedown, lazy.function(lower_volume))
        ]
)

current_window = None


def move_to(qtile, group_name):
    qtile.groups_map[group_name].cmd_toscreen()
    eww_update("wp_val", group_name)


def move_window_to(qtile, group_name):
    if current_window is None:
        return
    current_window.cmd_togroup(group_name)
    qtile.groups_map[group_name].cmd_toscreen()
    eww_update("wp_val", group_name)


groups = [Group(i) for i in "0123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.function(move_to, i.name),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.function(move_window_to, i.name),
                desc="Switch to & move focused window to group {}"
                    .format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

margin = 30
border0 = "#a0b1d633"
border1 = "#1a1b2633"
layouts = [
    layout.MonadTall(margin=margin,
                     border_normal=border1, border_focus=border0,
                     border_width=5),
    layout.MonadThreeCol(margin=margin,
                         border_normal=border1, border_focus=border0,
                         border_width=5),
    layout.MonadWide(margin=margin,
                     border_normal=border1, border_focus=border0,
                     border_width=5),
    layout.Max(margin=margin,
               border_normal=border1, border_focus=border0,
               border_width=5),
    layout.TreeTab(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Gap(50),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod],
         "Button1",
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod],
         "Button3",
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

wmname = "placidusax"


# hooks
@hook.subscribe.client_focus
@hook.subscribe.client_name_updated
def update_window_bar(window):
    name = window.name
    global current_window
    current_window = window
    eww_update("window_val", name)


@hook.subscribe.layout_change
def update_layout_bar(layout, group):
    name = layout.name
    eww_update("layout_val", name.upper())
