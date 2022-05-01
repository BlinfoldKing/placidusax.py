{ username, config, lib, pkgs, ... }:
{
    imports = [
        ./placidusax.nix
    ];

    services.xserver.displayManager.defaultSession = "none+placidusax";
    services.xserver.windowManager = {
       placidusax.enable = true;
    };

    services.picom.enable = true;
    services.picom.activeOpacity = 1.0;
    services.picom.inactiveOpacity = 1.0;
    services.picom.backend = "glx";
    services.picom.experimentalBackends = true;
    services.picom.settings = {
      shadow = true;
      blur = { 
        method = "dual_kawase";
        size = 20;
        deviation = 5.0;
      };
    };


  home-manager.users.${username} = {
    programs.rofi = {
        enable = true;
        terminal = "kitty";
        theme = /etc/nixos/qtile/rofi.rasi;
    };

    services.dunst.enable = true;
  };
}
